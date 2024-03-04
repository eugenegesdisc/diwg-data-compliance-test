"""
    For recommendation:

    Adopt Semantically Rich Dataset Release Identifiers

    Partition filename and verify completeness of crid (major, minor, and patch)

"""
import re
import os

class FilenameDatasetAdoptSemanticallyRichDatasetReleaseIdentifiers:
    """
        This class is for testing:
            Adopt Semantically Rich Dataset Release Identifiers

            https://wiki.earthdata.nasa.gov/display/ESDSWG/Adopt+Semantically+Rich+Dataset+Release+Identifiers
    """
    def valid_dataname_crid_partitions(self,
                                dataset_name:str,
                                dataset_crid:str=None,
                                dataset_crid_major:str=None,
                                dataset_crid_major_group:str="major",
                                dataset_crid_minor:str=None,
                                dataset_crid_minor_group:str="major",
                                dataset_crid_patch:str=None,
                                dataset_crid_patch_group:str="patch")->dict:
        """
            Get filename exteion for the dataset.
            @param dataset_name: Full path to a granuale file.
            @param dataset_crid: a unique identifier for each release (version, collection)
                of the dataset or a unique Combined Release ID or a regex expression for such 
                id to be extracted from the filename or to be matched in the filename.
            @param dataset_crid_major: Regex pattern to retrieve the major version from the
                composite release id string extracted using dataset_crid. 
            @param dataset_crid_minor: Regex pattern to retrieve the minor version from the
                composite release id string extracted using dataset_crid. 
            @param dataset_crid_patch: Regex pattern to retrieve the patch version from the
                composite release id string extracted using dataset_crid. 
            @return: 
            {
                "dataset_name":"/some/path/SMAP_L4_SM_gph_20200915T193000_Vv5014_001.h5",
                "error":"message for error if error exists",
                "partition":
                        {
                            "filename":"SMAP_L4_SM_gph_20200915T193000_Vv5014_001.h5",
                            "id":"SMAP_L4_SM_gph",
                            "crid":"Vv5014_001",
                            "major": "v5014",
                            "minor":"001",
                            "patch":"")
                        },
                "valid":
                    {
                        "skip": False,
                        "status": False,
                        "message": "Missing: patch"                        
                    }
            }
        """
        _the_ret = self.get_dataname_crid_partitions(
            dataset_name=dataset_name,
            dataset_crid=dataset_crid,
            dataset_crid_major=dataset_crid_major,
            dataset_crid_major_group=dataset_crid_major_group,
            dataset_crid_minor=dataset_crid_minor,
            dataset_crid_minor_group=dataset_crid_minor_group,
            dataset_crid_patch=dataset_crid_patch,
            dataset_crid_patch_group=dataset_crid_patch_group)
        _the_ret['valid']=dict()
        _the_ret["valid"]["message"]=""
        if (not dataset_crid or
            not dataset_crid_major or
            not dataset_crid_minor or 
            not dataset_crid_patch):
            _the_ret["valid"]["skip"]=True
        else:
            _the_ret["valid"]["skip"]=False
            self._validate(_the_ret)
        return _the_ret

    def _validate(
            self,
            crid_partition:dict):
        """
            Analyze if the dataset has valid minimum set of content included in
            the CRID.
            @param crid_partitiion: [Input][Output] dict object ("valid" attribute
            is where the result of the validation goes))
            {
                "dataset_name":"/some/path/SMAP_L4_SM_gph_20200915T193000_Vv5014_001.h5",
                "error":"message for error if error exists",
                "partition":
                    {
                        "filename":"SMAP_L4_SM_gph_20200915T193000_Vv5014_001.h5",
                        "id":"SMAP_L4_SM_gph",
                        "crid":"Vv5014_001",
                        "major": "v5014",
                        "minor":"001",
                        "patch":""),
                    },
                "valid":
                    {
                        "skip": False,
                        "status": False,
                        "message": "Missing: patch"                        
                    }
            }
            Attributes under "valid":
                - skip [bool]: Set depending on input parameters.
                - status [bool]: True - major/minor/patch exist.
        """
        if 'valid' not in crid_partition:
            crid_partition["valid"]=dict()
        _v = crid_partition["valid"]
        if "partition" not in crid_partition:
            crid_partition["warning"] = "Unexpected Error for partition"
            _v["skip"] = True
            return

        _p = crid_partition["partition"]
        if "crid" not in _p:
            crid_partition["warning"] = "No crid is set"
            _v["skip"] = True
            return
        if not _p["crid"]:
            crid_partition["warning"] = ("No crid is extracted from filename."
                                         " Regex pattern for crid may be incorrect.")
            _v["skip"] = True
            return
        if "major" not in _p:
            crid_partition["warning"] = "Unexpected Error for partition crid major parameter"
            _v["skip"] = True
            return
        if "minor" not in _p:
            crid_partition["warning"] = "Unexpected Error for partition crid minor parameter"
            _v["skip"] = True
            return
        if "patch" not in _p:
            crid_partition["warning"] = "Unexpected Error for partition crid patch parameter"
            _v["skip"] = True
            return
        _v["status"] = True
        _the_message = _v["message"]
        if not _p["major"]:
            _the_message = _the_message + "Missing major. "
            _v["status"] = False
        if not _p["minor"]:
            _the_message = _the_message + "Missing minor. "
            _v["status"] = False
        if not _p["patch"]:
            _the_message = _the_message + "Missing patch. "
            _v["status"] = False
        # check order of major, minor, patch
        _s = ".*" + _p["major"] + ".*" + _p["minor"] + ".*" + _p["patch"] + ".*"
        _pattern = re.compile(_s)
        _m = re.match(_pattern, _p["crid"])
        if not _m:
            _the_message = _the_message + "Incorrect order of major, minor, and patch in CRID."
            _v["status"] = False
        _v["message"] = _the_message

    def get_dataname_crid_partitions(self,
                                dataset_name:str,
                                dataset_crid:str=None,
                                dataset_crid_major:str=None,
                                dataset_crid_major_group:str="major",
                                dataset_crid_minor:str=None,
                                dataset_crid_minor_group:str="major",
                                dataset_crid_patch:str=None,
                                dataset_crid_patch_group:str="patch")->dict:
        """
            Get filename exteion for the dataset.
            @param dataset_name: Full path to a granuale file.
            @param dataset_crid: a unique identifier for each release (version, collection)
                of the dataset or a unique Combined Release ID or a regex expression for such 
                id to be extracted from the filename or to be matched in the filename.
            @param dataset_crid_major: Regex pattern to retrieve the major version from the
                composite release id string extracted using dataset_crid. 
            @param dataset_crid_minor: Regex pattern to retrieve the minor version from the
                composite release id string extracted using dataset_crid. 
            @param dataset_crid_patch: Regex pattern to retrieve the patch version from the
                composite release id string extracted using dataset_crid. 
            @return: 
            {
                "dataset_name":"/some/path/SMAP_L4_SM_gph_20200915T193000_Vv5014_001.h5",
                "error":"message for error if error exists",
                "partition":
                        {
                            "filename":"SMAP_L4_SM_gph_20200915T193000_Vv5014_001.h5",
                            "id":"SMAP_L4_SM_gph",
                            "crid":"Vv5014_001",
                            "major": "v5014",
                            "minor":"001",
                            "patch":"")
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
            _the_crid = ""
            # extract granule crid (composite release id)
            if dataset_crid:
                _the_crid = self._gdal_extract_from_filename_using_regex(
                    pattern=dataset_crid, filename=_the_filename)
                _the_ret["partition"]["crid"] = _the_crid
            if not  _the_crid:
                return _the_ret
            # extract major
            if dataset_crid_major:
                _the_ret["partition"]["major"] = self._gdal_extract_from_substring_using_regex_group(
                    pattern=dataset_crid_major,
                    group_name=dataset_crid_major_group,
                    substring=_the_crid)
            # extract minor
            if dataset_crid_minor:
                _the_ret["partition"]["minor"] = self._gdal_extract_from_substring_using_regex_group(
                    pattern=dataset_crid_minor,
                    group_name=dataset_crid_minor_group,
                    substring=_the_crid)
            # extract patch
            if dataset_crid_patch:
                _the_ret["partition"]["patch"] = self._gdal_extract_from_substring_using_regex_group(
                    pattern=dataset_crid_patch,
                    group_name=dataset_crid_patch_group,
                    substring=_the_crid)
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
