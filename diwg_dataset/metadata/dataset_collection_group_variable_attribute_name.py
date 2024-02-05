"""
    Retrieve all names of groups, variables, and attributes in a dataset.
"""
import glob
from diwg_dataset.metadata.dataset_group_variable_attribute_name import (
    DatasetGroupVariableAttributeName
)
class DatasetCollectionGroupVariableAttributeName:
    """
        This class is for testing:
            Character Set for User-Defined Group, Variable, and Attribute Names
    """
    def get_group_variable_attribute_names(
            self,dataset_name_listfile:str)->dict:
        """
            Retrieve the metadata.
            @return: 
            {
            collection_name: "thecollection_list.file",
            error: "Error message if there is error",
            datasets: [{
                "name":"example.nc",
                "error":"message for error if error exists",
                "group_names":["group1", "2group"],
                "variable_names":["var1", "var-2"],
                "attribute_names":["attr1", "attr_2"]
            }]
            }
        """

        the_ret = dict()
        the_ret["collection_name"] = dataset_name_listfile
        the_ret["datasets"] = list()
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
                        dgva = DatasetGroupVariableAttributeName()
                        the_ret["datasets"].append(
                            dgva.get_group_variable_attribute_names(_the_sfile))
        except Exception as err:
            the_ret["error"]=str(err)

        return the_ret
