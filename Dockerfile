FROM ubuntu

RUN echo "deb http://archive.ubuntu.com/ubuntu/ $(lsb_release -sc) main universe" >> /etc/apt/sources.list
RUN apt-get update

RUN apt-get install -y git curl wget python-setuptools python-dev libffi-dev libssl-dev
RUN easy_install pip

RUN git clone https://github.com/iaintshine/pymailer.git 
RUN cd /pymailer; git pull
RUN cd /pymailer; pip install pyopenssl ndg-httpsclient pyasn1
RUN cd /pymailer; pip install -r requirements.txt

RUN mkdir /pymailer/log; touch /pymailer/log/access.log; touch /pymailer/log/error.log

EXPOSE 5000

WORKDIr /pymailer

CMD PYTHONUNBUFFERED=FALSE gunicorn -w 2 -b 0.0.0.0:5000 --access-logfile "-" --error-logfile "-" --log-level info --enable-stdio-inheritance mailer:app 
