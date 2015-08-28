import click
import pytest

from click.testing import CliRunner


@pytest.fixture(scope='function')
def ctx(request):
    ctx = click.Context(click.Command('test'))
    ctx.obj = dict(api='http://localhost', token='secret')
    return ctx


@pytest.fixture(scope='function')
def runner(request):
    return CliRunner()
