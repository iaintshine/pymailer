import os
import json
from yaml import load
import flask
from flask import request
import mandrill

app = flask.Flask(__name__)


class Config:
    DEFAULT_PATH = '/etc/pymailer/'

    def __init__(self):
        self._config = None

    @property
    def app_home(self):
        path = os.environ.get('PYMAILER_HOME')
        if path is None:
            path = self.DEFAULT_PATH
        return path

    @property
    def config_path(self):
        return os.path.join(self.app_home, 'config.yml')

    def load(self):
        if not self._config:
            if not os.path.isfile(self.config_path):
                raise Exception('config.yml file could not be found at'
                                'path: ' + self.app_home)

            with open(self.config_path) as f:
                self._config = load(f.read())
        return self

    @property
    def dict(self):
        return self._config


class PyMailer:
    __global_config = None

    @classmethod
    def config(cls):
        if cls.__global_config is None:
            cls.__global_config = Config().load().dict
        return cls.__global_config


class Mail:
    def __init__(self, params):
        self.params = params
        self.config = PyMailer.config()

    @property
    def mandrill_client(self):
        return mandrill.Mandrill(self.config['mandrill']['api_key'])

    @property
    def name(self):
        return self.params.get('name', 'unknown')

    @property
    def email(self):
        return self.params.get('email', 'unknown@unknown.com')

    @property
    def phone(self):
        return self.params.get('phone', 'unknown')

    @property
    def domain(self):
        return self.config['website']['domain']

    @property
    def subject(self):
        return self.domain + ' ' + self.name + ', tel: ' + self.phone

    @property
    def text(self):
        return self.params.get('comment', '')

    @property
    def recipient(self):
        return {
            'email': self.config['recipient']['email'],
            'name': self.config['recipient']['name'],
            'type': 'to'
        }

    @property
    def message(self):
        return {
            'from_email': self.email,
            'from_name': self.name,
            'to': [self.recipient],
            'subject': self.subject,
            'text': self.text,
            'metadata': {
                'website': self.domain
            }
        }

    def send(self):
        try:
            result = self.mandrill_client.messages.send(message=self.message,
                                                        async=True)
            print result
            return {
                'status': result[0]['status'],
                'id': result[0].get('_id', None)
            }
        except mandrill.Error, e:
            print 'A mandrill error occurred: %s - %s' % (e.__class__, e)
            raise


@app.route("/ping", methods=['GET'])
def ping():
    return "pong"


@app.route("/emails/send", methods=['POST'])
def send():
    status = Mail(request.form).send()
    return json.dumps(status)

if __name__ == "__main__":
    app.run(debug=True)
