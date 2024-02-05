"""
    Include Georeference Information with Geospatial Coordinates

    https://wiki.earthdata.nasa.gov/display/ESDSWG/Include+Georeference+Information+with+Geospatial+Coordinates

"""
import re
import json
import pytest
import cfunits

from diwg_dataset.metadata.dataset_include_georeference_information import (
    DatasetIncludeGeoreferenceInformation)

def setup_module(module):
    """Setup at the module level"""
    print("setup module level")


def teardown_module(module):
    """Setup at the module level"""
    print("teardown module level")

@pytest.fixture(scope="class")
def dataset(request):
    """
        Retrieve the dataset-name from the command line options.
        Expect the following
        the_ret_dataset = 
            {
            "name":"example.nc",
            "error":"message for error if error exists",
            "variables":[
                    {
                        "fullpath":"/group1",
                        "parent_group":["","group1"],
                        "has_grid_mapping":True,
                        "has_crs_wkt": True,
                        "name":"variable1"},
                    {
                        "fullpath":"/group_g2",
                        "parent_group":["","group g2"],
                        "has_grid_mapping":True,
                        "has_crs_wkt": True,
                        "name":"variable2"},
                    {
                        "fullpath":"",
                        "parent_group":[],
                        "has_grid_mapping":False,
                        "has_crs_wkt": False,
                        "name":""},
                    {
                        "fullpath":"",
                        "parent_group":[],
                        "has_grid_mapping":True,
                        "has_crs_wkt": True,
                        "name":"variable0"}
                    ]
                ]
            }
    """
    #setup - class
    the_dataset_name=request.config.getoption("--dataset-name")
    the_dmp = DatasetIncludeGeoreferenceInformation()
    the_ret_dataset = the_dmp.get_variables(the_dataset_name)
    # return the_database_name
    yield the_ret_dataset
    # teardown - class
    the_ret_dataset = None
    the_dmp = None


@pytest.mark.skip_dataset_noneexistence
@pytest.mark.skip_dataset_is_grid_noneexistence
class TestClassDatasetIncludeGeoreferenceInformation:
    """
        This test class is for compliance check against the recommendation on

        Include Georeference Information with Geospatial Coordinates
        (Recommendation 3.6 in ESDS-RFC-036v1.2)
    """
    def setup_class(self):
        """
            Setup at the class level.
        self.ds = 
            {
                "name":"example.nc",
                "error":"message for error if error exists",
                "variables":
                [
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
C                ]
            }
        """
        pass

    def test_include_georeference_information(
            self, dataset):
        """
            Test variable has grid_mapping and crs_wkt.
            Intermediate test_results: A list of failed test results where each test result is 

            a dict:
                * dataset_name: name of a dataset or a sub-dataset
                * error: reason of incompliance or error
        """
        #dataset = self.ds
        if "error" in dataset:
            _the_dict = dict()
            _the_dict["error"]=dataset["error"]
            _the_dict["dataset_name"]=dataset["name"]
            _the_reason = json.dumps(_the_dict)
            pytest.xfail(_the_reason)
        _errors = list()
        _warnings = list()
        for _the_var in dataset['variables']:
            self._check_variable_has_grid_mapping_wkt(
                _errors,_warnings,_the_var)
        _the_o = dict()
        _the_o["dataset_name"]=dataset["name"]
        _the_o["errors"] = _errors
        _the_o["warnings"] = _warnings
        test_except_message = json.dumps(_the_o)
        if (not _errors
            and _warnings):
            pytest.skip(test_except_message)
        assert len(_errors) == 0, test_except_message

    def _check_variable_has_grid_mapping_wkt(
            self, errors:list,warnings:list,
            variable:dict):
        """
            Test 1: grid variable has "grid_mapping". If no "grid_mapping",
            it sets to "warning" where data prorovider does not provide or use
            "grid_mapping".

            Test 2: grid variable has "crs_wkt" attribute in the variable 
            referred to by "grid_mapping"..

            Parameters:
                errors(list): error list
                warnings(list): list of warnings with no grid_mapping or not supported.
                variable - 
                        {
                        "fullpath":"/group_g2",
                        "parent_group":["","group g2"],
                        "has_grid_mapping":True,
                        "has_grid_mapping_name":True,
                        "has_crs_wkt": True,
                        "name":"variable2"},
        """
        # Check 1: grid_mapping attribute/group variable
        if not variable["has_grid_mapping"]:
            _the_o = dict()
            _p_path = variable["fullpath"]
            _v_name = variable["name"]
            _v_full_name = _v_name
            if _p_path:
                _v_full_name = f"{_p_path}/{_v_name}"
            _the_o["variable_name"] = _v_full_name
            _the_o["skipped"]=("No grid_mapping which may be result of using "
                                "non-supported data "
                                "format or dava provider chosing not to prvoide.")
            warnings.append(_the_o)
            return
        # Check 2: grid_mapping_name
        if not variable["has_grid_mapping_name"]:
            _the_o = dict()
            _p_path = variable["fullpath"]
            _v_name = variable["name"]
            _v_full_name = _v_name
            if _p_path:
                _v_full_name = f"{_p_path}/{_v_name}"
            _the_o["variable_name"] = _v_full_name
            _the_o["error"]=("No grid_mapping_name in the group variable"
                               " referred by grid_mapping")
            errors.append(_the_o)
        if not variable['has_crs_wkt']:
            _the_o = dict()
            _p_path = variable["fullpath"]
            _v_name = variable["name"]
            _v_full_name = _v_name
            if _p_path:
                _v_full_name = f"{_p_path}/{_v_name}"
            _the_o["variable_name"] = _v_full_name
            _the_o["error"]=("No crs_wkt provided.")
            errors.append(_the_o)
