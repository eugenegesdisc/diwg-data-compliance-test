"""
    For recommendation:

    Standardize File Extensions for HDF5/netCDF Files

    verify if the dataset (granule) filename has proper extension.

"""
import os
from osgeo import gdal

class FilenameDatasetStandardizeFileExtensions:
    """
        This class is for testing:
            Standardize File Extensions for HDF5/netCDF Files

            https://wiki.earthdata.nasa.gov/pages/viewpage.action?pageId=182297715
    """
    def get_dataname_extension(self, dataset_name:str)->dict:
        """
            Get filename exteion for the dataset.
            @return: 
            {
                "dataset_name":"example.nc",
                "error":"message for error if error exists",
                "extension":
                        {
                            "driver_short_name":"netCDF",
                            "HDFEOSVersion":"",
                            "expected":".nc",
                            "extension":".nc",
                            "valid": True
                        }
            }
        """
        gdal.UseExceptions()
        _the_ret = dict()
        _the_ret["dataset_name"] = dataset_name
        _the_ret["extension"] = dict()
        try:
            _the_info = gdal.Info(dataset_name, format="json",
                                  listMDD=True,extraMDDomains=['all'],
                                  reportProj4=True)

            self._gdal_get_file_extension(
                dataset_name=dataset_name,
                ext_info=_the_ret,
                dataset_info=_the_info)
            self._check_file_extension(_the_ret)
        except Exception as err:
            _the_ret["error"]=str(err)

        return _the_ret

    def _check_file_extension(
            self, ext_info:dict):
        if 'extension' not in ext_info:
            return
        _the_ext = ext_info["extension"]
        if "driver_short_name" not in _the_ext:
            return
        _the_driver = _the_ext["driver_short_name"].upper()
        # if not in scope (HDF5, HDFEOS5, and NETCDF), not add "valid" attribute
        _in_scope_format = ["HDF5", "NETCDF"]
        if _the_driver not in _in_scope_format:
            return
        # validate "NETCDF" file extension
        _expect_ext = ".nc"
        if _the_driver == "NETCDF":
            _the_ext['expected'] = _expect_ext
            if _the_ext["extension"] == _expect_ext:
                _the_ext["valid"] = True
            else:
                _the_ext["valid"] = False
            return
        # "HDF5"
        _expect_ext = ".h5"
        if  not _the_ext["HDFEOSVersion"]:
            _the_ext['expected'] = _expect_ext
            if _the_ext["extension"] == _expect_ext:
                _the_ext["valid"] = True
            else:
                _the_ext["valid"] = False
            return

        # HDFEOS5
        _expect_ext = ".he5"
        if _the_ext["extension"] == _expect_ext:
            _the_ext["valid"] = True
        else:
            _the_ext["valid"] = False

    def _gdal_get_file_extension(
            self, dataset_name:str,
            ext_info:dict,
            dataset_info:dict):
        _the_ext = ext_info["extension"]
        # get driver name
        if 'driverShortName' in dataset_info:
            _the_ext["driver_short_name"] = dataset_info["driverShortName"]
        else:
            _the_ext["driver_short_name"] = ""
        # get HDFEOSVersion
        _the_ext["HDFEOSVersion"] = self._gdal_get_hdfeos_version(
            dataset_info)
        # get file extension
        _the_ext['extension'] = self._gdal_get_file_extension_from_info(
            dataset_name, dataset_info) 

    def _gdal_get_file_extension_from_info(
            self, dataset_name:str,
            dataset_info:dict)->str:
        the_files = list()
        if 'files' in dataset_info:
            the_files = dataset_info["files"]
        the_file = dataset_name
        # in case dataset_name is a subdataset string
        for f in the_files:
            if f in dataset_name:
                the_file = f
                break
        # get extension
        the_ext = os.path.splitext(the_file)[1]
        return the_ext



    def _gdal_get_hdfeos_version(
            self,dataset_info:dict)->str:
        if 'metadata' not in dataset_info:
            return ""
        the_info = dataset_info["metadata"]
        if '' not in the_info:
            return ""
        the_info = the_info['']
        for k in the_info:
            if k.endswith('HDFEOSVersion'):
                return the_info[k]
        return ""
