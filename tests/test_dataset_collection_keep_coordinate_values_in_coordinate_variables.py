"""
Keep Coordinate Values in Coordinate Variables

https://wiki.earthdata.nasa.gov/display/ESDSWG/Keep+Coordinate+Values+in+Coordinate+Variables

"""
import re
import json
import pytest
import cfunits

from diwg_dataset.metadata.dataset_collection_keep_coordinate_values_in_coordinate_variables import (
    DatasetCollectionKeepCoordValuesInCoordVariables)

def setup_module(module):
    """Setup at the module level"""
    print("setup module level")


def teardown_module(module):
    """Setup at the module level"""
    print("teardown module level")

@pytest.fixture(scope="class")
def dataset_collection(request):
    """
        Retrieve the dataset-name from the command line options.
        Expect the following
        the_ret_dataset = 
            {
            collection_name: "thecollection_list.file",
            error: "Error message if there is error",
            datasets: [
                {
                    "dataset_name":"example.nc",
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
    #setup - class
    the_dataset_collection_filename=request.config.getoption("--dataset-name-list")
    the_dmp = DatasetCollectionKeepCoordValuesInCoordVariables()
    the_ret_dataset = the_dmp.get_coordinates_values_in_groups_variables_attributes(
        the_dataset_collection_filename)
    # return the_database_name
    yield the_ret_dataset
    # teardown - class
    the_ret_dataset = None
    the_dmp = None


@pytest.mark.skip_dataset_collection_noneexistence
class TestClassDatasetCollectionKeepCoordValuesInCoordVariables:
    """
        This test class is for compliance check against the recommendation on

        Keep Coordinate Values in Coordinate Variables
        (Recommendation 3.5 in ESDS-RFC-036v1.2)
    """
    def setup_class(self):
        """
            Setup at the class level.
            self.ds = 
                {
                collection_name: "thecollection_list.file",
                error: "Error message if there is error",
                "time_variables":['/somegroup/time'],
                datasets: [
                    {
                        "dataset_name":"example.nc",
                        "error":"message for error if error exists",
                        "coords_in_groups":[
                                {
                                    "fullpath":"//group1",
                                    "parent_path":["/","group1"],
                                    "type":"group",
                                    "name":"coord3"}
                            ]
                            ],
                        "coords_not_in_variables":[
                                {
                                    "fullpath":"//group1/variable1",
                                    "parent_path":["/","group1","variable1"],
                                    "type":"attribute",
                                    "name":"coord2"},
                                {
                                    "fullpath":"//group1",
                                    "parent_path":["/","group1"],
                                    "type":"group",
                                    "name":"coord3"}
                                ]
                            ],
                        "coords_in_attributes":[
                                {
                                    "fullpath":"//group1/variable1",
                                    "parent_path":["/","group1","variable1"],
                                    "type":"attribute",
                                    "name":"coord2"}
                            ],
                        "coordinates":[
                                {
                                    "fullpath":"//group1",
                                    "parent_path":["/","group1"],
                                    "type":"variable",
                                    "name":"coord1"},
                                {
                                    "fullpath":"//group1/variable1",
                                    "parent_path":["/","group1","variable1"],
                                    "type":"attribute",
                                    "name":"coord2"},
                                {
                                    "fullpath":"//group1",
                                    "parent_path":["/","group1"],
                                    "type":"group",
                                    "name":"coord3"}
                            ]
                    }
                    ]
                }
        """
        pass

    def test_keep_coordinate_values_in_coordinate_variables(
            self, dataset_collection):
        """
            Test if coordinate values are defined in variables.
            Intermediate test_results: A list of failed test results where each test result is 
            a dict:
                * dataset_collection: name of a file containing a list of dataset or sub-dataset
                * error: reason of incompliance or error
        """
        if "error" in dataset_collection:
            _the_o = dict()
            _the_o["collection_name"]=dataset_collection['collection_name']
            _the_o["error"]=dataset_collection['error']
            _the_reason = json.dumps(_the_o)
            pytest.xfail(_the_reason)
        if len(dataset_collection['datasets'])<1:
            _the_o = dict()
            _the_o["collection_name"]=dataset_collection['collection_name']
            _the_o["error"]="Empty collection"
            _the_reason = json.dumps(_the_o)
            pytest.xfail(_the_reason)
        _test_results = list()
        _the_ref_ds = dataset_collection["datasets"][0]
        for dataset in dataset_collection["datasets"]:
            _the_result = self._process_one_dataset(dataset)
            if _the_result:
                _test_results.append(_the_result)
        _the_o = dict()
        _the_o["collection_name"]=dataset_collection["collection_name"]
        _the_o["errors"]=_test_results
        text_except_message = json.dumps(_the_o)
        assert len(_test_results) == 0, text_except_message

    def _process_one_dataset(
            self, dataset):
        """
            Test if coordinate values are defined in variables.
            Intermediate test_results: A list of failed test results where each test result is 
            a dict:
                * dataset_name: name of a dataset or a sub-dataset
                * error: reason of incompliance or error
        """
        #dataset = self.ds
        if "error" in dataset:
            _the_dict = dict()
            _the_dict["error"]=dataset["error"]
            _the_dict["dataset_name"]=dataset["dataset_name"]
            _the_reason = json.dumps(_the_dict)
            pytest.xfail(_the_reason)
        # test if dataset has time variable

        test_results = list()
        # test 1: check if all coordinate values are stored in variables
        if len(dataset['coords_not_in_variables']) > 0:
                for crd in dataset['coords_not_in_variables']:
                    _fullname = crd['fullname']
                    _name = crd['name']
                    _type = crd['type']
                    _the_o = dict()
                    _the_o["coord_name"]=f"{_fullname}/{_name}"
                    _the_o["error"]=(f"Not in variable. In type: {_type}")
                    test_results.append(_the_o)
        # test 2: check if coordiates are in attributes
        if len(dataset['coords_in_attributes']) > 0:
                for crd in dataset['coords_in_attributes']:
                    _fullname = crd['fullname']
                    _name = crd['name']
                    _type = crd['type']
                    _the_o = dict()
                    _the_o["coord_name"]=f"{_fullname}/{_name}"
                    _the_o["error"]=(f"In type: {_type}")
                    test_results.append(_the_o)
        # test 3: check if coordiate values are in groups, including both name and
        #         value in group, such as /day/2023/12/13
        if len(dataset['coords_in_groups']) > 0:
                for crd in dataset['coords_in_groups']:
                    _fullname = crd['fullname']
                    _name = crd['name']
                    _type = crd['type']
                    _the_o = dict()
                    _the_o["coord_name"]=f"{_fullname}/{_name}"
                    _the_o["error"]=(f"In type: {_type}")
                    test_results.append(_the_o)
        _the_o = dict()
        _the_o["dataset_name"]=dataset["dataset_name"]
        _the_o["errors"]=test_results
        if len(test_results) == 0:
            return None
        else:
            return _the_o
