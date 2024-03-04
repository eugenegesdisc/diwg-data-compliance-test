"""
    For recommendation:

    Ensure Granule's Filename Uniqueness Across Different Dataset Releases

    Partition filename.

"""
import re
import os

class FilenameDatasetEnsureGranuleFilenameUniqueness:
    """
        This class is for testing:
            Ensure Granule's Filename Uniqueness Across Different Dataset Releases

            https://wiki.earthdata.nasa.gov/display/ESDSWG/Ensure+Granule%27s+Filename+Uniqueness+Across+Different+Dataset+Releases
    """
    def get_dataname_partitions(self,
                                dataset_name:str,
                                dataset_id:str=None,
                                dataset_crid:str=None,
                                dataset_datetime:str=None,
                                dataset_pdt:str=None)->dict:
        """
            Get filename exteion for the dataset.
            @param dataset_name: Full path to a granuale file.
            @param dataset_id: a unique dataset identifier
                or a regex expression for such id to be extracted from the filename or 
                to be matched in the filename.
            @param dataset_crid: a unique identifier for each release (version, collection)
                of the dataset or a unique Combined Release ID or a regex expression for such 
                id to be extracted from the filename or to be matched in the filename.
            @param dataset_datetime: the date-time, or any part thereof as applicable,
                of the first data observation in the file or
                a regex for such part to be extracted from the filename or to be matched in the
                filename. 
            @param dataset_pdt: the Production Date Time (PDT), or any part representing
                produced more than once for the same release, in the filename, or a regex for such part to be extracted from the filename
                or to be matched in the filename. 
            @return: 
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
        """
        _the_ret = dict()
        _the_ret["dataset_name"] = dataset_name
        _the_ret["partition"] = dict()
        try:
            (_the_format,
            _the_file,
            _the_groups,
            _the_var
            ) = self._gdal_parse_variables_groups_from_dataset_name(
                dataset_name)           
            # extract dataset unique identifier
            _the_filename = os.path.basename(_the_file)
            _the_ret["partition"]["filename"] = _the_filename
            # extract dataset combined release ID
            if dataset_id:
                _the_ret["partition"]["id"] = self._gdal_extract_from_filename_using_regex(
                    dataset_id, _the_filename)
            # extract granule crid (composite release id)
            if dataset_crid:
                _the_ret["partition"]["crid"] = self._gdal_extract_from_filename_using_regex(
                    pattern=dataset_crid, filename=_the_filename)
            # extract granule datetime
            if dataset_datetime:
                _the_ret["partition"]["datetime"] = self._gdal_extract_from_filename_using_regex(
                    dataset_datetime, _the_filename)
            # extract production date time
            if dataset_pdt:
                _the_ret["partition"]["pdt"] = self._gdal_extract_from_filename_using_regex(
                    dataset_pdt, _the_filename)

        except Exception as err:
            _the_ret["error"]=str(err)

        return _the_ret

    def _gdal_extract_from_filename_using_regex(
            self, pattern:str, filename:str)->str:
        _p = re.compile(pattern)
        _f = re.findall(_p,filename)
        if _f:
            if len(_f) > 1:
                print("Warning: ambiguous pattern for id: pattern="+
                        pattern+ " filename=" +
                        filename)
            return _f[0]
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
