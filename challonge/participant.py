import asyncio
from aiohttp import ClientSession
import json
import challonge
from challonge import api_base, error, Client
from collections import namedtuple
import copy

class Participant:

    UPDATE_FIELDS = ['name', 'challonge_username', 'email', 'seed', 'misc']

    def __init__(self, data=None):
        for k in data['participant']:
            setattr(self, k, data['participant'][k])

        self.original = copy.copy(self)

    def base_url(self):
        return api_base + 'tournaments/' + str(self.tournament_id) + '/participants/' + str(self.id)

    def tournament_url(self):
        return api_base + 'tournaments/' + str(self.tournament_id)

    def update(self, session=None, loop=None):
        client = Client(session=session, loop=loop)

        params = { 'participant' : {} }

        for k in self.UPDATE_FIELDS:
            if hasattr(self, k):
                if getattr(self, k) != getattr(self.original, k):
                    params['participant'][k] = getattr(self, k)
        
        data = client.put(self.base_url() + '.json', params)

        if data is not None:
            for k in data['participant']:
                setattr(self, k, data['participant'][k])

        self.original = copy.copy(self)

    # Remove participant from the tournament
    def remove(self, session=None, loop=None):
        client = Client(session=session, loop=loop)
        return client.delete(self.base_url() + '.json')

    # Add participant from the tournament
    def add(self, session=None, loop=None):
        client = Client(session=session, loop=loop)

        params = { 'participant' : {} }

        for k in self.UPDATE_FIELDS:
            if hasattr(self, k):
                params['participant'][k] = getattr(self, k)

        data = client.post(self.tournament_url() + '/participants.json', params)

        if data is not None:
            for k in data['participant']:
                setattr(self, k, data['participant'][k])

        self.original = copy.copy(self)

    def checkin(self, session=None, loop=None):
        client = Client(session=session, loop=loop)
        return client.delete(self.base_url() + '/check_in.json')

    def undo_checkin(self, session=None, loop=None):
        client = Client(session=session, loop=loop)
        return client.delete(self.base_url() + '/undo_check_in.json')

    # Get the next match or optional id
    def winner(self):
        pass       