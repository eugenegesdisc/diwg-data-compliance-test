"""
    For recommendation:

    Date-Time Information in Granule Filenames

    Verify that all date/time fields in filename are in proper order and format.
"""
import json
import pytest

from diwg_dataset.dataname.filename_dataset_date_time_information_in_granule_filenames import (
    FilenameDatasetDateTimeInformationInGranuleFilenames)

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
                "dataset_name":"/some/path/DeepBlue-SeaWiFS_L2_20101210T135954Z_v004-20130525T172725Z.h5",
                "error":"message for error if error exists",
                "filename": "DeepBlue-SeaWiFS_L2_20101210T135954Z_v004-20130525T172725Z.h5",
                "temporal_extent":[
                    {
                        "field_name":"temporal_begin",
                        "token":"20101210T135954Z"
                        "start":20,
                        "end": 36,
                        "iso": True
                    }]
                "date_time_fields":[
                    {
                        "field_name":"pdt",
                        "token":"20130525T172725Z",
                        "start": 42,
                        "end": 58,
                        "iso": True
                    }
                ],
                "valid":{
                    "skip": False,
                    "iso": True,
                    "temporal_order": True,
                    "fields_order": True,
                    "same_isoformat": True,
                    "overall": True
                }
            }
    """
    #setup - class
    the_dataset_name=request.config.getoption("--dataset-name")
    the_dataset_datetime=request.config.getoption("--dataset-datetime")
    the_dataset_datetime_group=request.config.getoption("--dataset-datetime-group")
    the_dataset_pdt=request.config.getoption("--dataset-pdt")
    the_dataset_pdt_group=request.config.getoption("--dataset-pdt-group")
    the_dataset_datetime_fields=request.config.getoption("--dataset-datetime-fields")
    the_dataset_datetime_fields_groups=request.config.getoption("--dataset-datetime-fields-groups")
    the_dmp = FilenameDatasetDateTimeInformationInGranuleFilenames()
    the_ret_dataset = the_dmp.validate_dataname_date_time_information(
        dataset_name=the_dataset_name,
        dataset_datetime=the_dataset_datetime,
        dataset_datetime_group=the_dataset_datetime_group,
        dataset_pdt=the_dataset_pdt,
        dataset_pdt_group=the_dataset_pdt_group,
        dataset_datetime_fields=the_dataset_datetime_fields,
        dataset_datetime_fields_groups=the_dataset_datetime_fields_groups)
    # return the_database_name
    yield the_ret_dataset
    # teardown - class
    the_ret_dataset = None
    the_dmp = None


@pytest.mark.skip_dataset_noneexistence
class TestClassFilenameDatasetDateTimeInformationInGranuleFilenames:
    """
        This test class is for compliance check against the recommendation on

        Date-Time Information in Granule Filenames

        https://wiki.earthdata.nasa.gov/display/ESDSWG/Date-Time+Information+in+Granule+Filenames
        (Recommendation 3.11 in ESDS-RFC-036v1.2)
    """
    def setup_class(self):
        """
            Setup at the class level.
        self.ds = 
            {
                "dataset_name":"/some/path/DeepBlue-SeaWiFS_L2_20101210T135954Z_v004-20130525T172725Z.h5",
                "error":"message for error if error exists",
                "filename": "DeepBlue-SeaWiFS_L2_20101210T135954Z_v004-20130525T172725Z.h5",
                "temporal_extent":[
                    {
                        "field_name":"temporal_begin",
                        "token":"20101210T135954Z"
                        "start":20,
                        "end": 36,
                        "iso": True
                    }]
                "date_time_fields":[
                    {
                        "field_name":"pdt",
                        "token":"20130525T172725Z",
                        "start": 42,
                        "end": 58,
                        "iso": True
                    }
                ],
                "valid":{
                    "skip": False,
                    "iso": True,
                    "temporal_order": True,
                    "fields_order": True,
                    "same_isoformat": True,
                    "overall": True
                }
            }
        """
        pass

    def test_date_time_information_in_granule_filenames(
            self, dataset):
        """
            Test datetime fields in filename.
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

        if dataset['valid']['skip']:
            # skip - not applicable, most likely incomplete parameters for extracting components.
            _the_reason = ("Skipped: incomplete parameters. " + 
                           " Filename=" + dataset["filename"])
            pytest.skip(_the_reason)

        if not dataset['valid']['overall']:
            _the_o = dict()
            _the_o["dataset_name"]=dataset["dataset_name"]
            _msg = ""
            _v = dataset['valid']
            if ("iso" in _v and not _v["iso"]):
                _msg += "Not in correct ISO8601 format. "
            if ("temporal_order" in _v and not _v["temporal_order"]):
                _msg += "Temporal interval in wrong order. "
            if ("fields_order" in _v and not _v["fields_order"]):
                _msg += "Temporal extent are not before all other date/time fields. "
            if ("same_isoformat" in _v and not _v["same_isoformat"]):
                _msg += "Not all datetime fields in the same ISO8601 format. "
            _the_o["error"]=("Datetime info incompliance: "
                             + _msg)
            test_results.append(_the_o)
        _the_o = dict()
        _the_o["dataset_name"]=dataset["dataset_name"]
        _the_o["errors"]=test_results
        test_except_message = json.dumps(_the_o)
        assert len(test_results) == 0, test_except_message
