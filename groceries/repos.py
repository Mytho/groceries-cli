import json
import os

from groceries.wrappers import Request


class Repo(object):

    def __init__(self, ctx):
        '''Create a new instance.

        A Repo wraps a Request object and serves as a sort of repository for a
        specific type of data.

        Args:
            ctx: click.Context
        '''
        self.request = Request(ctx)


class Item(Repo):

    def id(self, name):
        '''Get the id of an item when a name is provided.

        Args:
            name: string containing item name

        Returns:
            id of the item as an int, None of no item was found
        '''
        r = self.request.get('/item')
        for item in r.json().get('items'):
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


class Token(Repo):

    TOKEN_PATH = '.token'

    def create(self, username, password):
        '''Login to allow manipulation of the groceries list.

        Args:
            username: string containing username
            password: string containing password

        Returns:
            True if login was successful, False otherwise
        '''
        data = json.dumps({'username': username, 'password': password})
        headers = {'Content-Type': 'application/json'}
        r = self.request.post('/login', data=data, headers=headers)
        if r.status_code == 200:
            with os.fdopen(os.open(self.TOKEN_PATH, os.O_WRONLY | os.O_CREAT, 0600), 'w') as file:
                file.write(r.json().get('token'))
                return True
        return False

    def read(self):
        '''Get the token.

        Returns:
            string containing token
        '''
        try:
            with os.fdopen(os.open(self.TOKEN_PATH, os.O_RDONLY), 'r') as file:
                return file.readline()
        except:
            return ''

    def delete(self):
        '''Logout.'''
        if os.path.exists(self.TOKEN_PATH):
            os.remove(self.TOKEN_PATH)
