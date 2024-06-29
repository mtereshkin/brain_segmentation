#!/bin/bash

workingDir=/test_assignment
git clone https://github.com/ANTsX/ANTs.git
mkdir build install
cd build
cmake \
    -DCMAKE_INSTALL_PREFIX=${workingDir}/install \
    -DBUILD_TESTING=OFF \
    -DRUN_LONG_TESTS=OFF \
    -DRUN_SHORT_TESTS=OFF \
    ../ANTs 2>&1 | tee cmake.log
make -j 4 2>&1 | tee build.log
cd ANTS-build
make install 2>&1 | tee install.log
export PATH=${workingDir}/install/antsbin/bin:$PATH
export ANTSPATH=${workingDir}/install/antsbin/bin
