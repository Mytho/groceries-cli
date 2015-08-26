import click
import yaml


CONFIG = dict(api='http://localhost',
              auth=dict(username='user', password='pass'))


@click.group()
@click.option('-c', '--config', default='.groceries.yml', type=click.File())
def cli(config):
    '''A command line interface for the Groceries API.'''
    CONFIG = yaml.load(config.read())


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
