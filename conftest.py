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
