"""
    pytest session configuration.
"""
import pytest

def pytest_addoption(parser):
    """
        Add CLI options.
    """
    parser.addoption("--dataset-name",
                     dest="dataset_name",
                     action="store", default=None,
                     help="dataset name. Accept GDAL dataset name.")
    parser.addoption("--dataset-name-list",
                     dest="dataset_name_list",
                     action="store", default=None,
                     help="filename for dataset list. In the list file, each line "
                     "can be a single sub-dataset (in GDAL nomination), a dataset file, "
                     "or files with wildcards (e.g. /some/path/files*.nc)")
    parser.addoption("--dataset-is-swath",
                     dest="dataset_is_swath",
                     action="store_true",
                     help="dataset or all dataset in the collection are swath. ")
    parser.addoption("--dataset-is-grid",
                     dest="dataset_is_grid",
                     action="store_true",
                     help="dataset or all dataset in the collection are regular grid. ")    

    parser.addoption("--dataset-id",
                     dest="dataset_id",
                     action="store", default=None,
                     help="Regex to extract unique dataset identifier from granule filename.")
    parser.addoption("--dataset-crid",
                     dest="dataset_crid",
                     action="store", default=None,
                     help="Regex to extract Compound Release ID (CRID) from filename. ")
    parser.addoption("--dataset-datetime",
                     dest="dataset_datetime",
                     action="store", default=None,
                     help="Regex to extract temporal extent information from filename. ")
    parser.addoption("--dataset-pdt",
                     dest="dataset_pdt",
                     action="store", default=None,
                     help="Regex to extract Production Date Time (PDT) from filename. ")
    parser.addoption("--dataset-crid-major",
                     dest="dataset_crid_major",
                     action="store", default=None,
                     help="Regex to extrac major version from Compound Release ID (CRID) token. ")
    parser.addoption("--dataset-crid-major-group",
                     dest="dataset_crid_major_group",
                     action="store", default="major",
                     help="Group name in major regex for extracting major version. ")
    parser.addoption("--dataset-crid-minor",
                     dest="dataset_crid_minor",
                     action="store", default=None,
                     help="Regex to extract minor versionn from Compound Release ID (CRID) token. ")
    parser.addoption("--dataset-crid-minor-group",
                     dest="dataset_crid_minor_group",
                     action="store", default="minor",
                     help="Group name in minor regex for extracting minor version. ")
    parser.addoption("--dataset-crid-patch",
                     dest="dataset_crid_patch",
                     action="store", default=None,
                     help="Regex to extract patch number from Compound Release ID (CRID) token. ")
    parser.addoption("--dataset-crid-patch-group",
                     dest="dataset_crid_patch_group",
                     action="store", default="patch",
                     help="Group name in patch regex for extracting patch number. ")

    parser.addoption("--dataset-datetime-group",
                     dest="dataset_datetime_group",
                     action="store", default=None,
                     help="Group name in datetime regex for extracting datetime. ")
    parser.addoption("--dataset-pdt-group",
                     dest="dataset_pdt_group",
                     action="store", default=None,
                     help="Group name in pdt regex for extracting pdt. ")
    parser.addoption("--dataset-datetime-fields",
                     dest="dataset_datetime_fields",
                     action="store", default=None,
                     help="Regex to extract other date/time fields from filename. ")
    parser.addoption("--dataset-datetime-fields-groups",
                     dest="dataset_datetime_fields_groups",
                     action="store", default=None,
                     help="Group names in date/time fields regex for extracting date/time fields. ")

def pytest_configure(config):
    """
        Configuration: add marks
    """
    config.addinivalue_line("markers", "skip_dataset_noneexistence: mark "
                            "test as dataset-name to run")
    config.addinivalue_line("markers", "skip_dataset_collection_noneexistence: mark "
                            "test as dataset-name-list to run")
    config.addinivalue_line("markers", "skip_dataset_is_swath_noneexistence: mark "
                            "test as dataset-is-swath to run")
    config.addinivalue_line("markers", "skip_dataset_is_grid_noneexistence: mark "
                            "test as dataset-is-grid to run")

def pytest_collection_modifyitems(config, items):
    """
        Modify CLI options with markers.
    """
    # --dataset-name
    _pytest_collection_modifyitems1(config, items)
    # --dataset-list
    _pytest_collection_modifyitems2(config, items)
    # --dataset-is-swath
    _pytest_collection_modifyitems3(config, items)
    # --dataset-is-grid
    _pytest_collection_modifyitems4(config, items)


def _pytest_collection_modifyitems1(config, items):
    # --dataset-name
    if config.getoption("--dataset-name"):
        # --dataset-name given in cli: do not skip dataset tests
        return
    skip_dataset_noneexistence = pytest.mark.skip(reason="need --dataset-name option to run")
    for item in items:
        if "skip_dataset_noneexistence" in item.keywords:
            item.add_marker(skip_dataset_noneexistence)

def _pytest_collection_modifyitems2(config, items):
    # --dataset-name-list
    if config.getoption("--dataset-name-list"):
        # --dataset-name-list given in cli: do not skip dataset tests
        return
    skip_dataset_collection_noneexistence = pytest.mark.skip(reason="need --dataset-name-list "
                                                             "option to run")
    for item in items:
        if "skip_dataset_collection_noneexistence" in item.keywords:
            item.add_marker(skip_dataset_collection_noneexistence)

def _pytest_collection_modifyitems3(config, items):
    # --dataset-is-swath
    if config.getoption("--dataset-is-swath"):
        # --dataset-is-swath given in cli: do not skip dataset tests
        return
    skip_dataset_is_swath_noneexistence = pytest.mark.skip(reason="need --dataset-is-swath "
                                                           "option to run")
    for item in items:
        if "skip_dataset_is_swath_noneexistence" in item.keywords:
            item.add_marker(skip_dataset_is_swath_noneexistence)

def _pytest_collection_modifyitems4(config, items):
    # --dataset-is-grid
    if config.getoption("--dataset-is-grid"):
        # --dataset-is-grid given in cli: do not skip dataset tests
        return
    skip_dataset_is_grid_noneexistence = pytest.mark.skip(reason="need --dataset-is-grid "
                                                           "option to run")
    for item in items:
        if "skip_dataset_is_grid_noneexistence" in item.keywords:
            item.add_marker(skip_dataset_is_grid_noneexistence)
