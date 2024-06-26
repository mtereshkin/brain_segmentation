FROM python:3.9.19-slim

WORKDIR /test-assignment

COPY . .

RUN pip install -r requirements.txt

EXPOSE 8080

CMD ["python", "src/main.py"]