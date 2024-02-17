"""
    For recommendation:
    Include Georeference Information with Geospatial Coordinates

    Retrieve grid variables and check its grid_mapping/wkt info
    in a grid dataset.

"""
import re
import string
from osgeo import gdal

class DatasetIncludeGeoreferenceInformation:
    """
        This class is for testing:
            Include Georeference Information with Geospatial Coordinates

            https://wiki.earthdata.nasa.gov/display/ESDSWG/Include+Georeference+Information+with+Geospatial+Coordinates
    """
    def get_variables(self,dataset_name:str)->dict:
        """
            Retrieve the metadata.
            @return: 
            {
                "dataset_name":"example.nc",
                "error":"message for error if error exists",
                "variables":[
                        {
                            "fullpath":"/group1",
                            "parent_group":["","group1"],
                            "has_grid_mapping":True,
                            "has_grid_mapping_name":True,
                            "has_crs_wkt": True,
                            "name":"variable1"},
                        {
                            "fullpath":"/group_g2",
                            "parent_group":["","group g2"],
                            "has_grid_mapping":True,
                            "has_grid_mapping_name":True,
                            "has_crs_wkt": True,
                            "name":"variable2"},
                        {
                            "fullpath":"",
                            "parent_group":[],
                            "has_grid_mapping":False,
                            "has_grid_mapping_name":False,
                            "has_crs_wkt": False,
                            "name":""},
                        {
                            "fullpath":"",
                            "parent_group":[],
                            "has_grid_mapping":True,
                            "has_grid_mapping_name":True,
                            "has_crs_wkt": True,
                            "name":"variable0"}
                        ]
                    ]
            }
        """
        gdal.UseExceptions()
        _the_variables = dict()
        _the_variables["dataset_name"] = dataset_name
        _the_variables["variables"] = list()

        try:
            _the_info = gdal.Info(dataset_name, format="json",
                                  listMDD=True,extraMDDomains=['all'],
                                  reportProj4=True)

            self._gdal_get_variables(
                _the_variables,
                dataset_name,_the_info)
        except Exception as err:
            _the_variables["error"]=str(err)

        return _the_variables

    def _gdal_get_variables(
        self, g_variables:dict,
        dataset_name:str,
        dataset_info:dict):
        """
            @g_variables:
            {
                "dataset_name":"example.nc",
                "error":"message for error if error exists",
                "variables":[
                        {
                            "fullpath":"/group1",
                            "parent_group":["","group1"],
                            "has_grid_mapping":True,
                            "has_grid_mapping_name":True,
                            "has_crs_wkt": True,
                            "name":"variable1"},
                        {
                            "fullpath":"/group_g2",
                            "parent_group":["","group g2"],
                            "has_grid_mapping":True,
                            "has_grid_mapping_name":True,
                            "has_crs_wkt": True,
                            "name":"variable2"},
                        {
                            "fullpath":"",
                            "parent_group":[],
                            "has_grid_mapping":False,
                            "has_grid_mapping_name":False,
                            "has_crs_wkt": False,
                            "name":""},
                        {
                            "fullpath":"",
                            "parent_group":[],
                            "has_grid_mapping":True,
                            "has_grid_mapping_name":True,
                            "has_crs_wkt": True,
                            "name":"variable0"}
                        ]
                    ]
            }
            Note: 'fullpath' - string represenation of parent path useful for gdal where
                            space in group may replaced with "_".
                   'parent_group' - a list of parent groups.
        """
        (_the_format,
        _the_file,
        _the_groups,
        _the_var
         ) = self._gdal_parse_variables_groups_from_dataset_name(
            dataset_name)
        _grp_str = self._gdal_form_gv_path(_the_groups,_the_var)
        if not ('bands' not in dataset_info
            or not dataset_info['bands']):
            the_o = dict()
            the_o['fullpath'] = "/".join(_the_groups)
            the_o['parent_path'] = _the_groups
            the_o['name'] = _the_var
            (_has_grid_mapping,
             _has_wkt,
             _has_grid_mapping_name) = self._gdal_check_grid_mapping_wkt(
                dataset_info,the_o)
            the_o['has_grid_mapping'] = _has_grid_mapping
            the_o['has_grid_mapping_name'] = _has_grid_mapping_name
            the_o['has_crs_wkt'] = _has_wkt
            if the_o not in g_variables['variables']:
                g_variables['variables'].append(the_o)
            

        # loop through all subdatasets
        _the_subdatasets = self._gdal_get_subdatasets(dataset_info)
        for ds_name in _the_subdatasets:
            _the_info = gdal.Info(ds_name, format="json",
                                listMDD=True,extraMDDomains=['all'],
                                reportProj4=True)
            self._gdal_get_variables(
                g_variables,ds_name,_the_info
            )

    def _gdal_check_grid_mapping_wkt(
            self, dataset_info:dict,
            var_obj:dict)->tuple:
        """
            @return
            (<exist-grid-mapping, <provide-wkt>, <has-grid-mapping-name>)
        """
        _has_grid_mapping = False
        _has_wkt = False
        _has_grid_mapping_name = False
        if ('bands' not in dataset_info or
            not dataset_info['bands']):
            return (_has_grid_mapping, _has_wkt)

        # using band 1 to extract info
        band1 = dataset_info['bands'][0]
        band1_meta = dict()
        if 'metadata' in band1:
            band1_meta = band1['metadata']
        if '' in band1_meta:
            band1_meta = band1_meta['']

        if ("grid_mapping" not in band1_meta
            or not band1_meta['grid_mapping']):
            return (_has_grid_mapping, _has_wkt)
        _has_grid_mapping = True
        _gm_var_name = band1_meta['grid_mapping']

        # find the variable and get its attributes
        meta_info = dict()
        if 'metadata' in dataset_info:
            meta_info = dataset_info['metadata']
        if '' in meta_info:
            meta_info = meta_info['']
        _gm_var = self._gdal_ret_attributes_for_var(
            meta_info,
            var_obj,_gm_var_name)
        # Check if 'grid_mapping_name" in: not valid grid_mapping 
        # possibly not grid data???)
        if _gm_var:
            if 'crs_wkt' in _gm_var:
                _has_wkt = True
            if 'grid_mapping_name' in _gm_var:
                _has_grid_mapping_name = True
        return (_has_grid_mapping, _has_wkt, _has_grid_mapping_name)

    def _gdal_ret_attributes_for_var(
            self,meta_data:dict,
            var_obj:dict,
            search_var_name:str,
            sep_str:str='#')->dict:
        """
            Paramters:
                meta_data(dict): one level dict
                var_obj(dict): variable object
                search_var_name(str): grid_mapping variable name
                sep_str(str): Speartor used in gdalinfo. Netcdf, '#', others: '_'.
        """        
        the_ret = dict()
        if not search_var_name:
            return the_ret
        _search_var_name = search_var_name
        # ??? May need to look for the var by getting the info for the proper parent 
        # sub-dataset if teh search variable name starts with '/'
        if not _search_var_name.startswith('/'):
            _var_fullpath = var_obj['fullpath']
            if _var_fullpath:
                _search_var_name = f'{_var_fullpath}/{search_var_name}'
        _search_var_name = f'{_search_var_name}{sep_str}'
        for k in meta_data:
            if k.startswith(_search_var_name):
                att_value = meta_data[k]
                att_name = k.split(_search_var_name,1)[1]
                the_ret[att_name] = att_value
        return the_ret

    def _gdal_get_subdatasets(self, dataset_info:dict)->list:
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
                (format, filename, groups, variable)
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

    def _gdal_form_gv_path(self, groups:list, var_name:str)->str:
        """
            Consistently return fullpath starting with single '/'.
            i.e. '/group1/var1', '/var1'
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
