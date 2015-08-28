import click
import getpass
import json
import os
import requests
import yaml


class Config(object):

    def __init__(self, path):
        self.path = path
        self.read()

    def get(self, key):
        if not self.yaml:
            return None
        return self.yaml.get(key)

    def read(self):
        with os.fdopen(os.open(self.path, os.O_RDONLY | os.O_CREAT, 0600), 'r') as file:
            y = yaml.load(file.read())
            self.yaml = y if y else {}

    def set(self, key, value):
        if not self.yaml:
            self.yaml = {}
        self.yaml[key] = value

    def write(self):
        with os.fdopen(os.open(self.path, os.O_WRONLY | os.O_CREAT, 0600), 'w') as file:
            file.write(yaml.safe_dump(self.yaml, default_flow_style=False))


class Wizard(object):

    max_tries = 3

    def __call__(self, ctx, param, values):
        '''Helps create a configuration file when it does not exist.

        Args:
            ctx: click.Context
            param: click.Param
            values: parameter value

        Returns:
            groceries.config.Config
        '''
        config = Config(values)
        if not config.get('api'):
            config = self.api(ctx, config)
        if not config.get('token'):
            config = self.token(ctx, config)
        return config

    def api(self, ctx, config, count=1):
        if count == 1:
            click.echo('Config is missing an API setting.')
        url = raw_input('What is the URL of the API? ')
        try:
            if not requests.get('{0}{1}'.format(url, '/status')).status_code == 200:
                raise Exception()
            config.set('api', url)
            config.write()
        except Exception, e:
            if count < self.max_tries:
                click.echo('Incorrect URL provided')
                count += 1
                return self.api(ctx, config, count)
            ctx.abort()
        return config

    def token(self, ctx, config, count=1):
        if count == 1:
            click.echo('Configuration is missing a token.')
        username = raw_input('What is your username? ')
        password = getpass.getpass('And your password? ')
        try:
            token = requests.post('{0}{1}'.format(config.get('api'), '/login'),
                                  data=json.dumps({'username': username, 'password': password}),
                                  headers={'Content-Type': 'application/json'}).json().get('token')
            if not token:
                raise Exception()
            config.set('token', token)
            config.write()
        except:
            if count < self.max_tries:
                click.echo('Invalid username and/or password.')
                count += 1
                return self.token(ctx, config, count)
            ctx.abort()
        return config
