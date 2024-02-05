"""
    Retrieve all variables and their units attributes in a dataset.
"""
import re
import json
import string
from osgeo import gdal

class DatasetVariableUnits:
    """
        This class is for testing:
            Consistent Units Attribute Value for Variables Across One Data Collection
    """
    def get_variable_units(self,dataset_name:str)->dict:
        """
            Retrieve all the variables and their units.
            @return: 
            {
                "name":"example.nc",
                "error":"message for error if error exists",
                "variables":[
                        {
                        "path": 'somevariable.nc',
                        "fullname":"//group1/variable1",
                        "name": "variable1",
                        "units":["mm"]
                        }
                    ]
            }
        """
        gdal.UseExceptions()
        _the_variables = self.get_variables(dataset_name)
        _the_variable_units = self._gdal_add_units_to_variables(
            _the_variables)
        return _the_variable_units

    def _gdal_add_units_to_variables(
            self,variables:dict)->dict:
        for _the_v in variables['variables']:
            self._gdal_add_units_to_one_variable(_the_v)
            _the_new_v = self._gdal_add_units_to_one_variable(_the_v)
        return variables
    
    def _gdal_add_units_to_one_variable(
            self, variable:dict)->dict:
        variable['units']=[]
        try:
            with gdal.Open(variable['path'], gdal.GA_ReadOnly) as the_ds:
                the_info = gdal.Info(the_ds, format="json")
                #the_info['bands'][0]['metadata']['']['units']
                if 'bands' not in the_info:
                    return variable
                if len(the_info['bands'])<1:
                    return variable
                for band in the_info['bands']:
                    if (('metadata' in band)
                        and ('' in band['metadata'])
                        and ('units' in band['metadata'][''])
                        ):
                        variable['units'].append(
                            band['metadata']['']['units'])
                    else:
                        variable['units'].append(None)
        except Exception as err:
            print("error: ", str(err))
        return variable

    def get_variables(self,dataset_name:str)->dict:
        """
            Retrieve all the variables.
            @return: 
            {
                "name":"example.nc",
                "error":"message for error if error exists",
                "variables":[
                    {
                        "path": 'NETCDF:"somefile.nc"://group1/variable1',
                        "fullname":"//group1/variable1",
                        "name":"variable1"}
                    ]
            }
        """
        gdal.UseExceptions()
        _the_variables = dict()
        _the_variables["name"] = dataset_name
        _the_variables["variables"] = set()
        # {"path":"fullpath-to-subdataset",
        #  "name":"variable1"}

        try:
            _the_info = None
            with gdal.Open(dataset_name, gdal.GA_ReadOnly) as _the_ds:
                if not isinstance(_the_ds, gdal.Dataset):
                    _the_variables["error"] = "Failed at opening the dataset."
                    return _the_variables

                _the_info = gdal.Info(_the_ds, format="json")

            if _the_info:
                self._gdal_get_variables(
                    _the_variables,
                    dataset_name,
                    _the_info
                )
            
        except Exception as err:
            _the_variables["error"]=str(err)
        
        #change the set to list
        _the_list = list(_the_variables['variables'])
        _the_new_list = list()
        for _it in _the_list:
            _the_new_list.append(json.loads(_it))
        _the_variables['variables'] = _the_new_list

        return _the_variables

    def _gdal_get_variables(
            self, group_variables:dict,
            dataset_name:str,
            dataset_info:dict):
        _the_ds_format, _the_ds_filename, _the_ds_gv = self._gdal_parse_dataset_name(
            dataset_name)
        #print("\n\n\nDATASET=",dataset_name, " gv=",_the_ds_gv)
        #if _the_ds_gv:
        self._gdal_get_variables_inner(group_variables, dataset_name, _the_ds_gv)

        _the_subdatasets = self._gdal_get_subdatasets(dataset_info)

        for ds_name in _the_subdatasets:
            _the_info = None
            with gdal.Open(ds_name, gdal.GA_ReadOnly) as _the_ds:
                if not isinstance(_the_ds, gdal.Dataset):
                    continue
                _the_info = gdal.Info(_the_ds, format="json")
            if _the_info:
                self._gdal_get_variables(
                    group_variables,ds_name,_the_info
                )
        #======This is too slow
        #self._gdal_get_non_dataset_variables(
        #    group_variables,
        #    _the_ds_format, _the_ds_filename, _the_ds_gv,
        #    dataset_info)
    
        self._gdal_try_to_add_coordinate_variables(
            group_variables,
            _the_ds_format, _the_ds_filename, _the_ds_gv,
            dataset_info
        )

    def _gdal_try_to_add_coordinate_variables(
            self, group_varables:dict,
            ds_format:str, ds_filename:str, ds_group_variable:str,
            dataset_info:dict):
        #the_info1['bands'][0]['metadata']['']['coordinates']
        if 'bands' not in dataset_info:
            return
        if len(dataset_info['bands'])<1:
            return
        # Just use the first band ?
        the_band1 = dataset_info['bands'][0]
        if (('metadata' in the_band1)
            and ('' in the_band1['metadata'])
            and ('coordinates' in the_band1['metadata'][''])
            ):
            _the_coords = re.split(',[ ]*|[ ]+',
                the_band1['metadata']['']['coordinates'].strip())
            for _the_c in _the_coords:
                self._gdal_test_and_add_variable(
                    group_varables,
                    ds_format, ds_filename, ds_group_variable,
                    _the_c.strip(), "")

    def _gdal_get_non_dataset_variables(
            self,group_varables:dict,
            ds_format:str, ds_filename:str, ds_group_variable:str,
            dataset_info):
        if "metadata" not in dataset_info:
            return
        if '' not in dataset_info["metadata"]:
            return
        for k in dataset_info["metadata"]['']:
            _the_group_path, _the_var=self._gdal_add_variable_from_metadata(k)
            if _the_var:
                self._gdal_test_and_add_variable(
                group_varables,
                ds_format, ds_filename, ds_group_variable,
                _the_var, _the_group_path)

    def _gdal_test_and_add_variable(
            self,group_variables:dict,
            ds_format:str, ds_filename:str, ds_group_variable:str,
            var_candidate:str,group_path:str):
        """
            This function actually trys to open the variable, which
            makes it very stlow.
        """
        try:
            _the_ds_format = ds_format
            if not _the_ds_format:
                with gdal.Open(ds_filename, gdal.GA_ReadOnly) as _the_ds:
                    _the_ds_format=_the_ds.GetDriver().ShortName.upper()
            _the_ds_group = ""
            if "/" in ds_group_variable.lstrip('/'):
                _dsgs = ds_group_variable.lstrip('/').rsplit("/",1)
                _the_ds_group = f"{_dsgs[0]}/"
            #post-processing on group
            _the_ds_group = _the_ds_group.strip(' |/')
            if len(_the_ds_group)>0:
                _the_ds_group = f"{_the_ds_group}/"

            #post-processing on group
            group_path = group_path.strip(' |/')
            if len(group_path)>0:
                group_path = f"{group_path}/"


            _the_test_ds = f'{_the_ds_format}:"{ds_filename}"://{_the_ds_group}{var_candidate}'
            if self._gdal_test_dataset(_the_test_ds):
                _the_var = dict()
                _the_var['path']=_the_test_ds
                _the_var['fullname']=f'//{_the_ds_group}{var_candidate}'
                _the_var['name']=var_candidate
                _the_var_jsonstr = json.dumps(_the_var)
                group_variables['variables'].add(_the_var_jsonstr)
            else:
                #2nd try with the path from metadata
                _the_test_ds = f'{_the_ds_format}:"{ds_filename}"://{group_path}{var_candidate}'
                if self._gdal_test_dataset(_the_test_ds):
                    _the_var = dict()
                    _the_var['path']=_the_test_ds
                    _the_var['fullname']=f'//{group_path}{var_candidate}'
                    _the_var['name']=var_candidate
                    _the_var_jsonstr = json.dumps(_the_var)
                    group_variables['variables'].add(_the_var_jsonstr)

        except Exception:
            #print("Error: ", str(err))
            pass


    def _gdal_test_dataset(self,dataset_name:str)->bool:
        try:
            with gdal.Open(dataset_name,gdal.GA_ReadOnly) as the_ds:
                if isinstance(the_ds, gdal.Dataset):
                    return True
            return False
        except Exception:
            #print("Warning:", str(err))
            return False

    def _gdal_add_variable_from_metadata(
            self, attribute_key:str):
        _the_parts = [attribute_key]
        if '#' in attribute_key:
            _the_parts = self._gdal_attribute_key_split(
                attribute_key, regex_pattern='#')
            if len(_the_parts)>1:
                print("attrib_key=", attribute_key)
                return attribute_key.split(_the_parts[-2])[0].replace('#',"/"), _the_parts[-2]
            else:
                return None, None
        else:
            _the_parts = self._gdal_attribute_key_split(
                attribute_key, regex_pattern='_')
            if len(_the_parts)>1:
                print("attrib_key=", attribute_key)
                return attribute_key.split(_the_parts[-2])[0].replace('_',"/"), _the_parts[-2]
            else:
                return None, None

    def _gdal_get_variables_inner(
            self,group_variables:dict,
            dataset_name:str,
            group_variable_name:str):
        if '/' in group_variable_name:
            _the_strs = group_variable_name.rsplit('/', 1)
            _the_var = dict()
            _the_var['path']=dataset_name
            _the_var['fullname']=group_variable_name
            _the_var['name']=_the_strs[1]
        else:
            _the_var = dict()
            _the_var['path']=dataset_name
            _the_var['fullname']=group_variable_name
            _the_var['name']=group_variable_name
        _the_var_jsonstr = json.dumps(_the_var)
        group_variables['variables'].add(_the_var_jsonstr)



    def _gdal_parse_dataset_name(self, dataset_name:str)->tuple:
        """
            return:
            (format, filename, group_variable)
            Empty string will be the fill value for each field.
        """
        _the_format = ''
        _the_filename = ''
        _the_group_variable = ''
        if dataset_name is None:
            return _the_format, _the_filename, _the_group_variable
        if ':"' in dataset_name:
            _the_strs = dataset_name.split(':"', 1)
            _the_format = _the_strs[0]
            if '":' in _the_strs[1]:
                _the_strs2 = _the_strs[1].rsplit('":', 1)
                _the_filename = _the_strs2[0]
                _the_group_variable = _the_strs2[1]
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
        return _the_format, _the_filename, _the_group_variable

    def _gdal_get_subdatasets(self, dataset_info):
        _the_ret = []
        if "metadata" not in dataset_info:
            return _the_ret
        if "SUBDATASETS" not in dataset_info["metadata"]:
            return _the_ret
        _sd_keys = [k for k in dataset_info[
            "metadata"]["SUBDATASETS"] if "_NAME" in k]
        _the_ret = [dataset_info["metadata"][
            "SUBDATASETS"][k] for k in _sd_keys]
        return _the_ret


    def _gdal_attribute_key_split(
            self, attribute_key:str, regex_pattern:str='_')->list:
        """
            Break a attribute key by split with '_' or '#'.
            If '__' will be separated by first '_' and the rest will be
            kept as prefix for the second part. For example,
            "MS_G2_precipRateLocalTime_count__FillValue" ->
            ["MS","G2","precipRateLocalTime","count","_FillValue"] 
        """
        _the_ret = []
        _str = attribute_key
        while len(_str) > 0:
            #_ss = re.split('#|_', _str[1:], 1)
            _skip_str, _skip_index = self._gdal_attribute_key_skip_index(_str,regex_pattern)
            _ss = re.split(regex_pattern, _str[_skip_index:], 1)
            if len(_ss) <= 1 :
                _the_ret.append(_str)
                _str = ''
                break
            elif len(_ss[1]) <= 1 :
                _the_ret.append(_str)
                _str = ''
                break
            else:
                _the_ret.append(f"{_skip_str}{_ss[0]}")
                _str = _ss[1]
        return _the_ret

    def _gdal_attribute_key_skip_index(self,attribute_key:str, regex_pattern:str='_')->tuple:
        """
            return:
            prefix, skip_index
        """
        if not attribute_key:
            return 0
        _index = 0
        _loop = True
        _str = attribute_key
        _prefix = ''
        while _loop:
            _the_strs = re.split(regex_pattern, _str, 1)
            if len(_the_strs[0]) == 0:
                _index +=1
                _prefix += _str[0:1]
                _str = _str[1:]
            else:
                _loop = False
                break
        return _prefix, _index
