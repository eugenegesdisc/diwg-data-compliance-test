"""
    For recommendation: 

    Standardize File Extensions for HDF5/netCDF Files

    verify if the dataset (granule) filename has proper extension.
"""
import glob
from diwg_dataset.dataname.filename_dataset_standardize_file_extensions import (
    FilenameDatasetStandardizeFileExtensions
)
class FilenameDatasetCollectionStandardizeFileExtensions:
    """
        This class is for testing:
            Standardize File Extensions for HDF5/netCDF Files

            https://wiki.earthdata.nasa.gov/pages/viewpage.action?pageId=182297715
    """
    def validate_dataname_extension(self,dataset_name_listfile:str)->dict:
        """
            Retrieve file extensions of datasets (granules) in a collection.
            @return: 
            {
            collection_name: "thecollection_list.file",
            error: "Error message if there is error",
            datasets: [
                    {
                        "dataset_name":"example.HDF5",
                        "error":"message for error if error exists",
                        "extension":
                                {
                                    "driver_short_name":"HDF5",
                                    "HDFEOSVersion":"",
                                    "expected":".h5",
                                    "extension":".nc",
                                    "valid": False}
                    },
                ],
                "valid": {
                    "skip": False
                }
            }
        """
        _ret = self.get_dataname_extension(
            dataset_name_listfile=dataset_name_listfile)
        _datasets = _ret['datasets']
        _new_ds = list()
        _ret['datasets'] = _new_ds
        _ret['valid'] = dict()
        _skip = 0
        for _ds in _datasets:
            if ('extension' not in _ds
                or 'valid' not in _ds['extension']):
                _skip += 1
                continue
            if not _ds['extension']['valid']:
                _new_ds.append(_ds)
        if _skip == len(_datasets):
            _ret['valid']['skip'] = True
        else:
            _ret['valid']['skip'] = False

        return _ret

    def get_dataname_extension(self,dataset_name_listfile:str)->dict:
        """
            Retrieve file extensions of datasets (granules) in a collection.
            @return: 
            {
            collection_name: "thecollection_list.file",
            error: "Error message if there is error",
            datasets: [
                    {
                        "dataset_name":"example.nc",
                        "error":"message for error if error exists",
                        "extension":
                                {
                                    "driver_short_name":"netCDF",
                                    "HDFEOSVersion":"",
                                    "extension":".nc",
                                    "valid": True}
                    },
                    {
                        "dataset_name":"example2.HDFEOS",
                        "extension":
                                {
                                    "driver_short_name":"HDF4",
                                    "HDFEOSVersion":"HDFEOS_V2.14",
                                    "extension":".HDFEOS"}
                    }
                ]
            }
        """
        _the_ret = dict()
        _the_ret["collection_name"] = dataset_name_listfile
        _the_ret["datasets"] = list()

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
                        dmp = FilenameDatasetStandardizeFileExtensions()
                        _the_ret["datasets"].append(
                            dmp.get_dataname_extension(_the_sfile))
        except Exception as err:
            _the_ret["error"]=str(err)

        return _the_ret
