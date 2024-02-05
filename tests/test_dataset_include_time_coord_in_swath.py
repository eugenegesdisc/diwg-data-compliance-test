"""
Include Time Coordinate in Swath Structured Data

https://wiki.earthdata.nasa.gov/display/ESDSWG/Include+Time+Coordinate+in+Swath+Structured+Data

"""
import re
import json
import pytest
import cfunits

from diwg_dataset.metadata.dataset_include_time_coord_in_swath import (
    DatasetIncludeTimeCoordInSwath)

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
    """
    #setup - class
    the_dataset_name=request.config.getoption("--dataset-name")
    the_dmp = DatasetIncludeTimeCoordInSwath()
    the_ret_dataset = the_dmp.get_variables_with_dims(the_dataset_name)
    # return the_database_name
    yield the_ret_dataset
    # teardown - class
    the_ret_dataset = None
    the_dmp = None

@pytest.mark.skip_dataset_noneexistence
@pytest.mark.skip_dataset_is_swath_noneexistence
class TestClassDatasetIncludeTimeCoordInSwath:
    """
        This test class is for compliance check against the recommendation on
        Include Time Coordinate in Swath Structured Data.

        Include Time Coordinate in Swath Structured Data
        (Recommendation 3.4 in ESDS-RFC-036v1.2)
    """
    def setup_class(self):
        """
            Setup at the class level.
        self.ds = 
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
        """
        pass

    def test_include_time_coord_in_swath(
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
        # test if dataset has time variable

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
        test_except_message = json.dumps(_the_o)
        assert len(test_results) == 0, test_except_message
