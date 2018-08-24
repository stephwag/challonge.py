import asyncio
from aiohttp import ClientSession
import json
import challonge
from challonge import api_base, error
from collections import namedtuple
import copy

class Participant:

    UPDATE_FIELDS = ['name', 'challonge_username', 'email', 'seed', 'misc']

    def __init__(self, data=None):
        for k in data:
            setattr(self, k, data[k])

        self.original = copy.copy(self)

    def base_url(self):
        return api_base + 'tournaments/' + str(self.tournament_id) + '/participants/' + str(self.id)

    def tournament_url(self):
        return api_base + 'tournaments/' + str(self.tournament_id)

    def update_object(self, data):
        for k in data:
            if k == 'matches':
                setattr(self, k, self.build_participants(data['matches']))
            else:
                setattr(self, k, data[k])

        self.original = copy.copy(self)

        return self

    def update_params(self):
        params = { 'api_key' : challonge.api_key , 'participant' : {} }
        for k in self.UPDATE_FIELDS:
            if getattr(self, k) != getattr(self.original, k):
                params['participant'][k] = getattr(self, k)
        return params

    # Add participant to the tournament
    async def create(self, session):
        params = self.update_params()
        if 'id' in params: params.pop('id', None)
        async with session.post(self.base_url() + '.json', json=params) as r:
            if r.status == 200:
                data = await r.json()
                return self.update_object(data['participant'])
            else:
                error.raise_error(r)

    async def update(self, session):
        params = self.update_params()
        
        async with session.put(self.base_url() + '.json', json=params) as r:
            if r.status == 200:
                data = await r.json()
                return self.update_object(data['participant'])
            else:
                error.raise_error(r)

    async def get(self, session, include_matches=False):
        async with session.get(self.base_url() + '.json', params={'api_key': challonge.api_key}) as r:
            if r.status == 200:
                data = await r.json()
                return Participant(data=data)
            else:
                error.raise_error(r)

    # Get a participant by searching for one with a value set in the misc field
    # This is not part of the API itself but it's helpful to have.
    async def get_by_misc(self, session, misc, include_matches=False):
        async with session.get(self.tournament_url() + '/participants.json', params={'api_key': challonge.api_key}) as r:
            if r.status == 200:
                data = await r.json()

                for p in data:
                    if p['participant']['misc'] == misc:
                        return Participant(data=p['participant'])

                return None
            else:
                error.raise_error(r)

    # Remove participant from the tournament
    async def delete(self, session):
        async with session.delete(self.base_url() + '.json') as r:
            if r.status == 200:
                return True
            else:
                error.raise_error(r)

    async def checkin(self, session):
        async with session.post(self.base_url() + '/check_in.json', json={ 'api_key' : challonge.api_key }) as r:
            if r.status == 200:
                return True
            else:
                error.raise_error(r)

    async def undo_checkin(self, session):
        async with session.post(self.base_url() + '/undo_check_in.json', json={ 'api_key' : challonge.api_key }) as r:
            if r.status == 200:
                return True
            else:
                error.raise_error(r)

    # Get the next match or optional id
    async def winner(self):
        pass       