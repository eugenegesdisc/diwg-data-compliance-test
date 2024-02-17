"""
    Retrieve all variables and their coordinate attributes in a dataset.
    "include_time" is set true if it has coord ending with "time" (case-insensitive)
"""
import re
import json
import string
from osgeo import gdal

class DatasetIncludeTimeCoordInSwath:
    """
        This class is for testing:
            Include Time Coordinate in Swath Structured Data
    """

    def get_variables_with_dims(self,dataset_name:str)->dict:
        """
            Retrieve all the variables with dimensions and coordinates.
            This function utilizes gdalmdiminfo to retrieve variables, which should only
            work with dataset with multi-dimensional arrays, i.e. netcdf, hdf, hdfeos.
            @return: 
            {
                "dataset_name":"example.nc",
                "error":"message for error if error exists",
                "time_variables":['/somegroup/time'],
                "variables":[
                    {
                        "path": 'NETCDF:"somefile.nc"://group1/variable1',
                        "fullname":"//group1/variable1",
                        "name":"variable1",
                        "dimensions":['/nTimes','/nTrack'],
                        "coordinates":['time','lat','lon'],
                        "include_time": True}
                    ]
            }
        """
        gdal.UseExceptions()
        _the_variables = dict()
        _the_variables["dataset_name"] = dataset_name
        _the_variables["variables"] = list()

        try:
            _the_md_info = None
            (_the_format,
            _the_file,
            _the_groups,
            _the_var
            ) = self._gdal_parse_variables_groups_from_dataset_name(dataset_name)
            _gv_str = self._gdal_form_gv_path(_the_groups,_the_var)

            _the_md_info = gdal.MultiDimInfo(_the_file)

            if _the_md_info:
                self._gdal_get_variables_with_dims(
                    _the_variables,
                    _the_file,
                    _the_md_info
                )
            self._gdal_find_and_add_time_variables(_the_variables)
            _the_vars = _the_variables['variables']
            _the_variables['variables'] = [k for k in _the_vars if k[
                'fullname'].startswith(_gv_str)]
            self._gdal_verify_variable_include_time_coord(_the_variables)

        except Exception as err:
            _the_variables["error"]=str(err)

        return _the_variables

    def _gdal_find_and_add_time_variables(
            self,group_varables:dict):
        _the_times = list()
        for _the_var in group_varables['variables']:
            if _the_var['fullname'].lower().endswith('time'):
                _the_times.append(_the_var['fullname'])
        group_varables['time_variables'] = _the_times

    def _gdal_verify_variable_include_time_coord(
            self,group_varables:dict):
        # Assign 'include_time' soly depending on 'coordinates' attribute
        for _the_var in group_varables['variables']:
            _the_var['include_time']=self._check_coord_has_time(_the_var['coordinates'])

    def _check_coord_has_time(
            self,coords:list)->bool:
        for c in coords:
            if c.lower().endswith('time'):
                return True
        return False

    def _gdal_get_variables_with_dims(
            self, group_variables:dict,
            filename:str,
            dataset_info:dict):
        the_format = dataset_info['driver'].upper()
        if "arrays" in dataset_info:
            for ar in dataset_info['arrays']:
                the_o = dict()
                the_o["fullname"] = f"//{ar}"
                the_o["path"] = f'{the_format}:"{filename}"://{ar}'
                the_o["dimensions"] = []
                if 'dimensions' in dataset_info['arrays'][ar]:
                    the_o["dimensions"] = dataset_info['arrays'][ar]['dimensions']
                the_o['coordinates'] = list()
                if ('attributes' in dataset_info['arrays'][ar]
                    and 'coordinates' in dataset_info['arrays'][ar]['attributes']
                    ):
                    the_o['coordinates'] = dataset_info['arrays'][
                        ar]['attributes']['coordinates'].split(' ')
                group_variables['variables'].append(the_o)
        if "groups" in dataset_info:
            for grp in dataset_info['groups']:
                #dealing with whitespace group names for HDFEOS (e.g. 'Group Fields'
                # 'DHFEOS INFORMATION', 'Data Fields') to be in gdal path
                the_sgrp = grp.replace(" ", "_")
                the_group = f"//{the_sgrp}"
                group_info = dataset_info['groups'][grp]
                self._gdal_get_variables_with_dims_inner(
                    group_variables,
                    filename,
                    the_group,
                    the_format,
                    group_info
                )

    def _gdal_get_variables_with_dims_inner(
            self, group_variables:dict,
            filename:str,
            group:str,
            data_format:str,
            group_info:dict):
        if "arrays" in group_info:
            for ar in group_info['arrays']:
                the_o = dict()
                the_o["fullname"] = f"{group}/{ar}"
                the_o["path"] = f'{data_format}:"{filename}":{group}/{ar}'
                the_o["dimensions"] = list()
                if 'dimensions' in group_info['arrays'][ar]:
                    the_o['dimensions'] = group_info['arrays'][ar]['dimensions']
                the_o['coordinates'] = list()
                if ('attributes' in group_info['arrays'][ar]
                    and 'coordinates' in group_info['arrays'][ar]['attributes']
                    ):
                    the_o['coordinates'] = group_info['arrays'][
                        ar]['attributes']['coordinates'].split(' ')
                group_variables['variables'].append(the_o)
        if "groups" in group_info:
            for grp in group_info['groups']:
                #dealing with whitespace group names for HDFEOS (e.g. 'Group Fields'
                # 'DHFEOS INFORMATION', 'Data Fields') to be in gdal path
                the_sgrp = grp.replace(" ", "_")
                _the_group = f"{group}/{the_sgrp}"
                _the_group_info = group_info['groups'][grp]
                self._gdal_get_variables_with_dims_inner(
                    group_variables,
                    filename,
                    _the_group,
                    data_format,
                    _the_group_info
                )


    def _gdal_parse_variables_groups_from_dataset_name(
            self, dataset_name:str)->tuple:
        """
            @param dataset_name: 
                Examples - "/some/path/test.nc"
                    'NETCDF:"/some/pat/test.nc":variable1"
                    'NETCDF:"/some/pat/test.nc"://variable1"
                    'NETCDF:"/some/pat/test.nc"://group/variable1"
            return:
                (format, filename, groups, variable)
                For examples:
                ('', '', [], '')
                ('', "/some/path/test.nc", [], '')
                ('NETCDF', "/some/path/test.nc", [], 'variable1')
                ('NETCDF', "/some/path/test.nc", ['/'], 'variable1')
                ('NETCDF', "/some/path/test.nc", ['/', 'group'], 'variable1')
                
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

    def _gdal_extract_gv_path_from_dataset_name(
            self, dataset_name:str)->tuple:
        """
            Extract group/variable path
            @param dataset_name: 
                Examples - "/some/path/test.nc"
                    'NETCDF:"/some/pat/test.nc":variable1"
                    'NETCDF:"/some/pat/test.nc"://variable1"
                    'NETCDF:"/some/pat/test.nc"://group/variable1"
            return:
                group_variable_str with starting of '//'. '' returned if no group/variable.
                For examples:
                ''
                '//variable1'
                '//group/variable1'
                
        """
        (_the_format,
         _the_file,
         _the_groups,
         _the_var) = self._gdal_parse_variables_groups_from_dataset_name(dataset_name)
        return self._gdal_form_gv_path(_the_groups,_the_var)

    def _gdal_form_gv_path(self, groups:list, var_name:str)->str:
        if not var_name:
            return ''
        the_grp_str = '/'.join(groups)
        the_grp_str = the_grp_str.strip('/')
        if the_grp_str:
            the_ret = f'//{the_grp_str}/{var_name}'
        else:
            the_ret = f'//{var_name}'
        return the_ret
