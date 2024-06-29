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

RUN chmod +x install.sh

EXPOSE 8080

CMD ./install.sh && python src/main.py