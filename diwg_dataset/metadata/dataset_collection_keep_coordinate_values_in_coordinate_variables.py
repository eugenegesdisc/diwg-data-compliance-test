"""
    Retrieve all groups, variables, attributes
      and their coordinate attributes in a dataset.
"""
import glob
from diwg_dataset.metadata.dataset_keep_coordinate_values_in_coordinate_variables import (
    DatasetKeepCoordValuesInCoordVariables
)
class DatasetCollectionKeepCoordValuesInCoordVariables:
    """
        This class is for testing:
            Keep Coordinate Values in Coordinate Variables
    """
    def get_coordinates_values_in_groups_variables_attributes(
            self,dataset_name_listfile:str)->dict:
        """
            Retrieve all coordinates and find its location in groups, variables, or attributes.
            This function utilizes gdalmdiminfo to retrieve groups, variables, attributes,
             which should only work with dataset with multi-dimensional arrays, 
             i.e. netcdf, hdf, hdfeos.
            @return: 
            {
            collection_name: "thecollection_list.file",
            error: "Error message if there is error",
            datasets: [
                {
                    "name":"example.nc",
                    "error":"message for error if error exists",
                    "groups":[
                        {
                            "fullpath":"/group1",
                            "parent_group":["","group1"],
                            "name":"group11"},
                        {
                            "fullpath":"",
                            "parent_group":[],
                            "name":"group1"}
                        ],
                    "variables":[
                        {
                            "fullpath":"/group1/variable1",
                            "parent_group":["","group1"],
                            "name":"variable1"},
                        {
                            "fullpath":"",
                            "parent_group":[],
                            "name":"variable0"}
                        ],
                    "attributes":[
                        {
                            "fullpath":"/group1",
                            "parent_path":["","group1"],
                            "variable":"variable1",
                            "name":"attribute1"},
                        {
                            "fullpath":"/group1",
                            "parent_path":["","group1"]
                            "name":"attribute2"}
                        {
                            "fullpath":"",
                            "parent_group":[]
                            "name":"attribute0"}
                        ],
                    "coordinates":[
                        {
                            "fullpath":"/group1",
                            "parent_path":["","group1"],
                            "type":"variable",
                            "name":"coord1"},
                        {
                            "fullpath":"/group1/variable1",
                            "parent_path":["","group1","variable1"],
                            "type":"attribute",
                            "name":"coord2"},
                        {
                            "fullpath":"/group1",
                            "parent_path":["","group1"],
                            "type":"group",
                            "name":"coord3"}
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
                        dmp = DatasetKeepCoordValuesInCoordVariables()
                        _the_ret["datasets"].append(
                            dmp.get_coordinates_values_in_groups_variables_attributes(
                                _the_sfile))
        except Exception as err:
            _the_ret["error"]=str(err)

        return _the_ret
