"""
    Retrieve all variables and their coordinate attributes in each dataset in
    a dataset collection.
    "include_time" is set true if it has coord ending with "time" (case-insensitive)
"""
import glob
from diwg_dataset.metadata.dataset_include_time_coord_in_swath import (
    DatasetIncludeTimeCoordInSwath
)
class DatasetCollectionIncludeTimeCoordInSwath:
    """
        This class is for testing:
            Include Time Coordinate in Swath Structured Data
    """
    def get_variables_with_dims(self,dataset_name_listfile:str)->dict:
        """
            Retrieve all the variables with dimensions and coordinates for each dataset in 
            a dataset collection.
            This function utilizes gdalmdiminfo to retrieve variables, which should only
            work with dataset with multi-dimensional arrays, i.e. netcdf, hdf, hdfeos.
            @return: 
            {
            collection_name: "thecollection_list.file",
            error: "Error message if there is error",
            datasets: [
                    {
                        "name":"example.nc",
                        "error":"message for error if error exists",
                        "time_variables":['/somegroup/time'],
                        "variables":[
                            {
                                "path": 'NETCDF:"somefile.nc"://group1/variable1',
                                "fullname":"//group1/variable1",
                                "name":"variable1",
                                "dimensions":['/nTimes','/nTrack'],
                                "coordinates":['time','lat','lon'],
                                "include_time": True}
                            ]
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
                        dmp = DatasetIncludeTimeCoordInSwath()
                        _the_ret["datasets"].append(
                            dmp.get_variables_with_dims(_the_sfile))
        except Exception as err:
            _the_ret["error"]=str(err)

        return _the_ret
