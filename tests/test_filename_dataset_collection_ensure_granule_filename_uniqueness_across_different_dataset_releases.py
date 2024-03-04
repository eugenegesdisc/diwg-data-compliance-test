"""
    Ensure Granule's Filename Uniqueness Across Different Dataset Releases

    https://wiki.earthdata.nasa.gov/display/ESDSWG/Ensure+Granule%27s+Filename+Uniqueness+Across+Different+Dataset+Releases
"""
import re
import json
import pytest

from diwg_dataset.dataname.filename_dataset_collection_ensure_granule_filename_uniqueness_across_different_dataset_releases import (
    FilenameDatasetCollectionEnsureGranuleFilenameUniqueness)

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
                        "dataset_name":"/some/path/SMAP_L4_SM_gph_20200915T193000_Vv5014_001.h5",
                        "error":"message for error if error exists",
                        "partition":
                                {
                                    "filename":"SMAP_L4_SM_gph_20200915T193000_Vv5014_001.h5",
                                    "id":"SMAP_L4_SM_gph",
                                    "crid":"Vv5014_001",
                                    "datetime": "20200915T193000",
                                    "pdt":"__.h5")
                    }
                ]
            }
    """
    #setup - class
    the_dataset_collection_filename=request.config.getoption("--dataset-name-list")
    the_dataset_identifier=request.config.getoption("--dataset-id")
    the_dataset_crid=request.config.getoption("--dataset-crid")
    the_dataset_datetime=request.config.getoption("--dataset-datetime")
    the_dataset_pdt=request.config.getoption("--dataset-pdt")
    the_dmp = FilenameDatasetCollectionEnsureGranuleFilenameUniqueness()
    the_ret_dataset = the_dmp.get_dataname_uniqueness(
        dataset_name_listfile=the_dataset_collection_filename,
        dataset_id=the_dataset_identifier,
        dataset_crid=the_dataset_crid,
        dataset_datetime=the_dataset_datetime,
        dataset_pdt=the_dataset_pdt)
    # return the_database_name
    yield the_ret_dataset
    # teardown - class
    the_ret_dataset = None
    the_dmp = None


@pytest.mark.skip_dataset_collection_noneexistence
class TestClassFilenameDatasetCollectionEnsureGranuleFilenameUniqueness:
    """
        This test class is for compliance check against the recommendation on
        Ensure Granule's Filename Uniqueness Across Different Dataset Releases

        https://wiki.earthdata.nasa.gov/display/ESDSWG/Ensure+Granule%27s+Filename+Uniqueness+Across+Different+Dataset+Releases
        (Recommendation 3.9 in ESDS-RFC-036v1.2)
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
                            "dataset_name":"/some/path/SMAP_L4_SM_gph_20200915T193000_Vv5014_001.h5",
                            "error":"message for error if error exists",
                            "partition":
                                    {
                                        "filename":"SMAP_L4_SM_gph_20200915T193000_Vv5014_001.h5",
                                        "id":"SMAP_L4_SM_gph",
                                        "crid":"Vv5014_001",
                                        "datetime": "20200915T193000",
                                        "pdt":"__.h5")
                        }
                    ]
                }
        """
        pass

    def test_ensure_granule_filename_uniqueness(
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


    def _process_one_dataset(self,dataset:dict)->dict:
        """
            Test unique filename across different releases.
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
        _the_o = dict()
        _the_o["dataset_name"]=dataset["dataset_name"]
        _the_o["error"]=("Duplicated filename: "
                            + dataset['partition']['filename'])
        test_results.append(_the_o)

        _the_o = dict()
        _the_o["dataset_name"]=dataset["dataset_name"]
        _the_o["errors"]=test_results
        if len(test_results) == 0:
            return None
        else:
            return _the_o
