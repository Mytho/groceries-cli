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
    if not Item(ctx).create(name):
        click.echo('Unable to add {0} to the list'.format(name))


@cli.command()
@click.argument('name')
@authenticated
def buy(ctx, name):
    '''Buy an item on the groceries list.

    Args:
        ctx: click.Context
        item: string containing item name
    '''
    if not Item(ctx).update(name):
        click.echo('Unable to find {0} on the list.'.format(name))


@cli.command()
@authenticated
def list(ctx):
    '''List all items on the groceries list.

    Args:
        ctx: click.Context
    '''
    for item in Item(ctx).read():
        click.echo('{0}'.format(item.get('name')))


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
    if os.path.exists(TOKEN_PATH):
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
    if not Item(ctx).delete(name):
        click.echo('Unable to find {0} on the list.'.format(name))


class Item(object):

    def __init__(self, ctx):
        '''Create a new instance.

        Item is a sort of repository for the items, a wrapper around the
        Request object for even easier requests that have to do with the
        items on the grocery list.

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
        return None

    def create(self, name):
        '''Add a new item to the list.

        Args:
            name: string containing item name

        Returns:
            True if successful, otherwise False
        '''
        r = self.request.post('/item', data=json.dumps(dict(name=name)))
        return r.status_code == 200

    def read(self):
        '''List the items on the list.

        Returns:
            List of items
        '''
        r = self.request.get('/item')
        return r.json().get('items', [])

    def update(self, name):
        '''Buy an item of the list.

        Args:
            name: string containing item name

        Returns:
            True if successful, otherwise False
        '''
        id = self.id(name)
        if id:
            r = self.request.put('/item/{0}'.format(id))
            return r.status_code == 200
        return False

    def delete(self, name):
        '''Delete an item from the list.

        Args:
            name: string containing item name

        Returns:
            True if successful, otherwise False
        '''
        id = self.id(name)
        if id:
            r = self.request.delete('/item/{0}'.format(id))
            return r.status_code == 200
        return False


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
