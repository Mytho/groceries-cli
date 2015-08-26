import click
import json
import requests
import os
import yaml


@click.group()
@click.option('-c', '--config', default='.groceries.yml', type=click.File())
@click.pass_context
def cli(ctx, config):
    '''A command line interface for the Groceries API.'''
    try:
        with os.fdopen(os.open('.token', os.O_RDONLY), 'r') as file:
            token = file.readline()
    except:
        token = ''
    ctx.obj = {'CONFIG': yaml.load(config.read()),
               'TOKEN': token}


@cli.command()
def buy():
    '''Buy an item on the groceries list.'''
    click.echo('Buying grocery...')


@cli.command()
def add():
    '''Add an item to the groceries list.'''
    click.echo('Adding grocery...')


@cli.command()
def list():
    '''List all items on the groceries list.'''
    click.echo('Listing groceries...')


@cli.command()
def remove():
    '''Remove an item from the groceries list.'''
    click.echo('Removing grocery...')


@cli.command()
@click.option('-u', '--username', prompt=True)
@click.option('-p', '--password', prompt=True, hide_input=True)
@click.pass_context
def login(ctx, username, password):
    '''Authenticate using a username and password.'''
    r = requests.post('{0}{1}'.format(ctx.obj['CONFIG'].get('api'), '/login'),
                      data=json.dumps(dict(username=username, password=password)),
                      headers={'Content-Type':'application/json'})
    if r.status_code is not 200:
        click.echo('Login failed')
        ctx.exit(1)
    with os.fdopen(os.open('.token', os.O_WRONLY | os.O_CREAT, 0600), 'w') as file:
        file.write(r.json().get('token'))
    click.echo('Login successfull')
