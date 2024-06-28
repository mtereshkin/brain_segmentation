FROM python:3.7-alpine

WORKDIR /test-assignment

COPY requirements.txt .

RUN pip install -r requirements.txt

COPY . .

EXPOSE 8080

CMD ["python", "src/main.py"]