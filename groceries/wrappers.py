import requests


class Request(object):

    def __init__(self, ctx):
        '''Create a new instance.

        Args:
            ctx: click.Context
        '''
        self.ctx = ctx

    def delete(self, uri, data=None, headers=None):
        '''Shortcut method to do a delete request.

        Args:
            uri: string containing endpoint
            data: dict containing request payload
            headers: dict containing request headers

        Returns:
            requests.Response
        '''
        return self.do('delete', uri, data, headers)

    def do(self, method, uri, data=None, headers=None):
        '''Do a request using the requests library.

        Args:
            method: string containing HTTP method name
            uri: string containing endpoint
            data: dict containing request payload
            headers: dict containing request headers

        Returns:
            requests.Response
        '''
        if headers is None:
            headers = {'X-Auth-Token': self.ctx.obj.get('token').strip(),
                       'Content-Type': 'application/json'}
        url = '{0}{1}'.format(self.ctx.obj.get('api'), uri)
        return getattr(requests, method)(url, data=data, headers=headers)

    def get(self, uri, data=None, headers=None):
        '''Shortcut method to do a get request.

        Args:
            uri: string containing endpoint
            data: dict containing request payload
            headers: dict containing request headers

        Returns:
            requests.Response
        '''
        return self.do('get', uri, data, headers)

    def post(self, uri, data=None, headers=None):
        '''Shortcut method to do a post request.

        Args:
            uri: string containing endpoint
            data: dict containing request payload
            headers: dict containing request headers

        Returns:
            requests.Response
        '''
        return self.do('post', uri, data, headers)

    def put(self, uri, data=None, headers=None):
        '''Shortcut method to do a put request.

        Args:
            uri: string containing endpoint
            data: dict containing request payload
            headers: dict containing request headers

        Returns:
            requests.Response
        '''
        return self.do('put', uri, data, headers)
