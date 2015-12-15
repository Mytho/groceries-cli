import click

from groceries import __version__
from groceries.config import Wizard
from groceries.utils import Item


@click.group()
@click.option('-c', '--config', default='.groceries.yml',
              envvar='GROCERIES_CONFIG', callback=Wizard(),
              help='Location of the configuration file.')
@click.pass_context
def cli(ctx, config):
    '''A command line interface for the Groceries API.'''
    ctx.obj = config


@cli.command()
def version():
    '''Display the version of this tool.'''
    click.echo('groceries-cli/{}'.format(__version__))


@cli.command()
@click.argument('name')
@click.pass_context
def add(ctx, name):
    '''Add an item to the groceries list.'''
    if not Item(ctx).create(name):
        click.echo('Unable to add {0} to the list'.format(name))
        ctx.exit(1)


@cli.command()
@click.argument('name')
@click.pass_context
def buy(ctx, name):
    '''Buy an item on the groceries list.'''
    if not Item(ctx).update(name):
        click.echo('Unable to find {0} on the list.'.format(name))
        ctx.exit(1)


@cli.command()
@click.pass_context
def list(ctx):
    '''List all items on the groceries list.'''
    for item in Item(ctx).read():
        click.echo('{0}'.format(item.get('name')))


@cli.command()
@click.argument('name')
@click.pass_context
def remove(ctx, name):
    '''Remove an item from the groceries list.'''
    if not Item(ctx).delete(name):
        click.echo('Unable to find {0} on the list.'.format(name))
        ctx.exit(1)
