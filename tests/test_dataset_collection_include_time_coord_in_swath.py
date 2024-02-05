"""
Include Time Coordinate in Swath Structured Data

https://wiki.earthdata.nasa.gov/display/ESDSWG/Include+Time+Coordinate+in+Swath+Structured+Data

"""
import re
import json
import pytest
import cfunits

from diwg_dataset.metadata.dataset_collection_include_time_coord_in_swath import (
    DatasetCollectionIncludeTimeCoordInSwath)

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
                        "name":"example.nc",
                        "error":"message for error if error exists",
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
    #setup - class
    the_dataset_collection_filename=request.config.getoption("--dataset-name-list")
    the_dmp = DatasetCollectionIncludeTimeCoordInSwath()
    the_ret_dataset = the_dmp.get_variables_with_dims(the_dataset_collection_filename)
    # return the_database_name
    yield the_ret_dataset
    # teardown - class
    the_ret_dataset = None
    the_dmp = None


@pytest.mark.skip_dataset_collection_noneexistence
@pytest.mark.skip_dataset_is_swath_noneexistence
class TestClassDatasetCollectionVariableUnits:
    """
        This test class is for compliance check against the recommendation on
        Use the Units Attribute Only for Variables with Physical Units.

        Use the Units Attribute Only for Variables with Physical Units
        (Recommendation 3.3 in ESDS-RFC-036v1.2)
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
                            "name":"example.nc",
                            "error":"message for error if error exists",
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
        pass

    def test_include_time_coord_in_swath(
            self, dataset_collection):
        """
            Test if time coordinate is included in coordinates of a swath data for each
            dataset in the collection.
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
            Test if time coordinate is included in coordinates of a swath data
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
        test_results = list()
        if len(dataset['time_variables']) < 1:
                _the_o = dict()
                _the_o["dataset_name"]=dataset["name"]
                _the_o["error"]=("No time variable found")
                test_results.append(_the_o)
        for _the_var in dataset['variables']:
            # skip these without coordinates (possibly not valid data?)
            if len(_the_var['coordinates'])<1:
                continue
            if not _the_var['include_time']:
                _the_o = dict()
                _the_o["variable_name"]=_the_var["fullname"]
                _the_o["error"]=("Coordinates does not include time")
                test_results.append(_the_o)
        _the_o = dict()
        _the_o["dataset_name"]=dataset["name"]
        _the_o["errors"]=test_results
        if len(test_results) == 0:
            return None
        else:
            return _the_o
