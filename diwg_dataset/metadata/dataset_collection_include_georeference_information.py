"""
    For recommendation:
    Include Georeference Information with Geospatial Coordinates
    
    Retrieve grid variables and check its grid_mapping/wkt info
    in earch grid dataset in a collection.
"""
import glob
from diwg_dataset.metadata.dataset_include_georeference_information import (
    DatasetIncludeGeoreferenceInformation
)
class DatasetCollectionIncludeGeoreferenceInformation:
    """
        This class is for testing:
            Include Georeference Information with Geospatial Coordinates

            https://wiki.earthdata.nasa.gov/display/ESDSWG/Include+Georeference+Information+with+Geospatial+Coordinates
    """
    def get_variables(self,dataset_name_listfile:str)->dict:
        """
            Retrieve all the variables and their grid_mapping/wkt info.
            @return: 
            {
            collection_name: "thecollection_list.file",
            error: "Error message if there is error",
            datasets: [
                    {
                        "dataset_name":"example.nc",
                        "error":"message for error if error exists",
                        "variables":[
                            {
                                "fullpath":"/group1",
                                "parent_group":["","group1"],
                                "has_grid_mapping":True,
                                "has_grid_mapping_name":True,
                                "has_crs_wkt": True,
                                "name":"variable1"},
                            {
                                "fullpath":"/group_g2",
                                "parent_group":["","group g2"],
                                "has_grid_mapping":True,
                                "has_grid_mapping_name":True,
                                "has_crs_wkt": True,
                                "name":"variable2"},
                            {
                                "fullpath":"",
                                "parent_group":[],
                                "has_grid_mapping":False,
                                "has_grid_mapping_name":False,
                                "has_crs_wkt": False,
                                "name":""},
                            {
                                "fullpath":"",
                                "parent_group":[],
                                "has_grid_mapping":True,
                                "has_grid_mapping_name":True,
                                "has_crs_wkt": True,
                                "name":"variable0"}
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
                        dmp = DatasetIncludeGeoreferenceInformation()
                        _the_ret["datasets"].append(
                            dmp.get_variables(_the_sfile))
        except Exception as err:
            _the_ret["error"]=str(err)

        return _the_ret
