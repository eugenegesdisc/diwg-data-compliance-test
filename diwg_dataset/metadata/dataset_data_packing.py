"""
    Retrieve metadata on packing conventions in a dataset.
"""
from osgeo import gdal

class DatasetMetaPacking:
    """
        This class is for testing:
            Distinguish clearly between HDF and netCDF packing conventions
        
    """
    def get_packing_metadata(self,dataset_name:str)->dict:
        """
            Retrieve list of subdataset metadata.
            @return:
            {
            "dataset_name": "test_dataset.nc",
            "error": "add error here if there is a general error",
            "sudbdatasets":[{
                "name":"test_dataset.nc",
                "error":"message for error if error exists",
                "is_scaled": True,
                "scaling":{
                    "scale_factor": 0.1,
                    "add_offset": 1000.0
                }
                "packing":{
                    "packing_convention":"netCDF",
                    "packing_convention_description": 
                        "unpacked = scale_factor x packed + add_offset"
                }
            }]
            }
        """
        gdal.UseExceptions()
        _the_ret = dict()
        _the_ret["dataset_name"]=dataset_name
        _the_ret["subdatasets"]=list()

        try:
            with gdal.Open(dataset_name, gdal.GA_ReadOnly) as the_ds:
                if not isinstance(the_ds, gdal.Dataset):
                    _the_ret["error"] = "Failed at opening the dataset."
                    return _the_ret

                _the_info = gdal.Info(the_ds, format="json")

                # loop through all subdatasets
                _the_subdatasets = self._gdal_get_subdatasets(_the_info)

                for _the_sd_name in _the_subdatasets:
                    _s_metadata_packing = dict()
                    _s_metadata_packing["name"] = _the_sd_name
                    with gdal.Open(_the_sd_name, gdal.GA_ReadOnly) as the_sds:
                        if not isinstance(the_sds, gdal.Dataset):
                            _s_metadata_packing["error"] = "Failed at opening the subdataset."
                        else:
                            self._gdal_get_subdataset_metadata_packing(
                                _s_metadata_packing, the_sds)
                        _the_ret['subdatasets'].append(_s_metadata_packing)

                if the_ds.RasterCount>0:
                    _the_root = dict()
                    _the_root["dataset_name"] = dataset_name
                    self._gdal_get_subdataset_metadata_packing(
                        _the_root, the_ds)
                    _the_ret['subdatasets'].append(_the_root)

        except Exception as err:
            _the_ret["error"]=str(err)
        return _the_ret

    def _gdal_get_subdatasets(self, dataset_info):
        _the_ret = []
        if "metadata" not in dataset_info:
            return _the_ret
        if "SUBDATASETS" not in dataset_info["metadata"]:
            return _the_ret
        _sd_keys = [k for k in dataset_info[
            "metadata"]["SUBDATASETS"] if "_NAME" in k]
        _the_ret = [dataset_info["metadata"][
            "SUBDATASETS"][k] for k in _sd_keys]
        return _the_ret

    def _gdal_get_subdataset_metadata_packing(
            self, metadata_packing:dict, dataset:gdal.Dataset):
        the_metadata = dataset.GetMetadata()
        #scale_factor
        the_scale_factors = [(k,v) for k,v in the_metadata.items()
                                if k.endswith("scale_factor")]
        the_scale_factor = None
        if len(the_scale_factors) > 0:
            the_scale_factor = the_scale_factors[0][1]
        #add_offset
        the_add_offsets = [(k,v) for k,v in the_metadata.items()
                                if k.endswith("add_offset")]
        the_add_offset = None
        if len(the_add_offsets) > 0:
            the_add_offset = the_add_offsets[0][1]
        metadata_packing["is_scaled"] = (
            the_scale_factor is not None
            and
            the_add_offset is not None
        )
        #set scaling
        metadata_packing["scaling"]={}
        if the_scale_factor:
            metadata_packing["scaling"]["scale_factor"] = the_scale_factor
        if the_add_offset:
            metadata_packing["scaling"]["add_offset"] = the_add_offset
        #packing
        metadata_packing["packing"]={}
        the_packing_convs = [(k,v) for k,v in the_metadata.items()
                                if k.endswith("packing_convention")]
        the_packing_conv = None
        if len(the_packing_convs)>0:
            the_packing_conv = the_packing_convs[0][1]
        if the_packing_conv:
            metadata_packing["packing"]["packing_convention"] = the_packing_conv
        the_pack_con_descs = [(k,v) for k,v in the_metadata.items()
                                if k.endswith("packing_convention_description")]
        the_pack_con_desc = None
        if len(the_pack_con_descs)>0:
            the_pack_con_desc = the_pack_con_descs[0][1]
        if the_pack_con_desc:
            metadata_packing["packing"][
                "packing_convention_description"] = the_pack_con_desc


