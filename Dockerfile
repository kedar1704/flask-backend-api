FROM python:3.9-alpine
MAINTAINER kedar1704
WORKDIR /app
COPY requirements.txt .
COPY app.py .
RUN pip install -r requirements.txt
EXPOSE 5000
ENTRYPOINT ["python3", "app.py"]
