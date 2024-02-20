"""
    Retrieve metadata on packing conventions in a dataset.
"""
import glob
from diwg_dataset.metadata.dataset_variable_physical_units import (
    DatasetVariablePhysicalUnits
)
class DatasetCollectionVariablePhysicalUnits:
    """
        This class is for testing:
            Use the Units Attribute Only for Variables with Physical Units
    """
    def get_variable_units(self,dataset_name_listfile:str)->dict:
        """
            Retrieve all the variables and their units.
            @return: 
            {
            collection_name: "thecollection_list.file",
            error: "Error message if there is error",
            datasets: [{
                "dataset_name":"example.nc",
                "error":"message for error if error exists",
                "variables":[
                        {
                        "path": 'NETCDF:"somevariable.nc"://group1/variable1',
                        "fullname":"//group1/variable1",
                        "name": "variable1",
                        "units":"mm"
                        }
                    ]
                }]
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
                        dmp = DatasetVariablePhysicalUnits()
                        _the_ret["datasets"].append(
                            dmp.get_variable_units(_the_sfile))
        except Exception as err:
            _the_ret["error"]=str(err)

        return _the_ret
