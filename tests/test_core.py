from mock import patch

from groceries.core import cli
from tests import mock_list, MockResponse


@patch('requests.get', side_effect=[MockResponse(),
                                    MockResponse(json=dict(items=mock_list))])
@patch('requests.post', return_value=MockResponse(json=dict(token='secret')))
@patch('getpass.getpass', new=raw_input)
def test_wizard(get, post, runner):
    with runner.isolated_filesystem():
        result = runner.invoke(cli, args=['list'],
                               input='http://localhost\nuser\npass\n')
        assert result.exit_code == 0


@patch('requests.get', return_value=MockResponse(404))
def test_wizard_to_many_tries(get, runner):
    with runner.isolated_filesystem():
        result = runner.invoke(cli, args=['list'], input='http://localhost\n')
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
@patch('requests.get',
       return_value=MockResponse(json=dict(items=mock_list)))
@patch('requests.put', return_value=MockResponse())
def test_buy(wizard, get, put, runner):
    result = runner.invoke(cli, args=['buy', 'citrus'])
    assert result.exit_code == 0
    assert result.output == ''


@patch('groceries.config.Wizard.__call__')
@patch('requests.get',
       return_value=MockResponse(json=dict(items=mock_list)))
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
