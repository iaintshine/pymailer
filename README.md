# PyMailer

This is a super simple python server I wrote for a friend, to enable his clients to contact him directly from his web page. 

It exposes two endpoints:
1. `/ping` used for health-checking
2. `/emails/send` used for sending emails to him directly. Options: `email`, `name`, `phone`, `comment`.

## Requirements

Mandrill account. See config.yml.sample

## Docker 

`PYMAILER_HOME` is set by default to `/etc/pymailer/` so you should mount volume with a configuration file to `/etc/pymailer`.

To download (pull) and run the container:

```bash
$ docker pull iaintshine/pymailer
$ docker run -d --log-driver=syslog --restart=always -v /etc/pymailer:/etc/pymailer:ro -p 127.0.0.1:9000:5000 iaintshine/pymailer
```

## Development

```bash
$ PYMAILER_HOME=$(pwd) python mailer.py
```

or using gunicorn

```bash
$ PYMAILER_HOME=$(pwd) gunicorn -b 127.0.0.1:5000 mailer:app
```

To build the container:

```bash
$ docker build -t pymailer .
```

To run container in interactive mode:

```bash
$ docker run -it -v $(pwd):/etc/pymailer:ro -p 127.0.0.1:9000:5000 pymailer
```
