"""
    For recommendation: 

    Ensure Granule's Filename Uniqueness Across Different Dataset Releases

    filename unique.
"""
import glob
from diwg_dataset.dataname.filename_dataset_ensure_granule_filename_uniqueness_across_different_dataset_releases import (
    FilenameDatasetEnsureGranuleFilenameUniqueness
)
class FilenameDatasetCollectionEnsureGranuleFilenameUniqueness:
    """
        This class is for testing:
            Ensure Granule's Filename Uniqueness Across Different Dataset Releases

            https://wiki.earthdata.nasa.gov/display/ESDSWG/Ensure+Granule%27s+Filename+Uniqueness+Across+Different+Dataset+Releases
    """
    def get_dataname_uniqueness(
            self,dataset_name_listfile:str,
            dataset_id:str=None,
            dataset_crid:str=None,
            dataset_datetime:str=None,
            dataset_pdt:str=None)->dict:
        """
            Check the uniquess of filename in a collection over different releases.
            @param dataset_name_listfile: Full path to a file of granule collection.
            @param dataset_id: a unique dataset identifier
                or a regex expression for such id to be extracted from the filename or 
                to be matched in the filename. Multiple patterns are combined with "|".
            @param dataset_crid: a unique identifier for each release (version, collection)
                of the dataset or a unique Combined Release ID or a regex expression for such 
                id to be extracted from the filename or to be matched in the filename.
                Multiple patterns are combined with "|".
            @param dataset_datetime: the date-time, or any part thereof as applicable,
                of the first data observation in the file or
                a regex for such part to be extracted from the filename or to be matched in the
                filename. Multiple patterns are combined with "|".
            @param dataset_pdt: the Production Date Time (PDT), or any part representing
                produced more than once for the same release, in the filename, or a regex 
                for such part to be extracted from the filename
                or to be matched in the filename. Multiple patterns are combined with "|".
            @return: 
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
        _the_ret = dict()
        _the_ret["collection_name"] = dataset_name_listfile
        _the_ret["datasets"] = list()
        _the_c = self.get_dataname_partitions(
            dataset_name_listfile=dataset_name_listfile,
            dataset_id=dataset_id,
            dataset_crid=dataset_crid,
            dataset_datetime=dataset_datetime,
            dataset_pdt=dataset_pdt
        )
        if "error" in _the_c:
            _the_ret["error"]=_the_c["error"]
            return _the_ret
        self._screen_duplicates(_the_ret,_the_c["datasets"])
        return _the_ret

    def _screen_duplicates(
            self, dup_ret:dict, dataset_list:dict):
        _uniq_list = list()
        _dup_set = set()

        for k in dataset_list:
            _the_f = k["partition"]["filename"]
            if _the_f not in _uniq_list:
                _uniq_list.append(_the_f)
            else:
                _dup_set.add(_the_f)
        if not _dup_set:
            return    
        for k in dataset_list:
            _the_f = k["partition"]["filename"]
            if _the_f in _dup_set:
                dup_ret["datasets"].append(k)

    def get_dataname_partitions(
            self,dataset_name_listfile:str,
            dataset_id:str=None,
            dataset_crid:str=None,
            dataset_datetime:str=None,
            dataset_pdt:str=None)->dict:
        """
            Retrieve file partitions of datasets (granules) in a collection.
            @param dataset_name_listfile: Full path to a file of granule collection.
            @param dataset_id: a unique dataset identifier
                or a regex expression for such id to be extracted from the filename or 
                to be matched in the filename. Multiple patterns are combined with "|".
            @param dataset_crid: a unique identifier for each release (version, collection)
                of the dataset or a unique Combined Release ID or a regex expression for such 
                id to be extracted from the filename or to be matched in the filename.
                Multiple patterns are combined with "|".
            @param dataset_datetime: the date-time, or any part thereof as applicable,
                of the first data observation in the file or
                a regex for such part to be extracted from the filename or to be matched in the
                filename. Multiple patterns are combined with "|".
            @param dataset_pdt: the Production Date Time (PDT), or any part representing
                produced more than once for the same release, in the filename, or a regex for 
                such part to be extracted from the filename
                or to be matched in the filename. Multiple patterns are combined with "|".
            @return: 
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
        _the_ret = dict()
        _the_ret["collection_name"] = dataset_name_listfile
        _the_ret["datasets"] = list()

        try:
            with open(dataset_name_listfile, "r",encoding="utf-8") as _the_file:
                _the_lines = _the_file.readlines()
            for _line in _the_lines:
                _the_line = _line.strip()
                if _the_line:
                    _the_sfiles = glob.glob(_the_line)
                    # in case of a single GDAL dataset
                    if len(_the_sfiles) == 0:
                        _the_sfiles = [_the_line]
                    for _the_sfile in _the_sfiles:
                        dmp = FilenameDatasetEnsureGranuleFilenameUniqueness()
                        _the_ret["datasets"].append(
                            dmp.get_dataname_partitions(
                                dataset_name=_the_sfile,
                                dataset_id=dataset_id,
                                dataset_crid=dataset_crid,
                                dataset_datetime=dataset_datetime,
                                dataset_pdt=dataset_pdt))
        except Exception as err:
            _the_ret["error"]=str(err)

        return _the_ret
