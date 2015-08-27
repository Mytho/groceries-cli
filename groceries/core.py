import click
import json
import requests
import os
import yaml

from functools import update_wrapper


TOKEN_PATH = '.token'


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
@click.argument('name')
@authenticated
def add(ctx, name):
    '''Add an item to the groceries list.

    Args:
        ctx: click.Context
        item: string containing item name
    '''
    Item(ctx).add(name)


@cli.command()
@click.argument('name')
@authenticated
def buy(ctx, name):
    '''Buy an item on the groceries list.

    Args:
        ctx: click.Context
        item: string containing item name
    '''
    Item(ctx).buy(name)


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


@cli.command()
@click.pass_context
def logout(ctx):
    '''Logout.

    Args:
        ctx: click.Context
    '''
    if (os.path.exists(TOKEN_PATH)):
        os.remove(TOKEN_PATH)


@cli.command()
@click.argument('name')
@authenticated
def remove(ctx, name):
    '''Remove an item from the groceries list.

    Args:
        ctx: click.Context
        item: string containing item name
    '''
    Item(ctx).remove(name)


class Item(object):

    def __init__(self, ctx):
        '''Create a new instance.

        Args:
            ctx: click.Context
        '''
        self.request = Request(ctx)

    def id(self, name):
        '''Get the id of an item when a name is provided.

        Args:
            name: string containing item name

        Returns:
            id of the item as an int, None of no item was found
        '''
        r = self.request.get('/item')
        for item in r.json().get('items'):
            if item.get('name') == name:
                return item.get('id')
        click.echo('Unable to find item \'{0}\''.format(name))
        return None

    def add(self, name):
        '''Add a new item to the list.

        Args:
            name: string containing item name
        '''
        self.request.post('/item', data=json.dumps(dict(name=name)))

    def buy(self, name):
        '''Buy an item of the list.

        Args:
            name: string containing item name
        '''
        id = self.id(name)
        if id:
            self.request.put('/item/{0}'.format(id))

    def list(self):
        '''List the items on the list.'''
        r = self.request.get('/item')
        for item in r.json().get('items'):
            click.echo('{0}'.format(item.get('name')))

    def remove(self, name):
        '''Delete an item from the list.

        Args:
            name: string containing item name
        '''
        id = self.id(name)
        if id:
            self.request.delete('/item/{0}'.format(id))


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
            data: dict containing request payload
            headers: dict containing request headers

        Returns:
            requests.Response
        '''
        return self.do('delete', uri, data, headers)

    def do(self, method, uri, data=None, headers=None):
        '''Do a requests using the requests library.

        Args:
            method: string containing HTTP method name
            uri: string containing endpoint
            data: dict containing request payload
            headers: dict containing request headers

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
            data: dict containing request payload
            headers: dict containing request headers

        Returns:
            requests.Response
        '''
        return self.do('get', uri, data, headers)

    def post(self, uri, data=None, headers=None):
        '''Shortcut method to do a post request.

        Args:
            uri: string containing endpoint
            data: dict containing request payload
            headers: dict containing request headers

        Returns:
            requests.Response
        '''
        return self.do('post', uri, data, headers)

    def put(self, uri, data=None, headers=None):
        '''Shortcut method to do a put request.

        Args:
            uri: string containing endpoint
            data: dict containing request payload
            headers: dict containing request headers

        Returns:
            requests.Response
        '''
        return self.do('put', uri, data, headers)
