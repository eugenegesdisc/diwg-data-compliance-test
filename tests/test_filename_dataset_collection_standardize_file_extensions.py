"""
    For recommendation:

    Standardize File Extensions for HDF5/netCDF Files

    verify if the dataset (granule) filename in a collection has proper extension.

"""
import re
import json
import pytest
import cfunits

from diwg_dataset.dataname.filename_dataset_collection_standardize_file_extensions import (
    FilenameDatasetCollectionStandardizeFileExtensions)

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
                        "dataset_name":"example.HDF5",
                        "error":"message for error if error exists",
                        "extension":
                                {
                                    "driver_short_name":"HDF5",
                                    "HDFEOSVersion":"",
                                    "expected":".h5",
                                    "extension":".nc",
                                    "valid": False}
                    },
                ],
                "valid": {
                    "skip": False
                }
            }
    """
    #setup - class
    the_dataset_collection_filename=request.config.getoption("--dataset-name-list")
    the_dmp = FilenameDatasetCollectionStandardizeFileExtensions()
    the_ret_dataset = the_dmp.validate_dataname_extension(the_dataset_collection_filename)
    # return the_database_name
    yield the_ret_dataset
    # teardown - class
    the_ret_dataset = None
    the_dmp = None


@pytest.mark.skip_dataset_collection_noneexistence
class TestClassFilenameDatasetCollectionStandardizeFileExtensions:
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
            collection_name: "thecollection_list.file",
            error: "Error message if there is error",
            datasets: [
                    {
                        "dataset_name":"example.HDF5",
                        "error":"message for error if error exists",
                        "extension":
                                {
                                    "driver_short_name":"HDF5",
                                    "HDFEOSVersion":"",
                                    "expected":".h5",
                                    "extension":".nc",
                                    "valid": False}
                    },
                ],
                "valid": {
                    "skip": False
                }
            }
        """
        pass

    def test_standardize_file_extensions(
            self, dataset_collection):
        """
            Test if file extensions match its format version for HDF5/HDFEOS5/NetCDF.
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
        if dataset_collection['valid']['skip']:
            # skip - not applicable, most likely not in netcdf/hdfeos5/hdf5.
            _the_reason = ("All files are not in HDF5/NetCDF/HDFEOS5: " + 
                           "collection file=" + dataset_collection["collection_name"])
            pytest.skip(_the_reason)
        _test_results = list()
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
            Work on a datatset.
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
            return _the_dict
        test_results = list()
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
        if len(test_results) == 0:
            return None
        else:
            return _the_o
