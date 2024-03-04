"""
    For recommendation:

    Adopt Semantically Rich Dataset Release Identifiers

    Partition filename and verify if all parts (major, minor, and patch) of crid exist.

"""
import json
import pytest

from diwg_dataset.dataname.filename_dataset_adopt_semantically_rich_dataset_release_identifiers import (
    FilenameDatasetAdoptSemanticallyRichDatasetReleaseIdentifiers)

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
                        },
                "valid":
                    {
                        "skip": False,
                        "status": False,
                        "message": "Missing: patch"                        
                    }
            }
    """
    #setup - class
    the_dataset_name=request.config.getoption("--dataset-name")
    the_dataset_crid=request.config.getoption("--dataset-crid")
    the_dataset_crid_major=request.config.getoption("--dataset-crid-major")
    the_dataset_crid_major_group=request.config.getoption("--dataset-crid-major-group")
    the_dataset_crid_minor=request.config.getoption("--dataset-crid-minor")
    the_dataset_crid_minor_group=request.config.getoption("--dataset-crid-minor-group")
    the_dataset_crid_patch=request.config.getoption("--dataset-crid-patch")
    the_dataset_crid_patch_group=request.config.getoption("--dataset-crid-patch-group")
    the_dmp = FilenameDatasetAdoptSemanticallyRichDatasetReleaseIdentifiers()
    the_ret_dataset = the_dmp.valid_dataname_crid_partitions(
        dataset_name=the_dataset_name,
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


@pytest.mark.skip_dataset_noneexistence
class TestClassFilenameDatasetAdoptSemanticallyRichDatasetReleaseIdentifiers:
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
                        },
                "valid":
                    {
                        "skip": False,
                        "status": False,
                        "message": "Missing: patch"                        
                    }
            }
        """
        pass

    def test_semantically_rich_dataset_release_identifiers(
            self, dataset):
        """
            Test completeness of crid (major, minor, and patch) in filename.
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
        _msg = ""
        if 'message' in dataset['valid']:
            _msg = dataset['valid']['message']

        if dataset['valid']['skip']:
            # skip - not applicable, most likely incomplete parameters for extracting components.
            _the_reason = ("Skipped: incomplete parameters. " + _msg +
                           " Filename=" + dataset["dataset_name"])
            pytest.skip(_the_reason)

        if not dataset['valid']['status']:
            _the_o = dict()
            _the_o["dataset_name"]=dataset["dataset_name"]
            _the_o["error"]=("No semantically rich data release identifiers in filename: "
                             + _msg)
            test_results.append(_the_o)
        _the_o = dict()
        _the_o["dataset_name"]=dataset["dataset_name"]
        _the_o["errors"]=test_results
        test_except_message = json.dumps(_the_o)
        assert len(test_results) == 0, test_except_message
