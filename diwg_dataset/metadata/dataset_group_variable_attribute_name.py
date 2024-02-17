"""
    Retrieve all names of groups, variables, and attributes in a dataset.
"""
import re
import string
from osgeo import gdal

class DatasetGroupVariableAttributeName:
    """
        This class is for testing:
            Character Set for User-Defined Group, Variable, and Attribute Names
    """
    def get_group_variable_attribute_names(self,dataset_name:str)->dict:
        """
            Retrieve the metadata.
            @return: 
            {
                "dataset_name":"example.nc",
                "error":"message for error if error exists",
                "group_names":["group1", "2group"],
                "variable_names":["var1", "var-2"],
                "attribute_names":["attr1", "attr_2"]
            }
        """
        gdal.UseExceptions()
        _the_ret_gva_names = dict()
        _the_ret_gva_names["dataset_name"] = dataset_name
        _the_g_names = set()
        _the_ret_gva_names["group_names"] = _the_g_names
        _the_v_names = set()
        _the_ret_gva_names["variable_names"] = _the_v_names
        _the_a_names = set()
        _the_ret_gva_names["attribute_names"] = _the_a_names

        try:
            with gdal.Open(dataset_name, gdal.GA_ReadOnly) as _the_ds:
                if not isinstance(_the_ds, gdal.Dataset):
                    _the_ret_gva_names["error"] = "Failed at opening the dataset."
                    return _the_ret_gva_names

                _the_info = gdal.Info(_the_ds, format="json")

                self._gdal_get_group_variable(
                    _the_ret_gva_names,
                    dataset_name,_the_info
                )
        except Exception as err:
            _the_ret_gva_names["error"]=str(err)

        return _the_ret_gva_names

    def _gdal_get_group_variable(
            self, group_varable_attribute:dict,
            dataset_name:str, dataset_info):
        _the_ds_format, _the_ds_filename, _the_ds_gv = self._gdal_parse_dataset_name(
            dataset_name)
        if _the_ds_gv:
            self._gdal_get_group_variable_inner(group_varable_attribute, _the_ds_gv)
        # loop through all subdatasets
        _the_subdatasets = self._gdal_get_subdatasets(dataset_info)

        for ds_name in _the_subdatasets:
            _the_ds = gdal.Open(ds_name, gdal.GA_ReadOnly)
            if not isinstance(_the_ds, gdal.Dataset):
                continue
            _the_info = gdal.Info(_the_ds, format="json")
            self._gdal_get_group_variable(
                group_varable_attribute,ds_name,_the_info
            )
        self._gdal_get_all_attribute_names(
            group_varable_attribute,
            dataset_info)

    def _gdal_get_all_attribute_names(
            self,group_varable_attribute:dict,
            dataset_info):
        if "metadata" not in dataset_info:
            return
        if '' not in dataset_info["metadata"]:
            return
        for k in dataset_info["metadata"]['']:
            self._gdal_add_one_attribute(
                group_varable_attribute,
                k, dataset_info["metadata"][''][k])

    def _gdal_add_one_attribute(
            self, group_varable_attribute:dict,
            attribute_key:str, attribute_value:str):
        _the_parts = [attribute_key]
        if '#' in attribute_key:
            _the_parts = self._gdal_attribute_key_split(
                attribute_key, regex_pattern='#')
        else:
            _the_parts = self._gdal_attribute_key_split(
                attribute_key, regex_pattern='_')
        _the_values = self._gdal_attribute_value_parse(
            attribute_value)
        if len(_the_values)>0:
            for _v in _the_values:
                group_varable_attribute["attribute_names"].add(_v)
            if len(_the_parts)>0:
                group_varable_attribute["variable_names"].add(
                    _the_parts[-1])
            if len(_the_parts)>1:
                for _pv in _the_parts[:-2]:
                    group_varable_attribute["group_names"].add(_pv)
        else:
            if len(_the_parts)>0:
                group_varable_attribute["attribute_names"].add(
                    _the_parts[-1])
            if len(_the_parts)>1:
                group_varable_attribute["variable_names"].add(
                    _the_parts[-2])
            if len(_the_parts)>2:
                for _pv in _the_parts[:-3]:
                    group_varable_attribute["group_names"].add(_pv)

    def _gdal_attribute_value_parse(
        self, attribute_value:str,
        prop_sep:str=';\n',
        prop_value_sep:str='=')->list:

        _str = attribute_value
        _ss = _str.split(prop_sep)
        _the_ret = list()

        for _s in _ss:
            if not _s:
                continue
            _s_s = _s.split(prop_value_sep,1)
            if len(_s_s) != 2:
                return list()
            if (len(_ss) == 1 and
                self._gdal_non_attribute_name_has_special_prefix(
                    _s_s[0])):
                return list()
            if self._gdal_attribute_name_has_whitespace(_s_s[0]):
                return list()
            _the_ret.append(_s_s[0])
        return _the_ret

    def _gdal_attribute_name_has_whitespace(
            self, attribute_name:str)->bool:
        return any([c in attribute_name for c in string.whitespace])        

    def _gdal_non_attribute_name_has_special_prefix(
            self, attribute_name:str, prefix:str = "^[+]")->bool:
        _the_p = re.compile(prefix)
        if _the_p.match(attribute_name):
            return True
        return False

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

    def _gdal_get_group_variable_inner(
            self,group_varable_attribute:dict,
            group_variable_name:str):
        if '/' in group_variable_name:
            _the_strs = group_variable_name.rsplit('/', 1)
            group_varable_attribute["variable_names"].add(_the_strs[1])
            _the_strs2 = _the_strs[0].split('/')
            for g in _the_strs2:
                if g:
                    group_varable_attribute["group_names"].add(g)
        else:
            group_varable_attribute["variable_names"].add(group_variable_name)

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
