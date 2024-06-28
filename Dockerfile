FROM ubuntu:latest

RUN apt update
RUN apt install python3 python3-pip -y

WORKDIR /test-assignment

COPY . .

RUN pip3 install -r requirements.txt

EXPOSE 8080

CMD ["python3", "src/main.py"]