# diwg-data-compliance-test
Data compliance test against the recommendations of ESDSWG DIWG
## Recommendations for compliance test

**Test for recommendations in document # ESDS-RFC-028v1.3**
| Number | Name |Test signature |
| ----------- | ----------- |----------- |
| 2.5 | [Distinguish clearly between HDF and netCDF packing conventions](https://wiki.earthdata.nasa.gov/display/ESDSWG/Distinguish+clearly+between+HDF+and+netCDF+packing+conventions)  |data_packing|

**Test for recommendations in document # ESDS-RFC-36v1.2**
| Number | Name |Test signature |
| ----------- | ----------- |----------- |
| 3.1 | [Character Set for User-Defined Group, Variable, and Attribute Names](https://wiki.earthdata.nasa.gov/display/ESDSWG/Character+Set+for+User-Defined+Group%2C+Variable%2C+and+Attribute+Names)  |group_variable_attribute_name_conventions|
| 3.2 | [Consistent Units Attribute Value for Variables Across One Data Collection](https://wiki.earthdata.nasa.gov/display/ESDSWG/Consistent+Units+Attribute+Value+for+Variables+Across+One+Data+Collection)  |variable_units_consistency|
| 3.3 | [Use the Units Attribute Only for Variables with Physical Units](https://wiki.earthdata.nasa.gov/pages/viewpage.action?pageId=182296347)  |variable_physical_units|
| 3.4 | [Include Time Coordinate in Swath Structured Data](https://wiki.earthdata.nasa.gov/display/ESDSWG/Include+Time+Coordinate+in+Swath+Structured+Data)  |include_time_coord_in_swath|
| 3.5 | [Keep Coordinate Values in Coordinate Variables](https://wiki.earthdata.nasa.gov/display/ESDSWG/Keep+Coordinate+Values+in+Coordinate+Variables)  |keep_coordinate_values_in_coordinate_variables|
| 3.6 | [Include Georeference Information with Geospatial Coordinates](https://wiki.earthdata.nasa.gov/display/ESDSWG/Include+Georeference+Information+with+Geospatial+Coordinates)  |include_georeference_information|
| 3.7 | [Not-a-Number (NaN) Value](https://wiki.earthdata.nasa.gov/display/ESDSWG/Not-a-Number+%28NaN%29+Value)  |not_a_number_value|

## Setup running environment
### Run from source
To run the test by setting up the running environment with the source, follow these steps:

1. Clone the repository.
```
git clone https://github.com/eugenegesdisc/diwg-data-compliance-test.git
```
2. Change to the cloned source directory and create the conda environment.
```
cd diwg-data-compliance-test
conda env create -f conf/environment.yml
conda activate diwgtest
```
3. Run with pytest.
```
pytest --help
```
4. Run test against one dataset or subdataset (in GDAL term).
```
pytest --dataset-name='datasetname.nc' -v --tb=line
```
5. Run test against one dataset collection. The content of a dataset collection list file may contain lines of files/subdatasets. Each line may use wildcards for a group of files that can be extended using glob of python.
```
pytest --dataset-name-list='datacollection.lst' -v --tb=line
```

### Run with Docker

To run the test with Docker, follow these steps:

1. Clone the repository.
```
git clone https://github.com/eugenegesdisc/diwg-data-compliance-test.git
```
2. Change to the cloned source directory and build the docker image.
```
cd diwg-data-compliance-test
docker image build -t diwgtest .
```
3. Run with pytest. If a container with name 'diwgtest' exist, you may use a different name or remove it first by running 'docker container rm diwgtest'.
```
docker run --name diwgtest diwgtest
```
4. Run test against one dataset or subdataset (in GDAL term).
```
docker run --name diwgtest -v /datapath:/data diwgtest --dataset-name='/data/datasetname.nc' -v --tb=line
```
5. Run test against one dataset collection. The content of a dataset collection list file may contain lines of files/subdatasets. Each line may use wildcards for a group of files that can be extended using glob of python.
```
docker run --name diwgtest -v /localdatapath:/data -v /localdatapath:/data diwgtest --dataset-name-list='/data/datacollection.lst' -v --tb=line
```
## Testing Examples

The following will use the conda running environment. For docker environment, the only difference is mapping of a local path to docker container and using the mapped path for path in container.

Working environment assumptions:

- Data is made available under directory */data*
- Reports will be outputed to */reports*
- Current working directory is at the root of program diwg-data-compliance-test. So, pytest will collect all matching tests from the current directory.

The equivalent docker running command line would look like starting with the following:
```
docker run --name diwgtest -v /localdatapath:/data -v /localreportpaath:/reports diwgtest 
```

### Running all applicable tests against a dataset

Example steps:
1. Data source: Download the data from the following link to *"/data"* directory. It needs your earthdata authentication.
```
https://n5eil01u.ecs.nsidc.org/SMAP/NSIDC-0774.001/2015.04.20/NSIDC-0774-EASE2_N25km-SMAP_Radar_Slice-2015110_2015110-1.2HH-E-GRD-v1.0.nc
```
2. Running one of the following steps:

  - Running all applicable tests against a *subdataset*:
```
pytest --dataset-name='NETCDF:"/data/NSIDC-0774-EASE2_N25km-SMAP_Radar_Slice-2015110_2015110-1.2HH-E-GRD-v1.0.nc":Sigma0' -v --tb=line
```
  - Running all applicable tests against the dataset:
```
pytest --dataset-name="/data/NSIDC-0774-EASE2_N25km-SMAP_Radar_Slice-2015110_2015110-1.2HH-E-GRD-v1.0.nc" -v --tb=line
```

### Running all applicable tests against a grid dataset

Example steps:
1. Data source: Download the data from the following link to *"/data"* directory.
```
https://gamma.hdfgroup.org/ftp/pub/outgoing/NASAHDF/S1-GUNW-A-R-072-tops-20230520_20220618-145958-00044E_00030N-PP-ab21-v2_0_6.nc
```
2. Running one of the following steps:

  - Running all applicable tests against a *subdataset*:
```
pytest --dataset-is-grid --dataset-name='NETCDF:"/data/S1-GUNW-A-R-072-tops-20230520_20220618-145958-00044E_00030N-PP-ab21-v2_0_6.nc":/science/grids/data/coherence' -v --tb=line
```
  - Running all applicable tests against the dataset:
```
pytest --dataset-is-grid --dataset-name="/data/S1-GUNW-A-R-072-tops-20230520_20220618-145958-00044E_00030N-PP-ab21-v2_0_6.nc" -v --tb=line
```

### Running all applicable tests against a swath dataset


Example steps:
1. Data source: Download the data from the following link to *"/data"* directory. It needs your earthdata authentication.
```
https://measures.gesdisc.eosdis.nasa.gov/data/MINDS/TROPOMI_MINDS_NO2.1.1/2018/121/TROPOMI-S5P_L2-TROPOMI_MINDS_NO2_2018m0501t000052-o02832_v01-01-2022m0506t132144.nc
```
2. Running one of the following steps:

  - Running all applicable tests against a *subdataset*:
```
pytest --dataset-is-swath --dataset-name='NETCDF:"/data/TROPOMI-S5P_L2-TROPOMI_MINDS_NO2_2018m0501t000052-o02832_v01-01-2022m0506t132144.nc"://SCIENCE_DATA/AmfStrat' -v --tb=line
```
  - Running all applicable tests against the dataset:
```
pytest --dataset-is-swath --dataset-name="/data/TROPOMI-S5P_L2-TROPOMI_MINDS_NO2_2018m0501t000052-o02832_v01-01-2022m0506t132144.nc" -v --tb=line
```

### Running all applicable tests against a dataset collection

A dataset collection is defined by a file with multiple lines where each line represents a subdataset, a daataset, or a collection of datasets (with applicable wildcards).

Example steps:
1. Data source: Download the data from the following links to *"/data"* directory. It needs your earthdata authentication.
```
https://aura.gesdisc.eosdis.nasa.gov/data/Aura_OMI_Level2/OMNO2.003/2004/275/OMI-Aura_L2-OMNO2_2004m1001t0003-o01132_v003-2019m0814t172940.he5

https://aura.gesdisc.eosdis.nasa.gov/data/Aura_OMI_Level2/OMNO2.003/2004/276/OMI-Aura_L2-OMNO2_2004m1002t0046-o01147_v003-2019m0814t172908.he5
```
3. Create the collection file *"test_collection.lst"* under */data* with the following content:
```
/data/OMI-Aura_L2-OMNO2*.he5
```

4. Create the collection file *"test_subdataset_collection.lst"* under */data* with the following content:
```
HDF5:"/data/OMI-Aura_L2-OMNO2_2004m1001t0003-o01132_v003-2019m0814t172940.he5"://HDFEOS/SWATHS/ColumnAmountNO2/Data_Fields/ScenePressure
HDF5:"/data/MI-Aura_L2-OMNO2_2004m1002t0046-o01147_v003-2019m0814t172908.he5"://HDFEOS/SWATHS/ColumnAmountNO2/Data_Fields/ScenePressure
```


5. Running one of the following steps:

  - Running all applicable tests against a *subdataset* collection:
```
pytest --dataset-is-swath --dataset-name-list="/data/test_subdatasets_collection.lst" -v --tb=line
```
  - Running all applicable tests against a dataset collection:
```
pytest --dataset-is-swath --dataset-name-list="/data/test_collection.lst" -v --tb=line
```


### Running selected tests

Pytest allows search against the signature of tests using keyword. The signature of tests is formed by test filename + test class name + test method. Any part of the signature can be filtered with, without, or combined.

Example selection of tests:
1. Data source: Download the data from the following links to *"/data"* directory. It needs your earthdata authentication.
```
https://gpm1.gesdisc.eosdis.nasa.gov/data/GPM_L3/GPM_3IMERGHH.07/2023/132/3B-HHR.MS.MRG.3IMERG.20230512-S000000-E002959.0000.V07B.HDF5

https://gpm1.gesdisc.eosdis.nasa.gov/data/GPM_L3/GPM_3IMERGHH.07/2023/132/3B-HHR.MS.MRG.3IMERG.20230512-S003000-E005959.0030.V07B.HDF5
```
3. Create the collection file *"test_collection.lst"* under */data* with the following content:
```
/data/3B-HHR.MS.MRG.3IMERG*.HDF5
```

4. Running one of the following steps:

  - Running tests with "units" in signature but not "physical":
```
pytest -k "units and not physical" --dataset-name-list="/data/test_collection.lst" -v --tb=line
```
  - Running tests with "units" in signature but not "consistency":
```
pytest -k "units and not consistency" --dataset-name-list="/data/test_collection.lst" -v --tb=line
```


### Running tests on metadata only
Implementations of compliance tests primarily relies on GDAL library to examine dataset. There are three levels of computing intensities: verifying filenames, verifying metadata (mainly using gdalinfo library calls), and verifying data values (read all bands). The requirements of computing resources and time increases. At times, we may want to skip computing intensive routines and focuses on only those checks with less computing requirements on time and resources. This example demonstrates how to run all the tests on metadata but on actual data values.

Example testing on metadata only:
1. Data source: Download the data from the following links to *"/data"* directory. It needs your earthdata authentication.
```
https://gpm1.gesdisc.eosdis.nasa.gov/data/GPM_L3/GPM_3IMERGHH.07/2023/132/3B-HHR.MS.MRG.3IMERG.20230512-S000000-E002959.0000.V07B.HDF5

https://gpm1.gesdisc.eosdis.nasa.gov/data/GPM_L3/GPM_3IMERGHH.07/2023/132/3B-HHR.MS.MRG.3IMERG.20230512-S003000-E005959.0030.V07B.HDF5
```
3. Create the collection file *"test_collection.lst"* under */data* with the following content:
```
/data/3B-HHR.MS.MRG.3IMERG*.HDF5
```

4. Running all the tests except those requires loading data values:

```
pytest -k "not _array_" --dataset-name-list="/data/test_collection.lst" -v --tb=line
```

### Running a specific test
This example demonstrates how to run a specific test by specifying the name or searching the specific signature as listed at the begining of this document.

Example to run the compliance test on Recommendation 3.1 of ESDS-RFC-36v1.2 ([Character Set for User-Defined Group, Variable, and Attribute Names](https://wiki.earthdata.nasa.gov/display/ESDSWG/Character+Set+for+User-Defined+Group%2C+Variable%2C+and+Attribute+Names)):

1. Data source: Download the data from the following links to *"/data"* directory. It needs your earthdata authentication.
```
https://gpm1.gesdisc.eosdis.nasa.gov/data/GPM_L3/GPM_3IMERGHH.07/2023/132/3B-HHR.MS.MRG.3IMERG.20230512-S000000-E002959.0000.V07B.HDF5

https://gpm1.gesdisc.eosdis.nasa.gov/data/GPM_L3/GPM_3IMERGHH.07/2023/132/3B-HHR.MS.MRG.3IMERG.20230512-S003000-E005959.0030.V07B.HDF5
```
3. Create the collection file *"test_collection.lst"* under */data* with the following content:
```
/data/3B-HHR.MS.MRG.3IMERG*.HDF5
```


4. Running one of the following steps:

  - Running the test on a specific recommendation by searching with unique signature:
```
pytest -k "group_variable_attribute_name_conventions" --dataset-name-list="/data/test_collection.lst" -v --tb=line
```
  - Running the test on a specific recommendation by specifying test file names:
```
pytest tests/test_*_group_variable_attribute_name_conventions.py --dataset-name-list="/data/test_collection.lst" -v --tb=line
```


### Export a test to json
The results can be exported as a JSON file.

Example to produce report in JSON:
1. Data source: Download the data from the following links to *"/data"* directory. It needs your earthdata authentication.
```
https://gpm1.gesdisc.eosdis.nasa.gov/data/GPM_L3/GPM_3IMERGHH.07/2023/132/3B-HHR.MS.MRG.3IMERG.20230512-S000000-E002959.0000.V07B.HDF5

https://gpm1.gesdisc.eosdis.nasa.gov/data/GPM_L3/GPM_3IMERGHH.07/2023/132/3B-HHR.MS.MRG.3IMERG.20230512-S003000-E005959.0030.V07B.HDF5
```
3. Create the collection file *"test_collection.lst"* under */data* with the following content:
```
/data/3B-HHR.MS.MRG.3IMERG*.HDF5
```

4. Running the following to produce the report in JSON:

```
pytest  --dataset-name-list="/data/test_collection.lst" -v --tb=line --json-report --json-report-file=reports/report.json
```

### Export a test to HTML
The results can be exported as a HTML page.

Example to produce report in HTML:
1. Data source: Download the data from the following links to *"/data"* directory. It needs your earthdata authentication.
```
https://gpm1.gesdisc.eosdis.nasa.gov/data/GPM_L3/GPM_3IMERGHH.07/2023/132/3B-HHR.MS.MRG.3IMERG.20230512-S000000-E002959.0000.V07B.HDF5

https://gpm1.gesdisc.eosdis.nasa.gov/data/GPM_L3/GPM_3IMERGHH.07/2023/132/3B-HHR.MS.MRG.3IMERG.20230512-S003000-E005959.0030.V07B.HDF5
```
3. Create the collection file *"test_collection.lst"* under */data* with the following content:
```
/data/3B-HHR.MS.MRG.3IMERG*.HDF5
```

4. Running the following to produce the report in HTML:

```
pytest  --dataset-name-list="/data/test_collection.lst" -v --tb=line --html=reports/report.html
```

### Export a test to markdown

The results can be exported as a Markdown file.

Example to produce report in HTML:
1. Data source: Download the data from the following links to *"/data"* directory. It needs your earthdata authentication.
```
https://gpm1.gesdisc.eosdis.nasa.gov/data/GPM_L3/GPM_3IMERGHH.07/2023/132/3B-HHR.MS.MRG.3IMERG.20230512-S000000-E002959.0000.V07B.HDF5

https://gpm1.gesdisc.eosdis.nasa.gov/data/GPM_L3/GPM_3IMERGHH.07/2023/132/3B-HHR.MS.MRG.3IMERG.20230512-S003000-E005959.0030.V07B.HDF5
```
3. Create the collection file *"test_collection.lst"* under */data* with the following content:
```
/data/3B-HHR.MS.MRG.3IMERG*.HDF5
```

4. Running the following to produce the report in Markdown:

```
pytest  --dataset-name-list="/data/test_collection.lst" -v --tb=line --md=reports/report.md
```
