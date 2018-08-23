import asyncio
from aiohttp import ClientSession
import json
import challonge
from challonge import error

class Client:
    def __init__(self, session=None, loop=None):
        if session is None:
            session = ClientSession()
        if loop is None:
            loop = asyncio.get_event_loop()

        self.session = session
        self.loop = loop

    def raise_error(self, r):
        if r.status == 401:
            raise error.AuthenticationError(status=r.status,message="Unauthorized (Invalid API key or insufficient permissions)",request=r)
        elif r.status == 404:
            raise error.NotFoundError(status=r.status,message="Object not found within your account scope",request=r)
        elif r.status == 406:
            raise error.InvalidFormatError(status=r.status,message="Requested format is not supported - request JSON or XML only",request=r)
        elif r.status == 422:
            raise error.ValidationError(status=r.status,message="Validation error(s) for create or update method",request=r,json_body=r.json())
        else:
            raise error.ServerError(status=r.status,message="Something went wrong on Challonge's end. If you continually receive this, please contact them.",request=r)

    def get(self, url, params={}, response_type='json'):
        return self.loop.run_until_complete(self.async_get(url, response_type=response_type))

    def put(self, url, params, response_type='json'):
        return self.loop.run_until_complete(self.async_put(url, params, response_type=response_type))

    def post(self, url, params, response_type='json'):
        return self.loop.run_until_complete(self.async_post(url, params, response_type=response_type))

    def delete(self, url, response_type='json'):
        return self.loop.run_until_complete(self.async_delete(url, response_type=response_type))

    async def async_get(self, url, params={}, response_type='json'):
        async with self.session as session:
            params.update({ 'api_key' : challonge.api_key })
            async with session.get(url, params=params) as r:
                if r.status == 200:
                    if response_type == 'json':
                        return await r.json()
                    elif response_type == 'text':
                        return await r.text()
                    else:
                        return await r.read()
                else:
                    self.raise_error(r)

    async def async_delete(self, url, response_type='json'):
        async with self.session as session:
            async with session.delete(url, params={'api_key' : challonge.api_key}) as r:
                if r.status == 200:
                    if response_type == 'json':
                        return await r.json()
                    elif response_type == 'text':
                        return await r.text()
                    else:
                        return await r.read()
                else:
                    self.raise_error(r)

    async def async_put(self, url, params, response_type='json'):
        async with self.session as session:
            params.update({ 'api_key' : challonge.api_key })
            async with session.put(url, json=params) as r:
                if r.status == 200:
                    if response_type == 'json':
                        return await r.json()
                    elif response_type == 'text':
                        return await r.text()
                    else:
                        return await r.read()
                else:
                    self.raise_error(r)

    async def async_post(self, url, params, response_type='json'):
        async with self.session as session:
            params.update({ 'api_key' : challonge.api_key })
            async with session.post(url, json=params) as r:
                if r.status == 200:
                    if response_type == 'json':
                        return await r.json()
                    elif response_type == 'text':
                        return await r.text()
                    else:
                        return await r.read()
                else:
                    self.raise_error(r)
