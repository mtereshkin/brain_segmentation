FROM python:3.9.19-slim

WORKDIR /test-assignment

COPY requirements.txt .

RUN pip install -r --no-cache-dir requirements.txt

COPY . .

EXPOSE 8080

CMD ["python", "src/main.py"]