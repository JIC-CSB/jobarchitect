#!/bin/bash

# Clean up old stuff
rm -f deploy/docker/*.whl
rm -f dist/*

# Build and copy wheel
python2 setup.py bdist_wheel
cp dist/*.whl deploy/docker/jobarchitect-0.1.0-py2-none-any.whl

# Build docker image
docker build -t jicscicomp/jobarchitect deploy/docker/
