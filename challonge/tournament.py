import asyncio
from aiohttp import ClientSession
import json
import challonge
from challonge import api_base, error, Client, Participant, Match
from collections import namedtuple
import copy

class Tournament:

    UPDATE_FIELDS = [
            'name', 'tournament_type', 'url', 'subdomain', 'description', 'open_signup', 'hold_third_place_match',
            'pts_for_match_win', 'pts_for_match_tie', 'pts_for_game_win', 'pts_for_game_tie', 'pts_for_bye', 
            'swiss_rounds', 'ranked_by', 'rr_pts_for_match_win', 'rr_pts_for_match_tie', 'rr_pts_for_game_win',
            'rr_pts_for_game_tie', 'accept_attachments', 'hide_forum', 'show_rounds', 'private', 'notify_users_when_matches_open',
            'notify_users_when_the_tournament_ends', 'sequential_pairings', 'signup_cap', 
            'start_at', 'check_in_duration', 'grand_finals_modifier'
        ]

    def __init__(self, tid, session=None, loop=None, include_participants=False, include_matches=False):
        client = Client(session=session, loop=loop)
        data = client.get(api_base + 'tournaments/' + str(tid) + '.json')
        for k in data['tournament']:
            setattr(self, k, data['tournament'][k])

        self.original = copy.copy(self)

    def base_url(self):
        return (api_base + 'tournaments/' + str(self.id))

    def update(self, session=None, loop=None):
        params = { 'api_key' : challonge.api_key , 'tournament' : {} }
        client = Client(session=session, loop=loop)

        for k in UPDATE_FIELDS:
            if getattr(self, k) != getattr(self.original, k):
                params['tournament'][k] = getattr(self, k)
        
        data = client.put(self.base_url() + '.json', params)

        if data is not None:
            for k in data['tournament']:
                setattr(self, k, data['tournament'][k])

        self.original = copy.copy(self)

    def delete(self, session=None, loop=None):
        client = Client(session=session, loop=loop)
        return client.delete(self.base_url() + '.json')

    def get(self, session=None, loop=None, refresh=True):
        client = Client(session=session, loop=loop)
        data = client.get(self.base_url() + '.json')
        if refresh:
            for k in data['tournament']:
                setattr(self, k, data['tournament'][k])
            self.original = copy.copy(self)
            return self
        else:
            return data
    
    def svg(self):
        client = Client(session=session, loop=loop)
        return client.get('https://challonge.com/' + str(self.id) + '.svg', response_type='text')

    def participants(self, include_matches=False, session=None, loop=None):
        client = Client(session=session, loop=loop)
        data = client.get(self.base_url() + '/participants.json')
        return self.build_participants(data)

    def participant(self, pid, include_matches=False, session=None, loop=None):
        client = Client(session=session, loop=loop)
        data = client.get(self.base_url() + '/participants/' + str(pid) + '.json')
        print(data)
        return Participant(data=data)

    def add_participant(self, data=None, session=None, loop=None):
        client = Client(session=session, loop=loop)
        data = client.post(self.base_url() + '/participants.json', data)
        return Participant(data=data)

    def clear_participants(self):
        client = Client(session=session, loop=loop) 
        return client.delete(self.base_url() + '/participants/clear.json')

    def randomize_participants(self):
        client = Client(session=session, loop=loop) 
        return client.post(self.base_url() + '/participants/randomize.json')

    def matches(self, include_attachments=False, session=None, loop=None):
        client = Client(session=session, loop=loop)
        data = client.get(self.base_url() + '/matches.json')
        return build_matches(data)

    def match(self, mid, include_attachments=False, session=None, loop=None):
        client = Client(session=session, loop=loop)
        data = client.get(self.base_url() + '/matches/' + str(mid) + '.json')
        return Match(data=data)

    def build_participants(self, data={}):
        result = []
        for p in data: result.append(Participant(data=p))
        return result

    def build_matches(self, data={}):
        result = []
        for p in data: result.append(Match(data=p))
        return result

    @classmethod
    def list(self, session=None, loop=None):
        client = Client(session=session, loop=loop)
        return client.get(api_base + '/tournaments.json')

    @classmethod
    def create(self, session=None, loop=None, params={}):
        p = { 'api_key' : challonge.api_key , 'tournament' : params }
        client = Client(session=session, loop=loop)
        return client.post(api_base + '/tournaments.json', params=p)

