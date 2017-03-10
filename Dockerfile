FROM python:3.6.0-onbuild
ADD . /app
WORKDIR /app
RUN pip install -r requirements.txt
