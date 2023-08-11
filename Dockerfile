FROM python:3.9

WORKDIR /satelite-monitoring-app

COPY requirements.txt requirements.txt
RUN pip3 install -r requirements.txt
ENV KEY_NASA_EARTH=''
ENV READ_TIMEOUT_HTTPS=''
ENV CONNECT_TIMEOUT_HTTPS=''
ENV ACCESS_KEY_ID=''
ENV SECRET_ACCESS_KEY=''
ENV BUCKET_NAME=''
COPY . .

CMD ["uvicorn","app.main:app", "--reload", "--host", "0.0.0.0", "--port", "5000"]
