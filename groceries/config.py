import click
import os
import requests


def validate(ctx, param, values, tries=0):
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
                return validate(ctx, param, values, tries)
            click.echo('To many tries')
            ctx.exit(1)
        with os.fdopen(os.open(values, os.O_WRONLY | os.O_CREAT, 0600), 'w') as file:
            file.write('api: {0}'.format(url))
    return os.fdopen(os.open(values, os.O_RDONLY), 'r')
