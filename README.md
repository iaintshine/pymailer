# PyMailer

This is a super simple python server I wrote for a friend, to enable his clients to contact him directly from his web page. 

It exposes two endpoints:
1. `/ping` used for health-checking
2. `/emails/send` used for sending emails to him directly.

## Requirements

Mandrill account. See config.yml.sample

## Docker 

```bash
$ docker run -it -e MAILER_HOME=/etc/pymailer -v $(pwd):/etc/pymailer:ro -p 127.0.0.1:9000:5000 pymailer
```
