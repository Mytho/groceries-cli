import click
import json
import requests
import os
import yaml

from functools import update_wrapper


TOKEN_PATH = '.token'


class Item(object):

    def __init__(self, ctx):
        self.request = Request(ctx)

    def add(self, name):
        r = self.request.post('/item', data=json.dumps(dict(name=name)))
        self.list()

    def list(self):
        r = self.request.get('/item')
        for item in r.json().get('items'):
            click.echo('{0}'.format(item.get('name')))


class Request(object):

    def __init__(self, ctx):
        '''Create a new instance.

        Args:
            ctx: click.Context
        '''
        self.ctx = ctx

    def delete(self, uri, data=None, headers=None):
        '''Shortcut method to do a delete request.

        Args:
            uri: string containing endpoint
            data: dict containing the payload
            headers: dict containing the headers

        Returns:
            requests.Response
        '''
        return self.do('delete', uri, data, headers)

    def do(self, method, uri, data=None, headers=None):
        '''Do a requests using the requests library.

        Args:
            method: string containing HTTP method name
            uri: string containing endpoint
            data: dict containing the payload
            headers: dict containing the headers

        Returns:
            requests.Response
        '''
        if headers is None:
            headers = {'X-Auth-Token': self.ctx.obj.get('token'),
                       'Content-Type': 'application/json'}
        url = '{0}{1}'.format(self.ctx.obj.get('api'), uri)
        return getattr(requests, method)(url, data=data, headers=headers)

    def get(self, uri, data=None, headers=None):
        '''Shortcut method to do a get request.

        Args:
            uri: string containing endpoint
            data: dict containing the payload
            headers: dict containing the headers

        Returns:
            requests.Response
        '''
        return self.do('get', uri, data, headers)

    def post(self, uri, data=None, headers=None):
        '''Shortcut method to do a post request.

        Args:
            uri: string containing endpoint
            data: dict containing the payload
            headers: dict containing the headers

        Returns:
            requests.Response
        '''
        return self.do('post', uri, data, headers)

    def put(self, uri, data=None, headers=None):
        '''Shortcut method to do a put request.

        Args:
            uri: string containing endpoint
            data: dict containing the payload
            headers: dict containing the headers

        Returns:
            requests.Response
        '''
        return self.do('put', uri, data, headers)


def authenticated(f):
    @click.pass_context
    def decorated_function(ctx, *args, **kwargs):
        if not ctx.obj.get('token'):
            click.echo('Please login using the login command.')
            ctx.exit(1)
        return ctx.invoke(f, ctx, *args, **kwargs)
    return update_wrapper(decorated_function, f)


@click.group()
@click.option('-c', '--config', default='.groceries.yml', type=click.File())
@click.pass_context
def cli(ctx, config):
    '''A command line interface for the Groceries API.

    The main callback function that is executed. It loads the configuration and
    also get the token if it is available.

    Args:
        ctx: click.Context
        config: click.File
    '''
    try:
        with os.fdopen(os.open(TOKEN_PATH, os.O_RDONLY), 'r') as file:
            token = file.readline()
    except:
        token = ''
    ctx.obj = {'api': yaml.load(config.read()).get('api', ''),
               'token': token}


@cli.command()
@click.argument('item')
@authenticated
def add(ctx, item):
    '''Add an item to the groceries list.

    Args:
        ctx: click.Context
        item: string containing item name
    '''
    Item(ctx).add(item)


@cli.command()
@click.argument('item')
@authenticated
def buy(ctx, item):
    '''Buy an item on the groceries list.

    Args:
        ctx: click.Context
        item: string containing item name
    '''
    click.echo('Buying {0}...'.format(item))


@cli.command()
@authenticated
def list(ctx):
    '''List all items on the groceries list.

    Args:
        ctx: click.Context
    '''
    Item(ctx).list()


@cli.command()
@click.option('-u', '--username', prompt=True)
@click.option('-p', '--password', prompt=True, hide_input=True)
@click.pass_context
def login(ctx, username, password):
    '''Authenticate using a username and password.

    Args:
        ctx: click.Context
        username: string containing username
        password: string containing password
    '''
    r = Request(ctx).post('/login',
                          data=json.dumps(dict(username=username, password=password)),
                          headers={'Content-Type':'application/json'})
    if r.status_code is not 200:
        click.echo('Login failed')
        ctx.exit(1)
    with os.fdopen(os.open('.token', os.O_WRONLY | os.O_CREAT, 0600), 'w') as file:
        file.write(r.json().get('token'))
    click.echo('Login successful.')


@cli.command()
@click.pass_context
def logout(ctx):
    '''Logout.

    Args:
        ctx: click.Context
    '''
    if (os.path.exists(TOKEN_PATH)):
        os.remove(TOKEN_PATH)
    click.echo('Logout successful.')


@cli.command()
@click.argument('item')
@authenticated
def remove(ctx, item):
    '''Remove an item from the groceries list.

    Args:
        ctx: click.Context
        item: string containing item name
    '''
    click.echo('Removing {0}...'.format(item))
