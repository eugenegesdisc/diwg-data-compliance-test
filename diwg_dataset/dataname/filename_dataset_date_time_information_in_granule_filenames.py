"""
    For recommendation:

    Date-Time Information in Granule Filenames

    verify if the dataset (granule) filename has date/time fields.

"""
import os
import re
import dateutil.parser as duparser

class FilenameDatasetDateTimeInformationInGranuleFilenames:
    """
        This class is for testing:
        Date-Time Information in Granule Filenames

        https://wiki.earthdata.nasa.gov/display/ESDSWG/Date-Time+Information+in+Granule+Filenames
    """
    iso8601_regs = [r"(?P<YYYY>(19|20)[0-9]{2})(?P<MM>0[1-9]|1[1,2])(?P<DD>0[1-9]|[12][0-9]|3[01])T(?P<hh>0[1-9]|[1-5][0-9])(?P<mm>0[1-9]|[1-5][0-9])(?P<ss>0[1-9]|[1-5][0-9])[,.](?P<f>[0-9]+)Z",
                    r"(?P<YYYY>(19|20)[0-9]{2})(?P<MM>0[1-9]|1[1,2])(?P<DD>0[1-9]|[12][0-9]|3[01])T(?P<hh>0[1-9]|[1-5][0-9])(?P<mm>0[1-9]|[1-5][0-9])(?P<ss>0[1-9]|[1-5][0-9])Z",
                    r"(?P<YYYY>(19|20)[0-9]{2})(?P<MM>0[1-9]|1[1,2])(?P<DD>0[1-9]|[12][0-9]|3[01])T(?P<hh>0[1-9]|[1-5][0-9])(?P<mm>0[1-9]|[1-5][0-9])Z",
                    r"(?P<YYYY>(19|20)[0-9]{2})(?P<MM>0[1-9]|1[1,2])(?P<DD>0[1-9]|[12][0-9]|3[01])T(?P<hh>0[1-9]|[1-5][0-9])Z",r"(?P<YYYY>(19|20)[0-9]{2})(?P<MM>0[1-9]|1[1,2])(?P<DD>0[1-9]|[12][0-9]|3[01])",
                    r"(?P<YYYY>(19|20)[0-9]{2})(?P<MM>0[1-9]|1[1,2])",
                    r"(?P<YYYY>(19|20)[0-9]{2})"]

    def validate_dataname_date_time_information(
            self, dataset_name:str,
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
            @param dataset_name: Full path to a granuale file.
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
        _datetime_info = self.get_dataname_date_time_information(
            dataset_name=dataset_name,
            dataset_datetime=dataset_datetime,
            dataset_datetime_group=dataset_datetime_group,
            dataset_pdt=dataset_pdt,
            dataset_pdt_group=dataset_pdt_group,
            dataset_datetime_fields=dataset_datetime_fields,
            dataset_datetime_fields_groups=dataset_datetime_fields_groups)
        _datetime_info["valid"] = dict()
        _datetime_info["valid"]["skip"] = False
        # set skip to True if no date_info found in filename
        if (not _datetime_info["temporal_extent"]
            or not _datetime_info["date_time_fields"]):
            _datetime_info["valid"]["skip"] = True
            return _datetime_info

        # iso8601 format
        _datetime_info["valid"]["iso"] = True
        self._validate_dataname_date_time_inforamtion_iso8601(_datetime_info)

        # tempoeral interval order
        _datetime_info["valid"]["temporal_order"] = True
        self._validate_dataname_date_time_information_temporal_order(_datetime_info)

        # datetime field order
        _datetime_info["valid"]["fields_order"] = True
        self._validate_dataname_date_time_information_fields_order(_datetime_info)

        # same format
        _datetime_info["valid"]["same_isoformat"] = True
        self._validate_dataname_date_time_inforamtion_same_iso8601_format(_datetime_info)

        # set overall evaluation
        _datetime_info["valid"]["overall"] = True
        if (not _datetime_info["valid"]["iso"]
            or not _datetime_info["valid"]["temporal_order"]
            or not _datetime_info["valid"]["fields_order"]
            or not _datetime_info["valid"]["same_isoformat"]):
            _datetime_info["valid"]["overall"] = False


        return _datetime_info

    def _validate_dataname_date_time_inforamtion_same_iso8601_format(
            self, datetime_info:dict):
        """
            All date-time fields should have the same format.

            Also ensures:
                Date-time information should always be in the UTC time zone.
                The delimiter between the seconds and the fraction of a second can only be the comma or the full stop.
            @return: 
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
                valid:{
                    "skip": False,
                    "iso": True
                    "temporal_order": True,
                    "fields_order": True,
                    "same_isoformat": True
                }
            }
        """
        _format = -2
        for _f in datetime_info['temporal_extent']:
            _d_formats = self._detect_iso8601_format_from_token(_f['token'])
            # nof found in the narrow-down iso format - failed
            if not _d_formats:
                datetime_info['valid']['same_isoformat'] = False
                return
            if _format < -1:
                _format = _d_formats[0]
            if len(_d_formats) > 1:
                print("Error - multiple match found for " + _f["token"])
                print("matches=", _d_formats)
            for _k in _d_formats:
                if _format != _k:
                    datetime_info['valid']['same_isoformat'] = False
                    return

        for _f in datetime_info['date_time_fields']:
            _d_formats = self._detect_iso8601_format_from_token(_f['token'])
            # nof found in the narrow-down iso format - failed
            if not _d_formats:
                datetime_info['valid']['same_isoformat'] = False
                return
            if _format < -1:
                _format = _d_formats[0]
            if len(_d_formats) > 1:
                print("Error - multiple match found for " + _f["token"])
            for _k in _d_formats:
                if _format != _k:
                    datetime_info['valid']['same_isoformat'] = False
                    return

    def _detect_iso8601_format_from_token(
            self, token:str)->list:
        """
            @return: order number in iso8601_regs. -1 if not detected.
        """
        _ret = list()
        for _i, _v in enumerate(self.iso8601_regs):
            if self._regex_pattern_match(pattern=_v, token=token):
                _ret.append(_i)
        return _ret

    def _regex_pattern_match(
            self, pattern:str, token:str)->bool:
        """
            Do an exact match by attaching '^' and '$'.
            @return: order number in iso8601_regs. -1 if not detected.
        """
        _p = re.compile("^"+pattern+"$")
        _m = re.match(_p,token)
        if _m:
            return True
        return False

    def _validate_dataname_date_time_information_fields_order(
            self, datetime_info:dict):
        """
            Date-time fields representing the temporal extent of a granule's data should appear before
            any other date-time field in the file name.
            @return: 
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
                valid:{
                    "iso": True,
                    "temporal_order": True
                }
            }
        """
        if len(datetime_info["temporal_extent"]) < 1:
            return
        _temp_pos = datetime_info['temporal_extent'][0]['end']
        for _fd in datetime_info['temporal_extent']:
            if _temp_pos < _fd['end']:
                _temp_pos = _fd['end']

        for _fd in datetime_info["date_time_fields"]:
            if _fd['start'] < _temp_pos:
                datetime_info["valid"]["fields_order"] = False
                return

    def _validate_dataname_date_time_information_temporal_order(
            self, datetime_info:dict):
        """
            If describing a date-time interval, the start date-time should appear before the end
            date-time.
            @return: 
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
                valid:{
                    "skip": False,
                    "iso": True,
                    "temporal_order": True
                }
            }
        """
        if len(datetime_info["temporal_extent"]) < 2:
            return
        _begin = self._retrieve_elements_by_key_value(
            dict_list=datetime_info["temporal_extent"],
            key="field_name",
            value="temporal_begin")
        _end = self._retrieve_elements_by_key_value(
            dict_list=datetime_info["temporal_extent"],
            key="field_name",
            value="temporal_begin")
        if (not _begin or
            not _end):
            return
        _begin_value = self._convert_token_to_datetime(_begin[0]['token'])
        _end_value = self._convert_token_to_datetime(_end[0]['token'])
        if (not _begin_value or
            not _end_value):
            datetime_info['valid']['temporal_order'] = False
            return
        if _begin_value > _end_value:
            datetime_info['valid']['temporal_order'] = False
            return
        if (_begin[0]['start'] > _end[0]['start']
            or _begin[0]['end'] > _end[0]['start']):
            datetime_info['valid']['temporal_order'] = False

    def _convert_token_to_datetime(
            self, token:str):
        _ret = None
        try:
            _ret = duparser.isoparse(token)
            return _ret
        except Exception as er:
            print("Error: ", str(er))
            return _ret

    def _retrieve_elements_by_key_value(
            self, dict_list:list, key:str, value:str):
        return [k for k in dict_list if k[key] == value]

    def _validate_dataname_date_time_inforamtion_iso8601(
            self, datetime_info:dict):
        """
            Adopt the ISO 8601 [11] standard for date-time information representation.
            @return: 
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
                valid:{
                    "iso": True
                }
            }
        """
        for _f in datetime_info['temporal_extent']:
            if self._validate_token_iso8601(_f['token']):
                _f['iso'] = True
            else:
                _f['iso'] = False
                datetime_info['valid']['iso'] = False

        for _f in datetime_info['date_time_fields']:
            if self._validate_token_iso8601(_f['token']):
                _f['iso'] = True
            else:
                _f['iso'] = False
                datetime_info['valid']['iso'] = False

    def _validate_token_iso8601(
            self, token:str):
        try:
            duparser.isoparse(token)
            return True
        except Exception as er:
            print("Error: ", er)
            return False

    def get_dataname_date_time_information(
            self, dataset_name:str,
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
            @param dataset_name: Full path to a granuale file.
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
                "dataset_name":"/some/path/DeepBlue-SeaWiFS_L2_20101210T135954Z_v004-20130525T172725Z.h5",
                "error":"message for error if error exists",
                "filename": "DeepBlue-SeaWiFS_L2_20101210T135954Z_v004-20130525T172725Z.h5",
                "temporal_extent":[
                    {
                        "field_name":"temporal_begin",
                        "token":"20101210T135954Z"
                        "start":20,
                        "end": 36,
                        "value": <value in datetime>
                    }]
                "date_time_fields":[
                    {
                        "field_name":"pdt",
                        "token":"20130525T172725Z",
                        "start": 42,
                        "end": 58
                    }
                ]
            }
        """
        _the_ret = dict()
        _the_ret["dataset_name"] = dataset_name
        _the_ret["temporal_extent"] = list()
        _the_ret["date_time_fields"] = list()
        try:
            (_the_format,
            _the_file,
            _the_groups,
            _the_var
            ) = self._gdal_parse_variables_groups_from_dataset_name(
                dataset_name)           
            # extract dataset unique identifier
            _the_filename = os.path.basename(_the_file)
            _the_ret["filename"] = _the_filename
            self._gdal_get_dataname_date_time_information(
                _the_ret, _the_filename,
                dataset_datetime=dataset_datetime,
                dataset_datetime_group=dataset_datetime_group,
                dataset_pdt=dataset_pdt,
                dataset_pdt_group=dataset_pdt_group,
                dataset_datetime_fields=dataset_datetime_fields,
                dataset_datetime_fields_groups=dataset_datetime_fields_groups)
        except Exception as err:
            _the_ret["error"]=str(err)

        return _the_ret

    def _gdal_get_dataname_date_time_information(
            self,
            datetime_info:dict,
            filename:str,
            dataset_datetime:str=None,
            dataset_datetime_group:str=None,
            dataset_pdt:str=None,
            dataset_pdt_group:str=None,
            dataset_datetime_fields:str=None,
            dataset_datetime_fields_groups:str=None):
        """
            @param datetime_info: [In/Out] Hold the date/time information extracted
                from filename.
            @param filename: granule filename.
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
                "dataset_name":"/some/path/DeepBlue-SeaWiFS_L2_20101210T135954Z_v004-20130525T172725Z.h5",
                "error":"message for error if error exists",
                "filename": "DeepBlue-SeaWiFS_L2_20101210T135954Z_v004-20130525T172725Z.h5",
                "temporal_extent":[
                    {
                        "field_name":"temporal_begin",
                        "token":"20101210T135954Z"
                        "start":20,
                        "end": 36,
                        "value": <value in datetime>
                    }]
                "date_time_fields":[
                    {
                        "field_name":"pdt",
                        "token":"20130525T172725Z",
                        "start": 42,
                        "end": 58
                    }
                ]
            }
        """
        # extract datset temporal extent from filename
        # if there are more than 2 fields retrieved, only the first two used.
        if dataset_datetime:
            _fields = self._gdal_extract_fields_from_filename_using_regex_groups(
                pattern=dataset_datetime,
                group_names=dataset_datetime_group,
                filename=filename)
            if len(_fields)>0:
                _f = _fields[0]
                _f["field_name"] = "temporal_begin"
                datetime_info["temporal_extent"].append(_f)
            if len(_fields)>1:
                _f = _fields[1]
                _f["field_name"] = "temporal_end"
                datetime_info["temporal_extent"].append(_f)
            if len(_fields)>2:
                _more_fields = _fields[2:]
                for _fd in _more_fields:
                    datetime_info["date_time_fields"].append(_fd)
        # extract datset pdt
        if dataset_pdt:
            _fields = self._gdal_extract_fields_from_filename_using_regex_groups(
                pattern=dataset_pdt,
                group_names=dataset_pdt_group,
                filename=filename)
            datetime_info["date_time_fields"].extend(_fields)
        # extract other fields
        if dataset_datetime_fields:
            _field_regexs = dataset_datetime_fields.split("++")
            print("fields=", _field_regexs)
            if not dataset_datetime_fields_groups:
                for _fr in _field_regexs:
                    datetime_info["date_time_fields"].extend(
                        self._gdal_extract_fields_from_filename_using_regex_groups(
                            pattern=_fr,
                            group_names=None,
                            filename=filename))
            else:
                _group_names = dataset_datetime_fields_groups.split(";")
                if len(_group_names) != len(_field_regexs):
                    raise ValueError("Unmatch group names and expressions for fields: "
                                     + dataset_datetime_fields_groups +" vs "
                                     + dataset_datetime_fields)
                for _i, _fr in enumerate(_field_regexs):
                    datetime_info["date_time_fields"].extend(
                        self._gdal_extract_fields_from_filename_using_regex_groups(
                            pattern=_fr,
                            group_names=_group_names[_i],
                            filename=filename))
        # auto-detect all ISO8601 pattern
        if not dataset_datetime:
            self._gdal_auto_extract_iso8601_dateinfo_from_filename(
                datetime_info,filename)

    def _gdal_auto_extract_iso8601_dateinfo_from_filename(
            self,
            datetime_info:dict,
            filename:str):
        _fields = self._gdal_auto_detect_iso8601_dateinfo_from_filename(
            filename=filename)
        if len(_fields)>0:
            _f = _fields[0]
            _f["field_name"] = "temporal_begin"
            datetime_info["temporal_extent"].append(_f)
        #if len(_fields)>1:
        #    _f = _fields[1]
        #    _f["field_name"] = "temporal_end"
        #    datetime_info["temporal_extent"].append(_f)
        #if len(_fields)>2:
        #    _more_fields = _fields[2:]
        if len(_fields)>1:
            _more_fields = _fields[1:]
            for _fd in _more_fields:
                if not self._gdal_check_field_exist_in_list(
                    datetime_info["date_time_fields"],
                    _fd):
                    datetime_info["date_time_fields"].append(_fd)

    def _gdal_check_field_exist_in_list(
            self, date_time_fields:list[dict],
            key_field:dict)->bool:
        for _f in date_time_fields:
            if (_f['token'] == key_field['token']
                and _f['start'] == key_field['start']
                and _f['end'] == key_field['end']):
                return True
        return False

    def _gdal_auto_detect_iso8601_dateinfo_from_filename(
            self, filename:str)->list[dict]:
        """
            Detect ISO8601 format using regex. One by one from the following
            list. Stop if any match is found. Only for years between 1900 and 2099.

            ISO8601 format              Regex
            ------------------------    ----------------
            YYYYMMDDThhmmss[,.]f+Z      r'(?P<YYYY>(19|20)[0-9]{2})(?P<MM>0[1-9]|1[1,2])(?P<DD>0[1-9]|[12][0-9]|3[01])T(?P<hh>0[1-9]|[1-5][0-9])(?P<mm>0[1-9]|[1-5][0-9])(?P<ss>0[1-9]|[1-5][0-9])[,.](?P<f>[0-9]+)Z'
            YYYYMMDDThhmmssZ            r'(?P<YYYY>(19|20)[0-9]{2})(?P<MM>0[1-9]|1[1,2])(?P<DD>0[1-9]|[12][0-9]|3[01])T(?P<hh>0[1-9]|[1-5][0-9])(?P<mm>0[1-9]|[1-5][0-9])(?P<ss>0[1-9]|[1-5][0-9])Z'
            YYYYMMDDThhmmZ              r'(?P<YYYY>(19|20)[0-9]{2})(?P<MM>0[1-9]|1[1,2])(?P<DD>0[1-9]|[12][0-9]|3[01])T(?P<hh>0[1-9]|[1-5][0-9])(?P<mm>0[1-9]|[1-5][0-9])Z'
            YYYYMMDDThhZ                r'(?P<YYYY>(19|20)[0-9]{2})(?P<MM>0[1-9]|1[1,2])(?P<DD>0[1-9]|[12][0-9]|3[01])T(?P<hh>0[1-9]|[1-5][0-9])Z'
            YYYYMMDD                    r'(?P<YYYY>(19|20)[0-9]{2})(?P<MM>0[1-9]|1[1,2])(?P<DD>0[1-9]|[12][0-9]|3[01])'
            YYYY-MM                     r'(?P<YYYY>(19|20)[0-9]{2})(?P<MM>0[1-9]|1[1,2])'
            YYYY                        r'(?P<YYYY>(19|20)[0-9]{2})'
        """
        
        for _regstr in self.iso8601_regs:
            _match = self._gdal_extract_fields_from_filename_using_regex_groups(
                pattern=_regstr,
                group_names=None,
                filename=filename)
            if _match:
                return _match
        return list()
    
    def _gdal_extract_fields_from_filename_using_regex_groups(
            self, pattern:str,
            group_names:str,
            filename:str)->list[dict]:
        _p = re.compile(pattern)
        _groups = list()
        if group_names:
            _groups = group_names.split(",")
        _f = re.finditer(_p,filename)
        _ret = list()
        if not _f:
            return _ret
        for _i in _f:
            _ret += self._gdal_extract_allgroups(_i, _groups)
        return _ret

    def _gdal_extract_allgroups(
            self, re_match, groups:list[str])->list[dict]:
        _ret = list()
        if not re_match:
            return _ret
        if not groups:
            _t = dict()
            _t["field_name"] = ""
            _t["token"] = re_match.group()
            _t["start"] = re_match.start()
            _t["end"] = re_match.end()
            _ret.append(_t)
            return _ret
        for _g in groups:
            if _g in re_match.groupdict():
                _t = dict()
                _t["field_name"] = _g
                _t["token"] = re_match.group(_g)
                _t["start"] = re_match.start(_g)
                _t["end"] = re_match.end(_g)
                _ret.append(_t)
        return _ret

    def _gdal_extract_from_substring_using_regex_group(
            self, pattern:str,
            group_name:str,
            substring:str)->str:
        _p = re.compile(pattern)
        _f = re.search(_p,substring)
        if (_f and 
            group_name in _f.groupdict()):
            return _f[group_name]
        return ""


    def _gdal_parse_variables_groups_from_dataset_name(
            self, dataset_name:str)->tuple:
        """
            @param dataset_name: 
                Examples - "/some/path/test.nc"
                    'NETCDF:"/some/pat/test.nc":variable1'
                    'NETCDF:"/some/pat/test.nc":/variable1'
                    'NETCDF:"/some/pat/test.nc"://variable1'
                    'NETCDF:"/some/pat/test.nc":/group/variable1'
                    'NETCDF:"/some/pat/test.nc"://group/variable1"
            return:
                (format, filename, groups, variable, variable_fullpath)
                For examples:
                ('', '', [], '')
                ('', "/some/path/test.nc", [], '')
                ('NETCDF', "/some/path/test.nc", [], 'variable1')
                ('NETCDF', "/some/path/test.nc", [""], 'variable1')
                ('NETCDF', "/some/path/test.nc", ["", ""], 'variable1')
                ('NETCDF', "/some/path/test.nc", ["", 'group'], 'variable1')
                ('NETCDF', "/some/path/test.nc", ["", "", 'group'], 'variable1')
                
            Empty string will be the fill value for each field.
        """
        _the_format = ''
        _the_filename = ''
        _the_groups = []
        _the_variable = ''
        if dataset_name is None:
            return _the_format, _the_filename, _the_groups, _the_variable
        if ':"' in dataset_name:
            _the_strs = dataset_name.split(':"', 1)
            _the_format = _the_strs[0]
            if '":' in _the_strs[1]:
                _the_strs2 = _the_strs[1].rsplit('":', 1)
                _the_filename = _the_strs2[0]
                _the_group_variable_str = _the_strs2[1]
                _the_gv_strs = _the_group_variable_str.split('/')
                _the_len = len(_the_gv_strs)-1
                _the_variable = _the_gv_strs[-1]
                for _i in range(_the_len):
                    _the_groups.append(_the_gv_strs[_i])
            else:
                if _the_strs[1].endswith('"'):
                    _the_filename = _the_strs[1][:-1]
                else:
                    print(f"Warning: parse failed at {dataset_name}. "
                            "Assuming only filename included")
                    _the_format = ''
                    _the_filename = dataset_name
        else:
            _the_filename = dataset_name
        return _the_format, _the_filename, _the_groups, _the_variable
