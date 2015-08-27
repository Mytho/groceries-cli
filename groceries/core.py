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
@authenticated
def add(ctx):
    '''Add an item to the groceries list.'''
    click.echo('Adding grocery...')


@cli.command()
@authenticated
def buy(ctx):
    '''Buy an item on the groceries list.'''
    click.echo('Buying grocery...')


@cli.command()
@authenticated
def list(ctx):
    '''List all items on the groceries list.'''
    r = requests.get('{0}{1}'.format(ctx.obj.get('api'), '/item'),
                     headers={'X-Auth-Token': ctx.obj.get('token')})
    for item in r.json().get('items'):
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
    r = requests.post('{0}{1}'.format(ctx.obj.get('api'), '/login'),
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
@authenticated
def remove(ctx):
    '''Remove an item from the groceries list.'''
    click.echo('Removing grocery...')
