import click

from config import Wizard
from utils import Item


@click.group()
@click.option('-c', '--config', default='.groceries.yml', callback=Wizard())
@click.pass_context
def cli(ctx, config):
    '''A command line interface for the Groceries API.

    The main callback function that is executed. It loads the configuration and
    also get the token if it is available.

    Args:
        ctx: click.Context
        config: groceries.config.Config
    '''
    ctx.obj = config


@cli.command()
@click.argument('name')
@click.pass_context
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
@click.pass_context
def buy(ctx, name):
    '''Buy an item on the groceries list.

    Args:
        ctx: click.Context
        item: string containing item name
    '''
    if not Item(ctx).update(name):
        click.echo('Unable to find {0} on the list.'.format(name))


@cli.command()
@click.pass_context
def list(ctx):
    '''List all items on the groceries list.

    Args:
        ctx: click.Context
    '''
    for item in Item(ctx).read():
        click.echo('{0}'.format(item.get('name')))


@cli.command()
@click.argument('name')
@click.pass_context
def remove(ctx, name):
    '''Remove an item from the groceries list.

    Args:
        ctx: click.Context
        item: string containing item name
    '''
    if not Item(ctx).delete(name):
        click.echo('Unable to find {0} on the list.'.format(name))
