# The build-stage image:
FROM continuumio/miniconda3 AS build

# Install the package as normal:
COPY ./conf/environment.yml .
RUN conda env create -f environment.yml

# Install conda-pack:
RUN conda install -c conda-forge conda-pack

# Use conda-pack to create a standalone enviornment
# in /venv:
RUN conda-pack -n myenv -o /tmp/env.tar && \
  mkdir /venv && cd /venv && tar xf /tmp/env.tar && \
  rm /tmp/env.tar

# We've put venv in same path it'll be in final image,
# so now fix up paths:
RUN /venv/bin/conda-unpack


# The runtime-stage image; we can use Debian as the
# base image since the Conda env also includes Python
# for us.
FROM debian:bookworm-slim AS runtime

# Copy /venv from the previous stage:
COPY --from=build /venv /venv

# Copy programs to destination
RUN mkdir -p /opt/app
RUN mkdir -p /opt/app/tests
RUN mkdir -p /opt/app/diwg_dataset
COPY conftest.py /opt/app
COPY tests /opt/app/tests
COPY diwg_dataset /opt/app/diwg_dataset
COPY bin/startup /usr/local/bin
RUN chmod a+x /usr/local/bin/startup
#set up the running environment
#RUN cd /opt/app
#RUN source /venv/bin/activate
# When image is run, run the code with the environment
# activated:
#SHELL ["/bin/bash", "-c"]
#ENTRYPOINT source /venv/bin/activate && \
#           python -c "from osgeo import gdal; import pytest; import sys; print('pytest-version=', pytest.__version__); print('gdal versioninfo:', gdal.VersionInfo()); print('python version = ', sys.version); print('success!')"
# ENTRYPOINT ['source /venv/bin/activate && cd /opt/app && pytest']
ENTRYPOINT ["bash", "/usr/local/bin/startup"]
CMD ["--help"]