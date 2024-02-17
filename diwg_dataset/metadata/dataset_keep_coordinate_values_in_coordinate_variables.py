"""
    Retrieve all groups, variables, attributes
      and their coordinate attributes in a dataset.
    
"""
import re
import json
import string
import copy
from dateparser.search import search_dates
from osgeo import gdal

class DatasetKeepCoordValuesInCoordVariables:
    """
        This class is for testing:
            Keep Coordinate Values in Coordinate Variables
    """
    def get_coordinates_values_in_groups_variables_attributes(
            self,dataset_name:str)->dict:
        """
            Retrieve all coordinates and find its location in groups, variables, or attributes.
            This function utilizes gdalmdiminfo to retrieve groups, variables, attributes,
             which should only work with dataset with multi-dimensional arrays, 
             i.e. netcdf, hdf, hdfeos.
            @return: 
            {
                "dataset_name":"example.nc",
                "error":"message for error if error exists",
                "coords_in_groups":[
                        {
                            "fullpath":"/group1",
                            "parent_path":["","group1"],
                            "type":"group",
                            "name":"coord3"}
                    ]
                    ],
                "coords_not_in_variables":[
                        {
                            "fullpath":"/group1/variable1",
                            "parent_path":["","group1","variable1"],
                            "type":"attribute",
                            "name":"coord2"},
                        {
                            "fullpath":"/group1",
                            "parent_path":["","group1"],
                            "type":"group",
                            "name":"coord3"}
                        ]
                    ],
                "coords_in_attributes":[
                        {
                            "fullpath":"/group1/variable1",
                            "parent_path":["","group1","variable1"],
                            "type":"attribute",
                            "name":"coord2"}
                    ],
                "coordinates":[
                        {
                            "fullpath":"/group1",
                            "parent_path":["","group1"],
                            "type":"variable",
                            "name":"coord1"},
                        {
                            "fullpath":"/group1/variable1",
                            "parent_path":["","group1","variable1"],
                            "type":"attribute",
                            "name":"coord2"},
                        {
                            "fullpath":"/group1",
                            "parent_path":["","group1"],
                            "type":"group",
                            "name":"coord3"}
                    ]
            }
        """
        _gva_coords = dict()
        _gva_coords["dataset_name"] = dataset_name
        _gva_coords["coords_in_groups"] = list()
        _gva_coords["coords_not_in_variables"] = list()
        _gva_coords["coords_in_attributes"] = list()
        _gva_coords["coordinates"] = list()
        grp_var_attrs = self.get_groups_variables_attributes_and_coordinates(dataset_name)
        _gva_coords['coordinates'] = grp_var_attrs['coordinates']
        if 'error' in grp_var_attrs:
            _gva_coords['error'] = grp_var_attrs['error']
            return _gva_coords
        _gva_coords['coords_in_groups'] = [k for k in grp_var_attrs[
            'coordinates'] if k['type'] == 'group']
        _gva_coords['coords_not_in_variables'] = [k for k in grp_var_attrs[
            'coordinates'] if k['type'] != 'variable']
        _gva_coords['coords_in_attributes'] = [k for k in grp_var_attrs[
            'coordinates'] if k['type'] == 'attribute']
        self._scan_groups_for_date_time(
            grp_var_attrs,_gva_coords)
        return _gva_coords

    def _scan_groups_for_date_time(
            self, grp_var_attrs:dict,
            gva_coords):
        """
            Scan group for date/time in certain format.
            Used dateparser to search for dates.
        """
        _time_coords = [k for k in gva_coords[
            'coordinates'] if k['name'].lower() == 'time']
        if len(_time_coords) > 0:
            return
        for grp in grp_var_attrs['groups']:
            the_f_path = copy.deepcopy(grp['fullpath'])
            the_f_path.replace('/', " ").replace("_", " ")
            times = search_dates(the_f_path)
            if not times:
                continue
            the_o = dict()
            the_o['fullpath'] = grp['fullpath']
            the_o['parent_path'] = grp['parent_path']
            the_o['type'] = 'group_detected'
            the_o['name'] = grp['name']
            if the_o not in gva_coords:
                gva_coords.append(the_o)

    def get_groups_variables_attributes_and_coordinates(
            self,dataset_name:str)->dict:
        """
            Retrieve all groups, variables, and attributes.
            This function utilizes gdalmdiminfo to retrieve groups, variables, attributes,
             which should only work with dataset with multi-dimensional arrays, 
             i.e. netcdf, hdf, hdfeos.
            @return: 
            {
                "dataset_name":"example.nc",
                "error":"message for error if error exists",
                "groups":[
                    {
                        "fullpath":"/group1",
                        "parent_group":["","group1"],
                        "name":"group11"},
                    {
                        "fullpath":"",
                        "parent_group":[],
                        "name":"group1"}
                    ],
                "variables":[
                    {
                        "fullpath":"/group1/variable1",
                        "parent_group":["","group1"],
                        "name":"variable1"},
                    {
                        "fullpath":"",
                        "parent_group":[],
                        "name":"variable0"}
                    ],
                "attributes":[
                    {
                        "fullpath":"/group1",
                        "parent_path":["","group1"],
                        "variable":"variable1",
                        "name":"attribute1"},
                    {
                        "fullpath":"/group1",
                        "parent_path":["","group1"]
                        "name":"attribute2"}
                    {
                        "fullpath":"",
                        "parent_group":[]
                        "name":"attribute0"}
                    ],
                "coordinates":[
                    {
                        "fullpath":"/group1",
                        "parent_path":["","group1"],
                        "type":"variable",
                        "name":"coord1"},
                    {
                        "fullpath":"/group1/variable1",
                        "parent_path":["","group1","variable1"],
                        "type":"attribute",
                        "name":"coord2"},
                    {
                        "fullpath":"/group1",
                        "parent_path":["","group1"],
                        "type":"group",
                        "name":"coord3"}
                    ]
            }
        """
        gdal.UseExceptions()
        _grp_var_attrs = dict()
        _grp_var_attrs["dataset_name"] = dataset_name
        _grp_var_attrs["groups"] = list()
        _grp_var_attrs["variables"] = list()
        _grp_var_attrs["attributes"] = list()
        _grp_var_attrs["coordinates"] = list()
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
                self._gdal_extract_groups_variables_attributes(
                    _grp_var_attrs,
                    _the_md_info
                )
            # search all coordinate if coordinates exist for each variable
            # (for netcdf)
            self._gdal_extract_coordinates(
                _grp_var_attrs,_the_md_info)
            # scan for potential coordinates (i.e. lat, lon, time, latitude, longitutde)
            if len(_grp_var_attrs['coordinates']) < 1:
                self._gdal_scan_coordinates(
                    _grp_var_attrs,_the_md_info)

            #self._gdal_find_and_add_time_variables(_the_variables)
            #_the_vars = _the_variables['variables']
            #_the_variables['variables'] = [k for k in _the_vars if k[
            #    'fullname'].startswith(_gv_str)]
            #self._gdal_verify_variable_include_time_coord(_the_variables)

        except Exception as err:
            _grp_var_attrs["error"]=str(err)
        return _grp_var_attrs

    def _gdal_scan_coordinates(
            self, grp_var_attrs:dict,
            dataset_info:dict):
        _candidate_coordinates = ['lat',
                                  'latitude',
                                  'lon',
                                  'longitude',
                                  'time']
        for crd in _candidate_coordinates:
            the_coords = self._gdal_scan_coordinates_attributes(
                grp_var_attrs,crd)
            for c in the_coords:
                if c not in grp_var_attrs['coordinates']:
                    grp_var_attrs['coordinates'].append(c)
            the_coords = self._gdal_scan_coordinates_variables(
                grp_var_attrs,crd)
            for c in the_coords:
                if c not in grp_var_attrs['coordinates']:
                    grp_var_attrs['coordinates'].append(c)
            the_coords = self._gdal_scan_coordinates_groups(
                grp_var_attrs,crd)
            for c in the_coords:
                if c not in grp_var_attrs['coordinates']:
                    grp_var_attrs['coordinates'].append(c)

    def _gdal_scan_coordinates_attributes(
            self, grp_var_attrs:dict,
            coord_name:str)->list:
        """
            {
                "fullpath":"/group1/variable1",
                "parent_path":["","group1","variable1"],
                "type":"attribute",
                "name":"coord2"},
        """
        the_ret = list()
        coord_name_l = coord_name.lower()
        for att in grp_var_attrs['attributes']:
            if att['name'].lower() == coord_name_l:
                the_o = dict()
                the_f_path = att['fullpath']
                the_p_path = att['parent_path']
                if 'variable' in att:
                    the_var = att['variable']
                    the_f_path = f'{the_f_path}/{the_var}'
                    the_p_path.append(the_var)
                the_o['fullpath'] = the_f_path
                the_o['parent_path'] = the_p_path
                the_o['name'] = att['name']
                the_o['type'] = 'attribute'
                the_ret.append(the_o)
        return the_ret

    def _gdal_scan_coordinates_variables(
            self, grp_var_attrs:dict,
            coord_name:str):
        """
            {
                "fullpath":"/group1",
                "parent_path":["","group1"],
                "type":"variable",
                "name":"coord2"},
        """
        coord_name_l = coord_name.lower()
        the_ret = list()
        for c_var in grp_var_attrs['variables']:
            if c_var['name'].lower() == coord_name_l:
                the_o = dict()
                the_o['fullpath'] = c_var['fullpath']
                the_o['parent_path'] = c_var['parent_path']
                the_o['name'] = c_var['name']
                the_o['type'] = 'variable'
                the_ret.append(the_o)
        return the_ret

    def _gdal_scan_coordinates_groups(
            self, grp_var_attrs:dict,
            coord_name:str):
        """
            {
                "fullpath":"/group1",
                "parent_path":["","group1"],
                "type":"group",
                "name":"coord2"},
        """
        the_ret = list()
        coord_name_l = coord_name.lower()
        for c_grp in grp_var_attrs['groups']:
            if c_grp['name'].lower() == coord_name_l:
                the_o = dict()
                the_o['fullpath'] = c_grp['fullpath']
                the_o['parent_path'] = c_grp['parent_path']
                the_o['name'] = c_grp['name']
                the_o['type'] = 'group'
                the_ret.append(the_o)
        return the_ret


    def _gdal_extract_coordinates(
            self, grp_var_attrs:dict,
            dataset_info:dict):
        for att in grp_var_attrs['attributes']:
            # only look at 'coordinates' under variable ?
            if 'variable' not in att:
                continue
            if att['name'] != 'coordinates':
                continue
            # retrieve the value of 'coordinates'
            the_coords = self._gdal_retrieve_attribute_value_from_multidim_info(
                grp_var_attrs,
                dataset_info, att)
            for c in the_coords:
                if c not in grp_var_attrs['coordinates']:
                    grp_var_attrs['coordinates'].append(c)

    def _gdal_retrieve_attribute_value_from_multidim_info(
            self, grp_var_attrs:dict,
            dataset_info:dict, attr:dict)->list[dict]:
        """
            return:
                    [
                    {
                        "fullpath":"/group1",
                        "parent_path":["","group1"],
                        "name":"coord1"}
                    ]
        """
        the_info = dataset_info
        the_p = attr['parent_path']
        the_ret = list()
        # Under root
        #if len(the_p) == 0:
        #    return dataset_info['attributes'][attr['name']]
        # skip root
        if len(the_p) > 0:
            if the_p[0] == "":
                the_p = the_p[1:]
        for g in the_p:
            the_info = the_info['groups'][g]
        if 'variable' in attr:
            the_info = the_info['arrays'][attr['variable']]
        the_coords_str = the_info['attributes'][attr['name']]
        the_coords = the_coords_str.split(" ")
        for c in the_coords:
            the_c  = c.strip()
            if not the_c:
                continue
            the_cs = the_c.split('/')
            the_c_fullpath = ""
            the_c_parent_path = list()
            the_c_parent_path.append('')
            # if not from root, use the relative path to attr
            if the_cs[0] != '':
                the_c_fullpath = attr['fullpath']
                the_c_parent_path = attr['parent_path']
            else:
                the_cs = the_cs[1:]
            if len(the_cs) < 1:
                continue
            the_c_name = the_cs[-1]
            the_cs = the_cs[:-1]
            for p_c in the_cs:
                the_p_c = p_c.replace(' ','_') # for gdal
                the_c_fullpath = f"{the_c_fullpath}/{the_p_c}"
                the_c_parent_path.append(p_c)
            the_c_o = self._gdal_find_type_and_form_coordinate(
                grp_var_attrs,the_c_fullpath,
                the_c_parent_path, the_c_name
            )
            #the_c_o['fullpath'] = the_c_fullpath
            #the_c_o['parent_path'] = the_c_parent_path
            #the_c_o['name'] = the_c_name
            the_ret.append(the_c_o)
        return the_ret
    
    def _gdal_find_type_and_form_coordinate(
            self, grp_var_attrs:dict,
            fullpath:str, parent_path:list,
            coord_name:str)->dict:
        the_att_coords = self._gdal_scan_coordinates_attributes(
            grp_var_attrs,coord_name)
        the_var_coords = self._gdal_scan_coordinates_variables(
            grp_var_attrs,coord_name)
        the_grp_coords = self._gdal_scan_coordinates_groups(
            grp_var_attrs,coord_name)
        the_coords = list()
        the_coords.extend(the_att_coords)
        the_coords.extend(the_var_coords)
        the_coords.extend(the_grp_coords)
        the_ret = self._gdal_select_the_best_match_coordinate(
            the_coords, fullpath, parent_path,
            coord_name)
        if the_ret is None:
            the_ret = dict()
            the_ret['fullpath'] = fullpath
            the_ret['parent_path'] = parent_path
            the_ret['name'] = coord_name
            the_ret['type'] = ""
        return the_ret

    def _gdal_select_the_best_match_coordinate(
            self,coords:list,
            fullpath:str, parent_path:str,
            coord_name:str)->dict:
        if len(coords)<1:
            return None
        s_coords = [k for k in coords if k[
            'fullpath'] == fullpath and k[
                'name'] == coord_name]
        if len(s_coords)>0:
            return s_coords[0]
        s_coords = [k for k in coords if k[
            'fullpath'].startswith(fullpath) and k[
                'name'] == coord_name]
        if len(s_coords)>0:
            return s_coords[0]
        s_coords = [k for k in coords if k[
            'fullpath'].startswith(fullpath)]
        if len(s_coords)>0:
            return s_coords[0]
        return None

    def _gdal_extract_groups_variables_attributes(
            self, grp_var_attrs:dict,
            dataset_info:dict):
        if "attributes" in dataset_info:
            for att in dataset_info['attributes']:
                the_o = dict()
                the_o['fullpath'] = ""
                the_o['parent_path'] = []
                the_o['name'] = att
                grp_var_attrs['attributes'].append(the_o)
        if "arrays" in dataset_info:
            for ar in dataset_info['arrays']:
                the_o = dict()
                the_o['fullpath'] = ""
                the_o['parent_path'] = []
                the_o['name'] = ar
                grp_var_attrs['variables'].append(the_o)
                ar_v = dataset_info['arrays'][ar]
                if 'attributes' in ar_v:
                    for att in ar_v['attributes']:
                        the_o = dict()
                        the_o['fullpath'] = ""
                        the_o['parent_path'] = []
                        the_o['variable'] = ar
                        the_o['name'] = att
                        grp_var_attrs['attributes'].append(the_o)

        if "groups" in dataset_info:
            for grp in dataset_info['groups']:
                the_o = dict()
                the_o['fullpath'] = ""
                the_o['parent_path'] = []
                the_o['name'] = grp
                grp_var_attrs['groups'].append(the_o)
                # dig in sub-group
                the_grp_info = dataset_info['groups'][grp]
                the_grp_4_gdal = grp.replace(" ","_")
                the_c_path = f"/{the_grp_4_gdal}"
                the_c_grp = list(["",grp])
                self._gdal_extract_groups_variables_attributes_inner(
                    grp_var_attrs=grp_var_attrs,
                    group_info=the_grp_info,
                    parent_path=the_c_path,
                    parent_group=the_c_grp
                )

    def _gdal_extract_groups_variables_attributes_inner(
            self, grp_var_attrs:dict,
            group_info:dict,
            parent_path:str,
            parent_group:list):
        if "attributes" in group_info:
            for att in group_info['attributes']:
                the_o = dict()
                the_o['fullpath'] = parent_path
                the_o['parent_path'] = parent_group
                the_o['name'] = att
                grp_var_attrs['attributes'].append(the_o)
        if "arrays" in group_info:
            for ar in group_info['arrays']:
                the_o = dict()
                the_o['fullpath'] = parent_path
                the_o['parent_path'] = parent_group
                the_o['name'] = ar
                grp_var_attrs['variables'].append(the_o)
                ar_v = group_info['arrays'][ar]
                if 'attributes' in ar_v:
                    for att in ar_v['attributes']:
                        the_o = dict()
                        the_o['fullpath'] = parent_path
                        the_o['parent_path'] = parent_group
                        the_o['variable'] = ar
                        the_o['name'] = att
                        grp_var_attrs['attributes'].append(the_o)
        if "groups" in group_info:
            for grp in group_info['groups']:
                the_o = dict()
                the_o['fullpath'] = parent_path
                the_o['parent_path'] = parent_group
                the_o['name'] = grp
                grp_var_attrs['groups'].append(the_o)
                # recursively dig in sub-group
                the_grp_info = group_info['groups'][grp]
                the_grp_4_gdal = grp.replace(" ","_")
                the_c_path = f"{parent_path}/{the_grp_4_gdal}"
                the_c_grp = copy.deepcopy(parent_group)
                the_c_grp.append(grp)
                self._gdal_extract_groups_variables_attributes_inner(
                    grp_var_attrs,
                    the_grp_info,
                    the_c_path,
                    the_c_grp
                )

    def _gdal_parse_variables_groups_from_dataset_name(
            self, dataset_name:str)->tuple:
        """
            @param dataset_name: 
                Examples - "/some/path/test.nc"
                    'NETCDF:"/some/pat/test.nc":variable1"
                    'NETCDF:"/some/pat/test.nc":/variable1"
                    'NETCDF:"/some/pat/test.nc":/group/variable1"
            return:
                (format, filename, groups, variable)
                For examples:
                ('', '', [], '')
                ('', "/some/path/test.nc", [], '')
                ('NETCDF', "/some/path/test.nc", [], 'variable1')
                ('NETCDF', "/some/path/test.nc", [""], 'variable1')
                ('NETCDF', "/some/path/test.nc", ["", 'group'], 'variable1')
                
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

    def _gdal_form_gv_path(self, groups:list, var_name:str)->str:
        """
            Consistently return fullpath starting with single '/'.
            i.e. '/group1/var1', '/var1'
            empty variable: ''
        """
        if not var_name:
            return ''
        the_grp_str = '/'.join(groups)
        the_grp_str = the_grp_str.strip('/')
        if the_grp_str:
            the_ret = f'/{the_grp_str}/{var_name}'
        else:
            the_ret = f'/{var_name}'
        return the_ret

