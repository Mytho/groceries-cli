mock_list = [dict(id=1, name='apples'),
             dict(id=2, name='bananas'),
             dict(id=3, name='citrus')]


class MockResponse(object):

    def __init__(self, status_code=200, json=None):
        self.status_code = status_code
        self.data = json if json else {}

    def json(self):
        return self.data
