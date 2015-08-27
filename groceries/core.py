import click
import os
import requests
import yaml

from functools import update_wrapper

from utils import Item


def authenticated(f):
    @click.pass_context
    def decorated_function(ctx, *args, **kwargs):
        if not ctx.obj.get('token'):
            ctx.fail('Please login using the login command.')
        return ctx.invoke(f, ctx, *args, **kwargs)
    return update_wrapper(decorated_function, f)


def validate_config(ctx, param, values, tries=0):
    '''Validates if config file exists, if not create a configuration file.

    Args:
        ctx: click.Context
        param: click.Param
        values: parameter value
        tries: number of tries

    Returns:
        Open file object
    '''
    if not os.path.exists(values):
        if tries == 0:
            click.echo('No config file found. Let\'s create it:')
        url = raw_input('What is the API\'s base URL? ')
        try:
            if not requests.get(url).status_code != 200:
                raise Exception()
        except:
            tries += 1
            if tries < 3:
                click.echo('Invalid URL supplied')
                return validate_config(ctx, param, values, tries)
            click.echo('To many tries')
            ctx.exit(1)
        with os.fdopen(os.open(values, os.O_WRONLY | os.O_CREAT, 0600), 'w') as file:
            file.write('api: {0}'.format(url))
    return os.fdopen(os.open(values, os.O_RDONLY), 'r')


@click.group()
@click.option('-c', '--config', default='.groceries.yml', callback=validate_config)
@click.pass_context
def cli(ctx, config):
    '''A command line interface for the Groceries API.

    The main callback function that is executed. It loads the configuration and
    also get the token if it is available.

    Args:
        ctx: click.Context
        config: click.File
    '''
    ctx.obj = yaml.load(config.read())


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
