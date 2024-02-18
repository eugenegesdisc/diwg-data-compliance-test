# diwg-data-compliance-test
Data compliance test against the recommendations of ESDSWG DIWG

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
docker run --name diwgtest -v /datapath:/data diwgtest --dataset-name-list='/data/datacollection.lst' -v --tb=line
```
## Testing Examples

The following will use the conda running environment. For docker environment, the only difference is mapping of a local path to docker container and using the mapped path for path in container.

### Running all applicable tests against a dataset

### Running all applicable tests against a grid dataset

### Running all applicable tests against a swath dataset

### Running selected tests against a dataset

### Running tests on metadata only

### Running a specific tests by name

### Export a test to json

### Export a test to HTML

### Export a test to markdown
