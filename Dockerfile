FROM python:3.7-alpine

LABEL maintainer="Ludovic Ortega mastership@hotmail.fr"

# update package
RUN apk update

# install git
RUN apk add git

# copy program and requirements
COPY main.py requirements.txt /app/tplink-smartplug-influxdb/

# install dependencies
RUN pip3 install -r /app/tplink-smartplug-influxdb/requirements.txt

CMD ["python3", "/app/tplink-smartplug-influxdb/main.py"]