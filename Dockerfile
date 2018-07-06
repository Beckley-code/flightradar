# python:alpine is 3.{latest} 
FROM python:alpine 
LABEL maintainer="Michael Morandi"
RUN pip install flask peewee python-dateutil pytz
COPY . /src
WORKDIR /src
EXPOSE 5000 
ENTRYPOINT ["python", "web.py"]