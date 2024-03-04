"""
    For recommendation: 

    Adopt Semantically Rich Dataset Release Identifiers

    Partition of CRID & verify valid.
"""
import glob
from diwg_dataset.dataname.filename_dataset_adopt_semantically_rich_dataset_release_identifiers import (
    FilenameDatasetAdoptSemanticallyRichDatasetReleaseIdentifiers
)
class FilenameDatasetCollectionAdoptSemanticallyRichDatasetReleaseIdentifiers:
    """
        This class is for testing:
            Adopt Semantically Rich Dataset Release Identifiers

            https://wiki.earthdata.nasa.gov/display/ESDSWG/Adopt+Semantically+Rich+Dataset+Release+Identifiers
    """        
    def validate_dataname_crid_partitions(
            self,dataset_name_listfile:str,
            dataset_crid:str=None,
            dataset_crid_major:str=None,
            dataset_crid_major_group:str="major",
            dataset_crid_minor:str=None,
            dataset_crid_minor_group:str="major",
            dataset_crid_patch:str=None,
            dataset_crid_patch_group:str="patch")->dict:
        """
            Parition of CRID & verify if it has all Major, Minor, & Patch components.
            @return: 
            {
            collection_name: "thecollection_list.file",
            error: "Error message if there is error",
            datasets: [
                    {
                        "dataset_name":"/some/path/SMAP_L4_SM_gph_20200915T193000_Vv5014_001.h5",
                        "error":"message for error if error exists",
                        "partition":
                            {
                                "filename":"SMAP_L4_SM_gph_20200915T193000_Vv5014_001.h5",
                                "id":"SMAP_L4_SM_gph",
                                "crid":"Vv5014_001",
                                "major": "v5014",
                                "minor":"001",
                                "patch":"")
                            }
                        "valid":
                            {
                                "skip": False,
                                "status": False,
                                "message": "Missing: patch"                        
                            }
                    }
                ],
                "valid": {
                    "skip": False
                }
            }
        """
        _ret = self.get_dataname_crid_partitions(
            dataset_name_listfile=dataset_name_listfile,
            dataset_crid=dataset_crid,
            dataset_crid_major=dataset_crid_major,
            dataset_crid_major_group=dataset_crid_major_group,
            dataset_crid_minor=dataset_crid_minor,
            dataset_crid_minor_group=dataset_crid_minor_group,
            dataset_crid_patch=dataset_crid_patch,
            dataset_crid_patch_group=dataset_crid_patch_group)
        _datasets = _ret['datasets']
        _new_ds = list()
        _ret['datasets'] = _new_ds
        _ret['valid'] = dict()
        _skip = 0
        for _ds in _datasets:
            if _ds['valid']['skip']:
                _skip += 1
                continue
            if not _ds['valid']['status']:
                _new_ds.append(_ds)
        if _skip == len(_datasets):
            _ret['valid']['skip'] = True
        else:
            _ret['valid']['skip'] = False

        return _ret

    def get_dataname_crid_partitions(
            self,dataset_name_listfile:str,
            dataset_crid:str=None,
            dataset_crid_major:str=None,
            dataset_crid_major_group:str="major",
            dataset_crid_minor:str=None,
            dataset_crid_minor_group:str="major",
            dataset_crid_patch:str=None,
            dataset_crid_patch_group:str="patch")->dict:
        """
            Parition of CRID & verify if it has all Major, Minor, & Patch components.
            @return: 
            {
            collection_name: "thecollection_list.file",
            error: "Error message if there is error",
            datasets: [
                    {
                        "dataset_name":"/some/path/SMAP_L4_SM_gph_20200915T193000_Vv5014_001.h5",
                        "error":"message for error if error exists",
                        "partition":
                            {
                                "filename":"SMAP_L4_SM_gph_20200915T193000_Vv5014_001.h5",
                                "id":"SMAP_L4_SM_gph",
                                "crid":"Vv5014_001",
                                "major": "v5014",
                                "minor":"001",
                                "patch":"")
                            }
                        "valid":
                            {
                                "skip": False,
                                "status": False,
                                "message": "Missing: patch"                        
                            }
                    }
                ]
            }
        """
        _the_ret = dict()
        _the_ret["collection_name"] = dataset_name_listfile
        _the_ret["datasets"] = list()
        _the_ret['valid'] = dict()
        if (not dataset_crid or
            not dataset_crid_major or
            not dataset_crid_minor or 
            not dataset_crid_patch):
            _the_ret["valid"]["skip"] = True
            return _the_ret
        else:
            _the_ret["valid"]["skip"] = False

        try:
            with open(dataset_name_listfile, "r",encoding="utf-8") as _the_file:
                _the_lines = _the_file.readlines()
            for _line in _the_lines:
                _the_line = _line.strip()
                if _the_line:
                    _the_sfiles = glob.glob(_the_line)
                    # in case of a single GDAL dataset
                    if len(_the_sfiles) == 0:
                        _the_sfiles = [_the_line]
                    for _the_sfile in _the_sfiles:
                        dmp = FilenameDatasetAdoptSemanticallyRichDatasetReleaseIdentifiers()
                        _the_ds = dmp.valid_dataname_crid_partitions(
                            dataset_name=_the_sfile,
                            dataset_crid=dataset_crid,
                            dataset_crid_major=dataset_crid_major,
                            dataset_crid_major_group=dataset_crid_major_group,
                            dataset_crid_minor=dataset_crid_minor,
                            dataset_crid_minor_group=dataset_crid_minor_group,
                            dataset_crid_patch=dataset_crid_patch,
                            dataset_crid_patch_group=dataset_crid_patch_group)
                        if _the_ds["valid"]["skip"]:
                            continue
                        if _the_ds["valid"]["status"]:
                            continue
                        _the_ret["datasets"].append(_the_ds)
        except Exception as err:
            _the_ret["error"]=str(err)

        return _the_ret
