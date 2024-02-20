"""
Use the Units Attribute Only for Variables with Physical Units

https://wiki.earthdata.nasa.gov/pages/viewpage.action?pageId=182296347

"""
import re
import json
import pytest
import cfunits

from diwg_dataset.metadata.dataset_variable_physical_units import (
    DatasetVariablePhysicalUnits)

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
            "dataset_name":"example.nc",
            "error":"message for error if error exists",
            "variables":[
                    {
                    "path": 'NETCDF:"somevariable.nc"://group1/variable1',
                    "fullname":"//group1/variable1",
                    "name": "variable1",
                    "units":"mm"
                    }
                ]
            }
    """
    #setup - class
    the_dataset_name=request.config.getoption("--dataset-name")
    the_dmp = DatasetVariablePhysicalUnits()
    the_ret_dataset = the_dmp.get_variable_units(the_dataset_name)
    # return the_database_name
    yield the_ret_dataset
    # teardown - class
    the_ret_dataset = None
    the_dmp = None


@pytest.mark.skip_dataset_noneexistence
class TestClassDatasetVariableUnits:
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
            "dataset_name":"example.nc",
            "error":"message for error if error exists",
            "variables":[
                    {
                    "path": 'NETCDF:"somevariable.nc"://group1/variable1',
                    "fullname":"//group1/variable1",
                    "name": "variable1",
                    "units":["mm"]
                    }
                ]
            }
        """
        pass

    def test_variable_units(
            self, dataset):
        """
            Test units of variables in a dataset following CF convention.
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
        test_results = list()
        for _the_var in dataset['variables']:
            self._check_variable_units_1(
                test_results,_the_var)
            self._check_variable_units_2(
                test_results,_the_var)
        _the_o = dict()
        _the_o["dataset_name"]=dataset["dataset_name"]
        _the_o["errors"]=test_results
        test_except_message = json.dumps(_the_o)
        assert len(test_results) == 0, test_except_message

    def _check_variable_units_1(
            self, test_results:list,
            variable:dict):
        """
            Test: Unitless (dimensionless in the physical sense) 
                property of the data in a variable is indicated 
                by the lack of a units attribute, unless:
                    - appropriate physical units do exist;
                    - use of dimensionless units identifiers is common
                      practice in the target user community.
            The use of units="1", units="" (empty string), or any similar
            construct as generic units for unitless data are strongly discouraged.
        """
        for unit in variable['units']:
            if unit == "1":
                _the_o = dict()
                _the_o["variable_name"]=variable["fullname"]
                _the_o["error"]=("Units attribute set to '1', "
                                 "which is not allopwedc for unitless data.")
                test_results.append(_the_o)
            if unit == "":
                _the_o = dict()
                _the_o["variable_name"]=variable["fullname"]
                _the_o["error"]=("Units attribute set to '1', "
                                 "which is not allopwedc for unitless data.")
                test_results.append(_the_o)

    def _check_variable_units_2(
            self,test_results:list,variable:dict):
        """
        Values of the units attribute should be supported by the UDUNITS-2 library.
        """
        for sunit in variable['units']:
            _tu = cfunits.Units(sunit)
            if not _tu.isvalid:
                _the_o = dict()
                _the_o["variable_name"]=variable["fullname"]
                _the_o["error"]=("Units attribute value is not supported by "
                                 "the UDUNITS-2 library - "
                                 f"'{sunit}'")
                test_results.append(_the_o)
