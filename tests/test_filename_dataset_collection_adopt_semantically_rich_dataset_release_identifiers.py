"""
    Adopt Semantically Rich Dataset Release Identifiers

    Partition filename and verify if all parts (major, minor, and patch) of crid exist.
"""
import re
import json
import pytest

from diwg_dataset.dataname.filename_dataset_collection_adopt_semantically_rich_dataset_release_identifiers import (
    FilenameDatasetCollectionAdoptSemanticallyRichDatasetReleaseIdentifiers)

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
                                "major": "v5014",
                                "minor":"001",
                                "patch":"")
                            }
                        "valid":
                            {
                                "skip": False,
                                "status": False,
                                "message": "Missing: patch"                        
                            }
                    }
                ],
                "valid": {
                    "skip": False
                }
            }
    """
    #setup - class
    the_dataset_collection_filename=request.config.getoption("--dataset-name-list")
    the_dataset_crid=request.config.getoption("--dataset-crid")
    the_dataset_crid_major=request.config.getoption("--dataset-crid-major")
    the_dataset_crid_major_group=request.config.getoption("--dataset-crid-major-group")
    the_dataset_crid_minor=request.config.getoption("--dataset-crid-minor")
    the_dataset_crid_minor_group=request.config.getoption("--dataset-crid-minor-group")
    the_dataset_crid_patch=request.config.getoption("--dataset-crid-patch")
    the_dataset_crid_patch_group=request.config.getoption("--dataset-crid-patch-group")
    the_dmp = FilenameDatasetCollectionAdoptSemanticallyRichDatasetReleaseIdentifiers()
    the_ret_dataset = the_dmp.validate_dataname_crid_partitions(
        dataset_name_listfile=the_dataset_collection_filename,
        dataset_crid=the_dataset_crid,
        dataset_crid_major=the_dataset_crid_major,
        dataset_crid_major_group=the_dataset_crid_major_group,
        dataset_crid_minor=the_dataset_crid_minor,
        dataset_crid_minor_group=the_dataset_crid_minor_group,
        dataset_crid_patch=the_dataset_crid_patch,
        dataset_crid_patch_group=the_dataset_crid_patch_group)
    # return the_database_name
    yield the_ret_dataset
    # teardown - class
    the_ret_dataset = None
    the_dmp = None


@pytest.mark.skip_dataset_collection_noneexistence
class TestClassFilenameDatasetCollectionAdoptSemanticallyRichDatasetReleaseIdentifiers:
    """
        This test class is for compliance check against the recommendation on
        Adopt Semantically Rich Dataset Release Identifiers

        https://wiki.earthdata.nasa.gov/display/ESDSWG/Adopt+Semantically+Rich+Dataset+Release+Identifiers
        (Recommendation 3.10 in ESDS-RFC-036v1.2)
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
                                "major": "v5014",
                                "minor":"001",
                                "patch":"")
                            }
                        "valid":
                            {
                                "skip": False,
                                "status": False,
                                "message": "Missing: patch"                        
                            }
                    }
                ],
                "valid": {
                    "skip": False
                }
            }
        """
        pass

    def test_semantically_rich_dataset_release_identifiers(
            self, dataset_collection):
        """
            Test completeness of crid (major, minor, and patch) in filename.
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
        if dataset_collection['valid']['skip']:
            # skip - not applicable, most likely not in netcdf/hdfeos5/hdf5.
            _the_reason = ("All files are skipped: " + 
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


    def _process_one_dataset(self,dataset:dict)->dict:
        """
            Test completeness of crid (major, minor, and patch) in filename.
            Intermediate test_results: A list of failed test results where each test result is 
            an dict with the following attributes:
                * dataset_name: error dataset(with variable path)
                * error: error message
        """
        #dataset = self.ds
        if "error" in dataset:
            _the_dict = dict()
            _the_dict["error"]=dataset["error"]
            _the_dict["dataset_name"]=dataset["dataset_name"]
            return _the_dict
        test_results = list()
        _msg = ""
        if 'message' in dataset['valid']:
            _msg = dataset['valid']['message']

        if dataset['valid']['skip']:
            _the_o = dict()
            _the_o["dataset_name"]=dataset["dataset_name"]
            # skip - not applicable, most likely incomplete parameters for extracting components.
            _the_reason = ("Skipped: incomplete parameters. " + _msg +
                           " Filename=" + dataset["dataset_name"])
            _the_o["error"]=_the_reason
            return _the_o

        if not dataset['valid']['status']:
            _the_o = dict()
            _the_o["dataset_name"]=dataset["dataset_name"]
            _the_o["error"]=("No semantically rich data release identifiers in filename: "
                             + _msg)
            test_results.append(_the_o)

        _the_o = dict()
        _the_o["dataset_name"]=dataset["dataset_name"]
        _the_o["errors"]=test_results
        if len(test_results) == 0:
            return None
        else:
            return _the_o
