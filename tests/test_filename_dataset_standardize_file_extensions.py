"""
    For recommendation:

    Standardize File Extensions for HDF5/netCDF Files

    verify if the dataset (granule) filename has proper extension.

"""
import json
import pytest

from diwg_dataset.dataname.filename_dataset_standardize_file_extensions import (
    FilenameDatasetStandardizeFileExtensions)

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
                "extension":
                        {
                            "driver_short_name":"netCDF",
                            "HDFEOSVersion":"",
                            "extension":"nc",
                            "valid": True
                        }
            }
    """
    #setup - class
    the_dataset_name=request.config.getoption("--dataset-name")
    the_dmp = FilenameDatasetStandardizeFileExtensions()
    the_ret_dataset = the_dmp.get_dataname_extension(the_dataset_name)
    # return the_database_name
    yield the_ret_dataset
    # teardown - class
    the_ret_dataset = None
    the_dmp = None


@pytest.mark.skip_dataset_noneexistence
class TestClassFilenameDatasetStandardizeFileExtensions:
    """
        This test class is for compliance check against the recommendation on

        Standardize File Extensions for HDF5/netCDF Files

        https://wiki.earthdata.nasa.gov/pages/viewpage.action?pageId=182297715
        (Recommendation 3.8 in ESDS-RFC-036v1.2)
    """
    def setup_class(self):
        """
            Setup at the class level.
        self.ds = 
            {
                "dataset_name":"example.nc",
                "error":"message for error if error exists",
                "extension":
                        {
                            "driver_short_name":"netCDF",
                            "HDFEOSVersion":"",
                            "expected":".nc",
                            "extension":".nc",
                            "valid": True
                        }
            }
        """
        pass

    def test_standardize_file_extensions(
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
            _the_dict["dataset_name"]=dataset["dataset_name"]
            _the_reason = json.dumps(_the_dict)
            pytest.xfail(_the_reason)
        test_results = list()
        if ('extension' not in dataset or
            'valid' not in dataset['extension']):
            # skip - not applicable, most likely not in netcdf/hdfeos5/hdf5.
            _the_reason = ("Not in HDF5/NetCDF/HDFEOS5: " + 
                           "filename=" + dataset["dataset_name"])
            pytest.skip(_the_reason)
        if not dataset['extension']['valid']:
            _the_o = dict()
            _the_o["dataset_name"]=dataset["dataset_name"]
            _the_o["error"]=("Not valid extension: expect "
                             + dataset['extension']['expected']
                             + " Get: " + dataset['extension']['extension'])
            test_results.append(_the_o)
        _the_o = dict()
        _the_o["dataset_name"]=dataset["dataset_name"]
        _the_o["errors"]=test_results
        test_except_message = json.dumps(_the_o)
        assert len(test_results) == 0, test_except_message
