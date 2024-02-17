"""
Character Set for User-Defined Group, Variable, and Attribute Names

https://wiki.earthdata.nasa.gov/display/ESDSWG/Character+Set+for+User-Defined+Group%2C+Variable%2C+and+Attribute+Names

"""
import re
import json
import pytest

from diwg_dataset.metadata.dataset_group_variable_attribute_name import (
    DatasetGroupVariableAttributeName)

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
                "group_names":["group1", "2group"],
                "variable_names":["var1", "var-2"],
                "attribute_names":["attr1", "attr_2"]
            }
    """
    #setup - class
    the_dataset_name=request.config.getoption("--dataset-name")
    the_dmp = DatasetGroupVariableAttributeName()
    the_ret_dataset = the_dmp.get_group_variable_attribute_names(the_dataset_name)
    # return the_database_name
    yield the_ret_dataset
    # teardown - class
    the_ret_dataset = None
    the_dmp = None


@pytest.mark.skip_dataset_noneexistence
class TestClassDatasetGroupVariableAttributeNameConvention:
    """
        This test class is for compliance check against the recommendation on
        character set for user-defined group, variable, and attribute names.

        Character Set for User-Defined Group, Variable, and Attribute Names
        (Recommendation 3.1 in ESDS-RFC-036v1.2)
    """
    def setup_class(self):
        """
            Setup at the class level.
        """
        self.ds = {
            "dataset_name":'test_dataset.nc',
            "group_names":["group1", "2group"],
            "variable_names":["var1", "var-2"],
            "attribute_names":["attr1", "attr_2"]
            }

    def test_user_defined_group_variable_attribute_names(
            self, dataset):
        """
            Test names in CF convention.
            Intermediate test_results: A list of failed test results where each test result is 
            a tuple of the following:
                * Test type (group, variable, or attribute)
                * Test name
        """
        #dataset = self.ds
        if "error" in dataset:
            _the_dict = dict()
            _the_dict["error"]=dataset["error"]
            _the_dict["dataset_name"]=dataset["dataset_name"]
            _the_reason = json.dumps(_the_dict)
            pytest.xfail(_the_reason)
        test_results = list()
        cf_regex = re.compile(r'^[A-Za-z][A-Za-z0-9_]*$')
        # test group names
        _the_group=list()
        for name in dataset["group_names"]:
            if cf_regex.match(name) is None:
                _the_group.append(name)
        if len(_the_group)>0:
            _the_o = dict()
            _the_o["type"]="group"
            _the_o["invalid_values"]=_the_group
            test_results.append(_the_o)
        # test variable names
        _the_variable=list()
        for name in dataset["variable_names"]:
            if cf_regex.match(name) is None:
                _the_variable.append(name)
        if len(_the_variable)>0:
            _the_o = dict()
            _the_o["type"]="variable"
            _the_o["invalid_values"]=_the_variable
            test_results.append(_the_o)
        # test attribute names
        _the_attribute=list()
        for name in dataset["attribute_names"]:
            if cf_regex.match(name) is None:
                _the_attribute.append(name)
        if len(_the_attribute)>0:
            _the_o = dict()
            _the_o["type"]="attribute"
            _the_o["invalid_values"]=_the_attribute
            test_results.append(_the_o)
        _the_o = dict()
        _the_o["dataset_name"]=dataset["dataset_name"]
        _the_o["errors"]=test_results
        test_except_message = json.dumps(_the_o)
        assert len(test_results) == 0, test_except_message
