import click
import getpass
import json
import os
import requests
import yaml


class Config(object):

    def __init__(self, path):
        '''Create a new instance.

        Args:
            path: string containing file path
        '''
        self.path = path
        self.read()

    def get(self, key):
        '''Get a configuration value.

        Args:
            key: key as a string to get value for

        Returns:
            Configuration value for requested key.
        '''
        if not self.yaml:
            return None
        return self.yaml.get(key)

    def read(self):
        '''Read the contents of the configuration file.'''
        fd = os.open(self.path, os.O_RDONLY | os.O_CREAT, 0600)
        with os.fdopen(fd, 'r') as file:
            y = yaml.load(file.read())
            self.yaml = y if y else {}

    def set(self, key, value):
        '''Set a configuration value.

        Args:
            key: key as a string to set the value for
            value: value to assign to key
        '''
        if not self.yaml:
            self.yaml = {}
        self.yaml[key] = value

    def write(self):
        '''Write the configuration to the file.'''
        fd = os.open(self.path, os.O_WRONLY | os.O_CREAT, 0600)
        with os.fdopen(fd, 'w') as file:
            file.write(yaml.safe_dump(self.yaml, default_flow_style=False))


class Wizard(object):

    show_message = True

    def __init__(self):
        '''Helps create a configuration file when it does not exist.'''
        self.steps = [Api(), Token()]

    def __call__(self, ctx, param, values):
        '''Usable as the callback in a click.Parameter.

        Args:
            ctx: click.Context
            param: click.Param
            values: parameter value

        Returns:
            groceries.config.Config
        '''
        config = Config(values)
        for step in self.steps:
            if not config.get(step.key):
                if self.show_message:
                    self.show_message = False
                    click.echo('Part of the configuration is incomplete. '
                               'Please answer the following questions:')
                config = step(ctx, config)
        return config


class Step(object):

    key = None
    error = 'Invalid value provided'
    max_tries = 3

    def __call__(self, ctx, config, count=1):
        '''Execute a single step in the wizard.

        Args:
            ctx: click.Context
            config: groceries.config.Config
            count: number of tries

        Returns:
            groceries.config.Config
        '''
        try:
            config.set(self.key, self.value(config))
        except:
            if count < self.max_tries:
                click.echo(self.error)
                count += 1
                return self(ctx, config, count)
            ctx.abort()
        config.write()
        return config


class Api(Step):

    key = 'api'
    error = 'Invalid URL provided'

    def value(self, config):
        '''Get the URL for the API.

        Args:
            config: groceries.config.Config

        Returns:
            String containing the URL.
        '''
        url = raw_input('What is the URL of the API? ')
        r = requests.get('{0}{1}'.format(url, '/status'))
        if not r.status_code == 200:
            raise Exception()
        return url


class Token(Step):

    key = 'token'
    error = 'Invalid username and/or password provided.'

    def value(self, config):
        '''Get the token to use for authentication.

        Args:
            config: groceries.config.Config

        Returns:
            String containing the token.
        '''
        username = raw_input('What is your username? ')
        password = getpass.getpass('And your password? ')
        r = requests.post('{0}{1}'.format(config.get('api'), '/login'),
                          data=json.dumps({'username': username,
                                           'password': password}),
                          headers={'Content-Type': 'application/json'})
        return r.json().get('token')
