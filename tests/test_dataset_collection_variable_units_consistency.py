"""
Consistent Units Attribute Value for Variables Across One Data Collection

https://wiki.earthdata.nasa.gov/display/ESDSWG/Consistent+Units+Attribute+Value+for+Variables+Across+One+Data+Collection
"""
import re
import json
import pytest

from diwg_dataset.metadata.dataset_collection_variable_units import (
    DatasetCollectionVariableUnits)

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
            datasets: [{
                "name":"example.nc",
                "error":"message for error if error exists",
                "variables":[
                        {
                        "path": 'NETCDF:"somevariable.nc"://group1/variable1',
                        "fullname":"//group1/variable1",
                        "name": "variable1",
                        "units":["mm"]
                        }
                    ]
                }]
            }
    """
    #setup - class
    the_dataset_collection_filename=request.config.getoption("--dataset-name-list")
    the_dmp = DatasetCollectionVariableUnits()
    the_ret_dataset = the_dmp.get_variable_units(the_dataset_collection_filename)
    # return the_database_name
    yield the_ret_dataset
    # teardown - class
    the_ret_dataset = None
    the_dmp = None


@pytest.mark.skip_dataset_collection_noneexistence
class TestClassDatasetCollectionVarialeUnitsConsistency:
    """
        This test class is for compliance check against the recommendation on
        Consistent Units Attribute Value for Variables Across One Data Collection.

        Consistent Units Attribute Value for Variables Across One Data Collection
        (Recommendation 3.2 in ESDS-RFC-036v1.2)
    """
    def setup_class(self):
        """
            Setup at the class level.
            self.ds = 
                {
                collection_name: "thecollection_list.file",
                error: "Error message if there is error",
                datasets: [{
                    "name":"example.nc",
                    "error":"message for error if error exists",
                    "variables":[
                            {
                            "path": 'NETCDF:"somevariable.nc"://group1/variable1',
                            "fullname":"//group1/variable1",
                            "name": "variable1",
                            "units":["mm"]
                            }
                        ]
                    }]
                }
        """
        pass

    def test_units_consistency(
            self, dataset_collection):
        """
            Test units consistency across datasets.
            Intermediate test_results: A list of failed test results where each test result is 
            an object:
                * Test type (group, variable, or attribute)
                * Test name
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
            _the_result = self._process_one_dataset(dataset, _the_ref_ds)
            if _the_result:
                _test_results.append(_the_result)
        _the_o = dict()
        _the_o["collection_name"]=dataset_collection["collection_name"]
        _the_o["errors"]=_test_results
        text_except_message = json.dumps(_the_o)
        assert len(_test_results) == 0, text_except_message


    def _process_one_dataset(self,dataset:dict, ref_dataset:dict)->dict:
        """
            Test units consistency across datasets.
            Intermediate test_results: A list of failed test results where each test result is 
            an dict with the following attributes:
                * dataset_name: error dataset(with variable path)
                * error: error message
        """
        #dataset = self.ds
        if "error" in dataset:
            _the_dict = dict()
            _the_dict["error"]=dataset["error"]
            _the_dict["dataset_name"]=dataset["path"]
            return _the_dict
        test_results = list()
        # test variable units
        for _r_var in ref_dataset['variables']:
            _r_v_name = _r_var['fullname']
            the_var = [k for k in dataset['variables'] if k['fullname'] == _r_v_name]
            if len(the_var) == 1:
                _u = ','.join(map(str,the_var[0]['units']))
                _r_u = ','.join(map(str,_r_var['units']))
                if _u != _r_u:
                    _the_o = dict()
                    _the_o["dataset_name"]=the_var[0]["path"]
                    _the_o["error"]=(
                        f"Inconsistent units - '[{_u}]' "
                        f"vs '[{_r_u}]'")
                    test_results.append(_the_o)
            else:
                _the_o = dict()
                _the_o["dataset_name"]=dataset["name"]
                _the_o["error"]=(
                    f"No matching or ambiguous var - '{_r_v_name}'")
                test_results.append(_the_o)

        _the_o = dict()
        _the_o["dataset_name"]=dataset["name"]
        _the_o["errors"]=test_results
        if len(test_results) == 0:
            return None
        else:
            return _the_o
