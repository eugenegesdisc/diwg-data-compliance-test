"""
Distinguish clearly between HDF and netCDF packing conventions
(Recommendation 2.5 in ESDS-RFC-028v1.3)

https://wiki.earthdata.nasa.gov/display/ESDSWG/Distinguish+clearly+between+HDF+and+netCDF+packing+conventions
"""
import json
import pytest
from diwg_dataset.metadata.dataset_collection_data_packing import (
    DatasetCollectionMetaPacking)
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
                "dataset_name": "test_dataset.nc",
                "error": "add error here if there is a general error",
                "sudbdatasets":[{
                    "name":"test_dataset.nc",
                    "error":"message for error if error exists",
                    "is_scaled": True,
                    "scaling":{
                        "scale_factor": 0.1,
                        "add_offset": 1000.0
                    }
                    "packing":{
                        "packing_convention":"netCDF",
                        "packing_convention_description": 
                            "unpacked = scale_factor x packed + add_offset"
                    }
                }]
            }]
    """
    #setup - class
    the_dataset_name=request.config.getoption("--dataset-name-list")
    the_dmp = DatasetCollectionMetaPacking()
    the_ret_dataset = the_dmp.get_packing_metadata(the_dataset_name)
    # return the_database_name
    yield the_ret_dataset
    # teardown - class
    the_ret_dataset = None
    the_dmp = None


@pytest.mark.skip_dataset_collection_noneexistence
class TestClassDatasetCollectionDataPacking(object):
    """
        This test class is for compliance check against the recommendation on packing.

        Distinguish clearly between HDF and netCDF packing conventions 
        (Recommendation 2.5 in ESDS-RFC-028v1.3)
    """
    def setup_class(self):
        """
            Setup at the class level.
        # example test dataset
        self.ds = 
            {
            collection_name: "thecollection_list.file",
            error: "Error message if there is error",
            datasets: [{
                "dataset_name": "test_dataset.nc",
                "error": "add error here if there is a general error",
                "sudbdatasets":[{
                    "name":"test_dataset.nc",
                    "error":"message for error if error exists",
                    "is_scaled": True,
                    "scaling":{
                        "scale_factor": 0.1,
                        "add_offset": 1000.0
                    }
                    "packing":{
                        "packing_convention":"netCDF",
                        "packing_convention_description": 
                            "unpacked = scale_factor x packed + add_offset"
                    }
                }]
            }]
       """
        pass

    def test_dataset_has_packing_convention_attribute(self, dataset_collection):
        """
            Test that the dataest has a "packing_convention" attribute.
        """
        if "error" in dataset_collection:
            _the_o = dict()
            _the_o["collection_name"]=dataset_collection['collection_name']
            _the_o["error"]=dataset_collection['error']
            _the_reason = json.dumps(_the_o)
            pytest.xfail(_the_reason)
        _test_results = list()
        for dataset in dataset_collection["datasets"]:
            _the_result = self._process_one_dataset_has_packing_convention_attribute(dataset)
            if _the_result:
                _test_results.append(_the_result)
        _the_o = dict()
        _the_o["collection_name"]=dataset_collection["collection_name"]
        _the_o["errors"]=_test_results
        text_except_message = json.dumps(_the_o)
        assert len(_test_results) == 0, text_except_message

    def _process_one_dataset_has_packing_convention_attribute(self, dataset:dict)->dict:
        """
            Test that the dataest has a "packing_convention" attribute.
        """
        if "error" in dataset:
            _the_o = dict()
            _the_o["dataset_name"]=dataset['dataset_name']
            _the_o["error"]=dataset['error']
            return _the_o

        test_results = list()

        for subdataset in dataset['subdatasets']:
            if "error" in subdataset:
                _the_o = dict()
                _the_o['subdataset_name']=subdataset["name"]
                _the_o['error']=subdataset['error']
                test_results.append(_the_o)
                continue
            if not subdataset["is_scaled"]:
                continue
            if "packing_convention" not in subdataset["packing"]:
                _the_o = dict()
                _the_o['subdataset_name']=subdataset["name"]
                _the_o['error']="Missing packing_convention attribute"
                test_results.append(_the_o)
        _the_o = dict()
        _the_o["dataset_name"]=dataset["dataset_name"]
        _the_o["errors"]=test_results
        if len(test_results) == 0:
            return None
        else:
            return _the_o


    def test_dataset_packing_convention_is_valid(self, dataset_collection):
        """
            Test that the dataest's "packing_convention" attribute is a
            valid value.
        """
        if "error" in dataset_collection:
            _the_o = dict()
            _the_o["collection_name"]=dataset_collection['collection_name']
            _the_o["error"]=dataset_collection['error']
            _the_reason = json.dumps(_the_o)
            pytest.xfail(_the_reason)
        _test_results = list()
        for dataset in dataset_collection["datasets"]:
            _the_result = self._process_one_dataset_packing_convention_is_valid(dataset)
            if _the_result:
                _test_results.append(_the_result)
        _the_o = dict()
        _the_o["collection_name"]=dataset_collection["collection_name"]
        _the_o["errors"]=_test_results
        text_except_message = json.dumps(_the_o)
        assert len(_test_results) == 0, text_except_message

    def _process_one_dataset_packing_convention_is_valid(self, dataset)->dict:
        """
            Test that the dataest's "packing_convention" attribute is a
            valid value.
        """
        if "error" in dataset:
            _the_o = dict()
            _the_o["dataset_name"]=dataset['dataset_name']
            _the_o["error"]=dataset['error']
            return _the_o

        test_results = list()

        for subdataset in dataset['subdatasets']:
            if "error" in subdataset:
                _the_o = dict()
                _the_o['subdataset_name']=subdataset["name"]
                _the_o['error']=subdataset['error']
                test_results.append(_the_o)
                continue
            if not subdataset["is_scaled"]:
                continue
            _the_ds_pc_value = subdataset["packing"]["packing_convention"]
            if _the_ds_pc_value not in [
                "netCDF", "non-netCDF"]:
                _the_o = dict()
                _the_o['subdataset_name']=subdataset["name"]
                _the_o['error']=f"Invalid value for packing_convension - '{_the_ds_pc_value}'"
                test_results.append(_the_o)
                continue
        _the_o = dict()
        _the_o["dataset_name"]=dataset["dataset_name"]
        _the_o["errors"]=test_results
        if len(test_results) == 0:
            return None
        else:
            return _the_o

    def test_dataset_has_packing_convention_description_attribute(self, dataset_collection):
        """
            Test that the dataest has a "packing_convention_description" attribute.
        """
        if "error" in dataset_collection:
            _the_o = dict()
            _the_o["collection_name"]=dataset_collection['collection_name']
            _the_o["error"]=dataset_collection['error']
            _the_reason = json.dumps(_the_o)
            pytest.xfail(_the_reason)
        _test_results = list()
        for dataset in dataset_collection["datasets"]:
            _the_result = self._process_one_dataset_has_packing_convention_description_attribute(
                dataset)
            if _the_result:
                _test_results.append(_the_result)
        _the_o = dict()
        _the_o["collection_name"]=dataset_collection["collection_name"]
        _the_o["errors"]=_test_results
        text_except_message = json.dumps(_the_o)
        assert len(_test_results) == 0, text_except_message

    def _process_one_dataset_has_packing_convention_description_attribute(self, dataset)->dict:
        """
            Test that the dataest has a "packing_convention_description" attribute.
        """
        if "error" in dataset:
            _the_o = dict()
            _the_o["dataset_name"]=dataset['dataset_name']
            _the_o["error"]=dataset['error']
            return _the_o

        test_results = list()

        for subdataset in dataset['subdatasets']:
            if "error" in subdataset:
                _the_o = dict()
                _the_o['subdataset_name']=subdataset["name"]
                _the_o['error']=subdataset['error']
                test_results.append(_the_o)
                continue
            if not subdataset["is_scaled"]:
                continue
            if "packing_convention_description" not in subdataset["packing"]:
                _the_o = dict()
                _the_o['subdataset_name']=subdataset["name"]
                _the_o['error']="Missing packing_convention_description attribute"
                test_results.append(_the_o)
        _the_o = dict()
        _the_o["dataset_name"]=dataset["dataset_name"]
        _the_o["errors"]=test_results
        if len(test_results) == 0:
            return None
        else:
            return _the_o

    def test_dataset_packing_convention_description_is_valid(self, dataset_collection):
        """
            Test that the dataest's "packing_convention_description" attribute is a
            valid value.
        """
        if "error" in dataset_collection:
            _the_o = dict()
            _the_o["collection_name"]=dataset_collection['collection_name']
            _the_o["error"]=dataset_collection['error']
            _the_reason = json.dumps(_the_o)
            pytest.xfail(_the_reason)
        _test_results = list()
        for dataset in dataset_collection["datasets"]:
            _the_result = self._process_one_dataset_packing_convention_description_is_valid(
                dataset)
            if _the_result:
                _test_results.append(_the_result)
        _the_o = dict()
        _the_o["collection_name"]=dataset_collection["collection_name"]
        _the_o["errors"]=_test_results
        text_except_message = json.dumps(_the_o)
        assert len(_test_results) == 0, text_except_message

    def _process_one_dataset_packing_convention_description_is_valid(self, dataset)->dict:
        """
            Test that the dataest's "packing_convention_description" attribute is a
            valid value.
        """
        if "error" in dataset:
            _the_o = dict()
            _the_o["dataset_name"]=dataset['dataset_name']
            _the_o["error"]=dataset['error']
            return(_the_o)

        test_results = list()

        for subdataset in dataset['subdatasets']:
            if "error" in subdataset:
                _the_o = dict()
                _the_o['subdataset_name']=subdataset["name"]
                _the_o['error']=subdataset['error']
                test_results.append(_the_o)
                continue
            if not subdataset["is_scaled"]:
                continue
            _the_ds_pcd_value = subdataset["packing"]["packing_convention_description"]
            if _the_ds_pcd_value not in [
                "unpacked = scale_factor x packed + add_offset",
                "unpacked = scale_factor x (packed - add_offset)"]:
                _the_o = dict()
                _the_o['subdataset_name']=subdataset["name"]
                _the_o['error']=("Invalid value for packing_convention_description -"
                                 f" '{_the_ds_pcd_value}'")
                test_results.append(_the_o)
        _the_o = dict()
        _the_o["dataset_name"]=dataset["dataset_name"]
        _the_o["errors"]=test_results
        if len(test_results) == 0:
            return None
        else:
            return _the_o

    def test_dataset_packing_convention_is_consistent_with_packing_convention_description(
            self, dataset_collection):
        """
            Test that the dataest's "packing_convention" attribute is 
            consistent with its "packing_convention_description" attribute.
        """
        if "error" in dataset_collection:
            _the_o = dict()
            _the_o["collection_name"]=dataset_collection['collection_name']
            _the_o["error"]=dataset_collection['error']
            _the_reason = json.dumps(_the_o)
            pytest.xfail(_the_reason)
        _test_results = list()
        for dataset in dataset_collection["datasets"]:
            _the_result = self._process_one_dataset_packing_convention_is_consistent_with_packing_convention_description(
                dataset)
            if _the_result:
                _test_results.append(_the_result)
        _the_o = dict()
        _the_o["collection_name"]=dataset_collection["collection_name"]
        _the_o["errors"]=_test_results
        text_except_message = json.dumps(_the_o)
        assert len(_test_results) == 0, text_except_message

    def _process_one_dataset_packing_convention_is_consistent_with_packing_convention_description(
            self, dataset)->dict:
        """
            Test that the dataest's "packing_convention" attribute is 
            consistent with its "packing_convention_description" attribute.
        """
        if "error" in dataset:
            _the_o = dict()
            _the_o["dataset_name"]=dataset['dataset_name']
            _the_o["error"]=dataset['error']
            return(_the_o)

        test_results = list()

        for subdataset in dataset['subdatasets']:
            if "error" in subdataset:
                _the_o = dict()
                _the_o['subdataset_name']=subdataset["name"]
                _the_o['error']=subdataset['error']
                test_results.append(_the_o)
                continue
            if not subdataset["is_scaled"]:
                continue
            _the_ds_name = subdataset["name"]
            _the_ds_pc_value = subdataset["packing"]["packing_convention"]
            _the_ds_pcd_value = subdataset["packing"]["packing_convention_description"]
            if _the_ds_pc_value == "netCDF":
                _valid_description = "unpacked = scale_factor x packed + add_offset"
                if _the_ds_pcd_value != _valid_description:
                    _the_o = dict()
                    _the_o['subdataset_name']=subdataset["name"]
                    _the_o['error']=(f"Inconsistent description '{_the_ds_pcd_value}' for "
                                     f"packing_convention '{_the_ds_pc_value}' "
                                     f"- Expect '{_valid_description}' "
                                     "for packing convention 'netCDF' ")
                    test_results.append(_the_o)
            elif _the_ds_pc_value == "non-netCDF":
                _valid_description = "unpacked = scale_factor x (packed - add_offset)"
                if _the_ds_pcd_value != _valid_description:
                    _the_o = dict()
                    _the_o['subdataset_name']=subdataset["name"]
                    _the_o['error']=(f"Inconsistent description '{_the_ds_pcd_value}' for "
                                     f"packing_convention '{_the_ds_pc_value}' "
                                     f"- Expect '{_valid_description}' "
                                     "for packing convention 'non-netCDF' ")
                    test_results.append(_the_o)
        _the_o = dict()
        _the_o["dataset_name"]=dataset["dataset_name"]
        _the_o["errors"]=test_results
        if len(test_results) == 0:
            return None
        else:
            return _the_o

    def teardown_class(self):
        """Teardown at the class level"""
        #print("teardown class")
        pass
