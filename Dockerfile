FROM python:3.9.19-slim

RUN apt-get update \
    && apt-get install -y --no-install-recommends \
        cmake \
        build-essential \
        git \
        bc \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /test-assignment

COPY requirements.txt .

RUN pip install -r requirements.txt

COPY . .

RUN git clone https://github.com/ANTsX/ANTs.git \
    && rm -rf build install \
    && mkdir build install \
    && cd build \
    && cmake \
    -DCMAKE_INSTALL_PREFIX=/test_assignment/install \
    -DBUILD_TESTING=OFF \
    -DRUN_LONG_TESTS=OFF \
    -DRUN_SHORT_TESTS=OFF \
    ../ANTs 2>&1 | tee cmake.log \
    && make -j 4 2>&1 | tee build.log \
    && cd ANTS-build && make install 2>&1 | tee install.log 

ENV PATH=/test_assignment/install/bin:$PATH 
    
ENV ANTSPATH=/test_assignment/install/bin

EXPOSE 8080

CMD ["python", "src/main.py"]

