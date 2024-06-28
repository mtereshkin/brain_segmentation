FROM ubuntu:latest

RUN apt-get update
RUN apt-get install -y --no-install-recommends python3 python3-pip -y

WORKDIR /test-assignment

COPY requirements.txt .

RUN pip3 install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 8080

CMD ["python3", "src/main.py"]