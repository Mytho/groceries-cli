from mock import patch

from groceries.core import cli


mock_list = [dict(id=1, name='apples'),
             dict(id=2, name='bananas'),
             dict(id=3, name='citrus')]


class MockResponse(object):

    def __init__(self, status_code=200, json=None):
        self.status_code = status_code
        self.data = json if json else {}

    def json(self):
        return self.data


@patch('groceries.config.Wizard.__call__')
@patch('requests.post', return_value=MockResponse())
def test_add(wizard, post, runner):
    result = runner.invoke(cli, args=['add', 'citrus'])
    assert result.exit_code == 0
    assert result.output == ''


@patch('groceries.config.Wizard.__call__')
@patch('requests.post', return_value=MockResponse(500))
def test_add_failed(wizard, post, runner):
    result = runner.invoke(cli, args=['add', 'citrus'])
    assert result.exit_code == 1
    assert 'citrus' in result.output


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
@patch('requests.put', return_value=MockResponse(403))
def test_buy_failed(wizard, get, put, runner):
    result = runner.invoke(cli, args=['buy', 'citrus'])
    assert result.exit_code == 1
    assert 'citrus' in result.output


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
@patch('requests.delete', return_value=MockResponse(403))
def test_delete_failed(wizard, get, delete, runner):
    result = runner.invoke(cli, args=['remove', 'citrus'])
    assert result.exit_code == 1
    assert 'citrus' in result.output
