FROM python:3.9.19-slim as builder

RUN apt-get update \
    && apt-get install -y --no-install-recommends \
        cmake \
        build-essential \
        git \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /test-assignment

RUN git clone https://github.com/ANTsX/ANTs.git \
    && rm -rf build install \
    && mkdir build install \
    && cd build \
    && cmake \
    -DCMAKE_INSTALL_PREFIX=/test-assignment/install \
    -DBUILD_TESTING=OFF \
    -DRUN_LONG_TESTS=OFF \
    -DRUN_SHORT_TESTS=OFF \
    ../ANTs 2>&1 | tee cmake.log \
    && make -j 4 2>&1 | tee build.log \
    && cd ANTS-build && make install 2>&1 | tee install.log \
    && rm -rf /var/lib/apt/lists/* 

FROM python:3.9.19-slim

RUN apt-get update \
    && apt-get install -y --no-install-recommends bc tar \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /test-assignment

COPY --from=builder /test-assignment/install/bin /test-assignment/install/bin

ENV PATH=/test-assignment/install/bin:$PATH 
    
ENV ANTSPATH=/test-assignment/install/bin

COPY requirements.txt .

RUN pip install -r requirements.txt

COPY . .

RUN chmod +x extract.sh

EXPOSE 4000

CMD ["python", "src/main.py"]
