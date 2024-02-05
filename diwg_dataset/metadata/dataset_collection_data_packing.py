"""
    Retrieve metadata on packing conventions in a dataset.
"""
import glob
from diwg_dataset.metadata.dataset_data_packing import (
    DatasetMetaPacking
)
class DatasetCollectionMetaPacking:
    """
        This class is for testing:
            Distinguish clearly between HDF and netCDF packing conventions
        
    """
    def get_packing_metadata(self,dataset_name_listfile:str)->dict:
        """
            Retrieve list of subdataset metadata.
            @return:
            {
            collection_name: "thecollection_list.file",
            error: "Error message if there is error",
            datasets: [{
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
            }]
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
                        dmp = DatasetMetaPacking()
                        _the_ret["datasets"].append(
                            dmp.get_packing_metadata(_the_sfile))
        except Exception as err:
            _the_ret["error"]=str(err)

        return _the_ret
