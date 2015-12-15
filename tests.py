import click
import os
import pytest

from click.testing import CliRunner
from mock import patch
from six.moves import input

from groceries.core import cli

del os.environ['GROCERIES_CONFIG']

mock_list = [
    dict(id=1, name='apples'),
    dict(id=2, name='bananas'),
    dict(id=3, name='citrus')]


class MockResponse(object):

    def __init__(self, status_code=200, json=None):
        self.status_code = status_code
        self.data = json if json else {}

    def json(self):
        return self.data


@pytest.fixture(scope='function')
def runner(request):
    return CliRunner()


@patch('requests.get', side_effect=[
    MockResponse(), MockResponse(json=dict(items=mock_list))])
@patch('requests.post', return_value=MockResponse(json=dict(token='secret')))
@patch('getpass.getpass', new=input)
def test_wizard(get, post, runner):
    with runner.isolated_filesystem():
        result = runner.invoke(
            cli, args=['list'], input='http://localhost\nuser\npass\n')
        assert result.exit_code == 0


@patch('requests.get', return_value=MockResponse(404))
def test_wizard_to_many_tries(get, runner):
    with runner.isolated_filesystem():
        result = runner.invoke(
            cli, args=['list'], input='http://localhost\n')
        args, kwargs = get.call_args
        print(args, kwargs)
        assert result.exit_code == 1


@patch('requests.get', side_effect=KeyboardInterrupt('Interrupt!'))
def test_wizard_keyboard_interrupt(get, runner):
    with runner.isolated_filesystem():
        result = runner.invoke(cli, args=['list'], input='http://localhost\n')
        assert result.exit_code == 1


@patch('groceries.config.Wizard.__call__')
@patch('requests.post', return_value=MockResponse())
def test_add(wizard, post, runner):
    result = runner.invoke(cli, args=['add', 'dates'])
    assert result.exit_code == 0
    assert result.output == ''


@patch('groceries.config.Wizard.__call__')
@patch('requests.post', return_value=MockResponse(500))
def test_add_failed(wizard, post, runner):
    result = runner.invoke(cli, args=['add', 'dates'])
    assert result.exit_code == 1
    assert 'dates' in result.output


@patch('groceries.config.Wizard.__call__')
@patch('requests.get', return_value=MockResponse(json=dict(items=mock_list)))
@patch('requests.put', return_value=MockResponse())
def test_buy(wizard, get, put, runner):
    result = runner.invoke(cli, args=['buy', 'citrus'])
    assert result.exit_code == 0
    assert result.output == ''


@patch('groceries.config.Wizard.__call__')
@patch('requests.get', return_value=MockResponse(json=dict(items=mock_list)))
def test_buy_failed(wizard, get, runner):
    result = runner.invoke(cli, args=['buy', 'cucumber'])
    assert result.exit_code == 1
    assert 'cucumber' in result.output


@patch('groceries.config.Wizard.__call__')
@patch('requests.get', return_value=MockResponse(json=dict(items=mock_list)))
def test_list(wizard, get, runner):
    result = runner.invoke(cli, args=['list'])
    assert result.exit_code == 0
    assert result.output == 'apples\nbananas\ncitrus\n'


@patch('groceries.config.Wizard.__call__')
@patch('requests.get', return_value=MockResponse(json=dict(items=mock_list)))
@patch('requests.delete', return_value=MockResponse())
def test_delete(wizard, get, delete, runner):
    result = runner.invoke(cli, args=['remove', 'citrus'])
    assert result.exit_code == 0
    assert result.output == ''


@patch('groceries.config.Wizard.__call__')
@patch('requests.get', return_value=MockResponse(json=dict(items=mock_list)))
def test_delete_failed(wizard, get, runner):
    result = runner.invoke(cli, args=['remove', 'cucumber'])
    assert result.exit_code == 1
    assert 'cucumber' in result.output
