import asyncio
from aiohttp import ClientSession
import json
import challonge
from challonge import api_base, error
import copy

class Match:

    UPDATE_FIELDS = ['scores_csv', 'winner_id', 'player1_votes', 'player2_votes']

    def __init__(self, data=None):
        for k in data['match']:
            setattr(self, k, data['match'][k])

        self.original = copy.copy(self)
