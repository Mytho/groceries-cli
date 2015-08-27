import click
import yaml

from functools import update_wrapper

from repos import Item, Token


def authenticated(f):
    @click.pass_context
    def decorated_function(ctx, *args, **kwargs):
        if not ctx.obj.get('token'):
            ctx.fail('Please login using the login command.')
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
    ctx.obj = {'api': yaml.load(config.read()).get('api', ''),
               'token': Token(ctx).read()}


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
    if not Token(ctx).create(username, password):
        click.echo('Incorrect username and/or password supplied')


@cli.command()
@click.pass_context
def logout(ctx):
    '''Logout.

    Args:
        ctx: click.Context
    '''
    Token(ctx).delete()


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
