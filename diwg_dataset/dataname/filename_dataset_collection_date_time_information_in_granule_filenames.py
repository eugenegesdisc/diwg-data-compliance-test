"""
    For recommendation: 

    Date-Time Information in Granule Filenames

    verify if the dataset (granule) filename has proper date/time fields.
"""
import glob
from diwg_dataset.dataname.filename_dataset_date_time_information_in_granule_filenames import (
    FilenameDatasetDateTimeInformationInGranuleFilenames
)
class FilenameDatasetCollectionDateTimeInformationInGranuleFilenames:
    """
        This class is for testing:
        Date-Time Information in Granule Filenames

        https://wiki.earthdata.nasa.gov/display/ESDSWG/Date-Time+Information+in+Granule+Filenames
    """
    def validate_dataname_date_time_information(
            self,dataset_name_listfile:str,
            dataset_datetime:str=None,
            dataset_datetime_group:str=None,
            dataset_pdt:str=None,
            dataset_pdt_group:str=None,
            dataset_datetime_fields:str=None,
            dataset_datetime_fields_groups:str=None)->dict:
        """
            Extracft datetime information from the granule filename.
            If no datetime parameters are passed, temporal extent will be assumed one date
            but interval if there is any date-time is automatically extracted.
            @param dataset_name_listfile: Full path to a list file of granule collection.
            @param dataset_datetime: a RegEx pattern to extract temporal information. It can be
                a pattern to retrieve one datetime or a temporal extent (start to end)
            @param dataset_datetime_group: a list of group names up to two elements used in 
                dataset_datetime. Elements are separated by ','. If two elements, the first 
                one will be corresponding to the begin of time and the second the end for 
                a temporal extent.
            @param dataset_pdt: a RegEx pattern to extract Production Date Time.
            @param dataset_pdt_group: a group names for Production Date Time used in
                dataset_pdt.
            @param dataset_datetime_fields: a list of RegEx patterns to extract any other datatime
                fields from the filename. Different regular expressions are separate by "++", 
                e.g. "reg1++reg2++reg3" ==>["reg1", "reg2", "reg3"]
            @param dataset_datetime_fields_group: a list of group names used in 
                dateset_datetime_fields. If given, the number of group names should be the same
                as that of dataset_datetime_fields. Each group name is corresponding to the datetime
                field at the exact index. The seperator will be ';'. Internal group separator is
                ",". For example, 'group1_0;;group3_1,group3_2' would be for reg1, there is one 
                group1_0. For reg2, there is no group. For reg3, there are two groups
                - group3_1 and group3_2.
            @return: 
            {
                collection_name: "thecollection_list.file",
                error: "Error message if there is error",
                datasets: [
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
                ],
                "valid": {
                    "skip": False
                }
            }
        """
        _ret = self.get_validate_dataname_date_time_information(
            dataset_name_listfile=dataset_name_listfile,
            dataset_datetime=dataset_datetime,
            dataset_datetime_group=dataset_datetime_group,
            dataset_pdt=dataset_pdt,
            dataset_pdt_group=dataset_pdt_group,
            dataset_datetime_fields=dataset_datetime_fields,
            dataset_datetime_fields_groups=dataset_datetime_fields_groups)
        _datasets = _ret['datasets']
        _new_ds = list()
        _ret['datasets'] = _new_ds
        _ret['valid'] = dict()
        _skip = 0
        for _ds in _datasets:
            if _ds['valid']['skip']:
                _skip += 1
                continue
            if not _ds['valid']['status']:
                _new_ds.append(_ds)
        if _skip == len(_datasets):
            _ret['valid']['skip'] = True
        else:
            _ret['valid']['skip'] = False

        return _ret

    def get_validate_dataname_date_time_information(
            self,dataset_name_listfile:str,
            dataset_datetime:str=None,
            dataset_datetime_group:str=None,
            dataset_pdt:str=None,
            dataset_pdt_group:str=None,
            dataset_datetime_fields:str=None,
            dataset_datetime_fields_groups:str=None)->dict:
        """
            Extracft datetime information from the granule filename.
            If no datetime parameters are passed, temporal extent will be assumed one date
            but interval if there is any date-time is automatically extracted.
            @param dataset_name_listfile: Full path to a list file of granule collection.
            @param dataset_datetime: a RegEx pattern to extract temporal information. It can be
                a pattern to retrieve one datetime or a temporal extent (start to end)
            @param dataset_datetime_group: a list of group names up to two elements used in 
                dataset_datetime. Elements are separated by ','. If two elements, the first 
                one will be corresponding to the begin of time and the second the end for 
                a temporal extent.
            @param dataset_pdt: a RegEx pattern to extract Production Date Time.
            @param dataset_pdt_group: a group names for Production Date Time used in
                dataset_pdt.
            @param dataset_datetime_fields: a list of RegEx patterns to extract any other datatime
                fields from the filename. Different regular expressions are separate by "++", 
                e.g. "reg1++reg2++reg3" ==>["reg1", "reg2", "reg3"]
            @param dataset_datetime_fields_group: a list of group names used in 
                dateset_datetime_fields. If given, the number of group names should be the same
                as that of dataset_datetime_fields. Each group name is corresponding to the datetime
                field at the exact index. The seperator will be ';'. Internal group separator is
                ",". For example, 'group1_0;;group3_1,group3_2' would be for reg1, there is one 
                group1_0. For reg2, there is no group. For reg3, there are two groups
                - group3_1 and group3_2.
            @return: 
            {
                collection_name: "thecollection_list.file",
                error: "Error message if there is error",
                datasets: [
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
                        dmp = FilenameDatasetDateTimeInformationInGranuleFilenames()
                        _the_ret["datasets"].append(
                            dmp.validate_dataname_date_time_information(
                                dataset_name=_the_sfile,
                                dataset_datetime=dataset_datetime,
                                dataset_datetime_group=dataset_datetime_group,
                                dataset_pdt=dataset_pdt,
                                dataset_pdt_group=dataset_pdt_group,
                                dataset_datetime_fields=dataset_datetime_fields,
                                dataset_datetime_fields_groups=dataset_datetime_fields_groups))
        except Exception as err:
            _the_ret["error"]=str(err)

        return _the_ret
