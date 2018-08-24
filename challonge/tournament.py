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

    def base_url(self):
        return (api_base + 'tournaments/' + str(self.id))

    def update_object(self, data):
        for k in data['tournament']:
            if k == 'participants':
                setattr(self, k, self.build_participants(data['tournament']['participants']))
            elif k == 'matches':
                setattr(self, k, self.build_participants(data['tournament']['matches']))
            else:
                setattr(self, k, data['tournament'][k])

        self.original = copy.copy(self)

        return self

    async def async_init(self, tid, session, include_participants=False, include_matches=False):
        url = api_base + 'tournaments/' + str(tid) + '.json?'
        if include_participants: url += 'include_participants=1&'
        if include_matches: url += 'include_matches=1&'

        async with session.get(url, params={'api_key': challonge.api_key}) as r:
            if r.status == 200:
                data = await r.json()
                return self.update_object(data)
            else:
                error.raise_error(r)

    async def update(self, session):
        params = { 'api_key' : challonge.api_key , 'tournament' : {} }

        for k in self.UPDATE_FIELDS:
            if getattr(self, k) != getattr(self.original, k):
                params['tournament'][k] = getattr(self, k)
        
        async with session as sess:
            r = await sess.put(api_base + 'tournaments/' + str(self.id) + '.json?api_key=' + challonge.api_key, json=params)
            if r.status == 200:
                data = r.json()
                return self.update_object(data)
            else:
                error.raise_error(r)

    async def delete(self, session):
        return client.delete(self.base_url() + '.json')

        async with session as sess:
            r = await sess.delete(self.base_url() + '.json', params={'api_key': challonge.api_key})
            if r.status == 200:
                return True
            else:
                error.raise_error(r)
    
    async def svg(self, session):
        async with session as sess:
            async with sess.get('https://challonge.com/' + str(self.url) + '.svg', params={'api_key': challonge.api_key}) as r:
                if r.status == 200:
                    return r.text()
                else:
                    error.raise_error(r)

    async def get_participants(self, session, include_matches=False, reload_array=False):
        url = self.base_url() + '/participants.json'
        if include_matches: url += '?include_matches=1'

        async with session as sess:
            async with sess.get(url, params={'api_key': challonge.api_key}) as r:
                if r.status == 200:
                    data = await r.json()
                    plist = self.build_participants(data)
                    if reload_array:
                        setattr(self, 'participants', plist)
                    return plist
                else:
                    error.raise_error(r)

    def get_participant(self, pid, include_matches=False, session=None, loop=None):
        client = Client(session=session, loop=loop)
        data = client.get(self.base_url() + '/participants/' + str(pid) + '.json')
        return Participant(data=data)

    def add_participant(self, data=None, session=None, loop=None):
        client = Client(session=session, loop=loop)
        data = client.post(self.base_url() + '/participants.json', data)
        return Participant(data=data)

    def bulk_add_participants(self, data=None, session=None, loop=None):
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
        return self.build_matches(data)

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

