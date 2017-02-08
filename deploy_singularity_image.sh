#!/bin/bash

source build_docker_image.sh

# Build singularity image
docker run \
    -v /var/run/docker.sock:/var/run/docker.sock \
    -v ~/mnt/cluster_home/singularity/:/output \
    --privileged \
    -t \
    --rm \
    mcdocker2singularity \
    jicscicomp/jobarchitect \
    sketchjob
