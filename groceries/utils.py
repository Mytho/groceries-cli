import json
import requests


class Item(object):

    def __init__(self, ctx):
        '''Create a new instance.

        Wraps a Request object and serves as a sort of repository for easier
        requests to retreive data.

        Args:
            ctx: click.Context
        '''
        self.request = Request(ctx)

    def id(self, name):
        '''Get the id of an item when a name is provided.

        Args:
            name: string containing item name

        Returns:
            id of the item as an int, None of no item was found
        '''
        r = self.request.get('/item')
        for item in r.json().get('items', []):
            if item.get('name') == name:
                return item.get('id')
        return None

    def create(self, name):
        '''Add a new item to the list.

        Args:
            name: string containing item name

        Returns:
            True if successful, otherwise False
        '''
        r = self.request.post('/item', data=json.dumps(dict(name=name)))
        return r.status_code == 200

    def read(self):
        '''List the items on the list.

        Returns:
            List of items
        '''
        r = self.request.get('/item')
        return r.json().get('items', [])

    def update(self, name):
        '''Buy an item of the list.

        Args:
            name: string containing item name

        Returns:
            True if successful, otherwise False
        '''
        id = self.id(name)
        if id:
            r = self.request.put('/item/{0}'.format(id))
            return r.status_code == 200
        return False

    def delete(self, name):
        '''Delete an item from the list.

        Args:
            name: string containing item name

        Returns:
            True if successful, otherwise False
        '''
        id = self.id(name)
        if id:
            r = self.request.delete('/item/{0}'.format(id))
            return r.status_code == 200
        return False


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
