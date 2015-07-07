FROM ubuntu

RUN echo "deb http://archive.ubuntu.com/ubuntu/ $(lsb_release -sc) main universe" >> /etc/apt/sources.list
RUN apt-get update

RUN apt-get install -y git curl wget python-setuptools
RUN easy_install pip

COPY  . /src
RUN cd /src; pip install -r requirements.txt

EXPOSE 5000

WORKDIR /src
CMD gunicorn -w 2 -b 0.0.0.0:5000 mailer:app 
