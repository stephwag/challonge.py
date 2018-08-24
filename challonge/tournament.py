import asyncio
from aiohttp import ClientSession
import json
import challonge
from challonge import api_base, error, Participant, Match
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

    def update_params(self):
        params = { 'api_key' : challonge.api_key , 'tournament' : {} }
        for k in self.UPDATE_FIELDS:
            if getattr(self, k) != getattr(self.original, k):
                params['tournament'][k] = getattr(self, k)
        return params

    def __init__(self, data=None):
        if data is not None:
            return self.update_object(data=data)

    async def get(self, session, tid, include_participants=False, include_matches=False):
        url = api_base + 'tournaments/' + str(tid) + '.json?'
        if include_participants: url += 'include_participants=1&'
        if include_matches: url += 'include_matches=1&'

        async with session.get(url, params={'api_key': challonge.api_key}) as r:
            if r.status == 200:
                data = await r.json()
                return self.update_object(data)
            else:
                error.raise_error(r)

    async def create(self):
        params = self.update_params()
        if 'id' in params: params.pop('id', None)
        async with session.post(api_base + 'tournaments/' + str(self.id) + '.json?api_key=' + challonge.api_key, json=params) as r:
            if r.status == 200:
                data = r.json()
                return self.update_object(data)
            else:
                error.raise_error(r)

    async def update(self, session):
        params = self.update_params()
        
        async with session.put(self.base_url() + '.json?api_key=' + challonge.api_key, json=params) as r:
            if r.status == 200:
                data = r.json()
                return self.update_object(data)
            else:
                error.raise_error(r)

    async def delete(self, session):
        async with session.delete(self.base_url() + '.json', params={'api_key': challonge.api_key}) as r:
            if r.status == 200:
                return True
            else:
                error.raise_error(r)
    
    async def svg(self, session):
        async with session.get('https://challonge.com/' + str(self.url) + '.svg', params={'api_key': challonge.api_key}) as r:
            if r.status == 200:
                return r.text()
            else:
                error.raise_error(r)

    async def get_participants(self, session, include_matches=False, reload_array=False):
        url = self.base_url() + '/participants.json'
        if include_matches: url += '?include_matches=1'

        async with session.get(url, params={'api_key': challonge.api_key}) as r:
            if r.status == 200:
                data = await r.json()
                plist = self.build_participants(data)
                if reload_array:
                    setattr(self, 'participants', plist)
                return plist
            else:
                error.raise_error(r)

    async def get_participant(self, session, pid, include_matches=False):
        async with session.get(self.base_url() + '/participants/' + str(pid) + '.json', params={'api_key': challonge.api_key}) as r:
            if r.status == 200:
                data = r.json()
                return Participant(data=data)
            else:
                error.raise_error(r)

    async def add_participant(self, session, data={}):
        data.update({'api_key': challonge.api_key})

        async with session.post(self.base_url() + '/participants.json', json=data) as r:
            if r.status == 200:
                data = r.json()
                return Participant(data=data)
            else:
                error.raise_error(r)

    async def bulk_add_participants(self, session, data=None):
        pass

    async def clear_participants(self):
        async with session.delete(self.base_url() + '/participants/clear.json', params={'api_key': challonge.api_key}) as r:
            if r.status == 200:
                return True
            else:
                error.raise_error(r)

    async def randomize_participants(self):
        async with session.post(self.base_url() + '/participants/randomize.json', params={'api_key': challonge.api_key}) as r:
            if r.status == 200:
                return True
            else:
                error.raise_error(r)

    async def matches(self, session, include_attachments=False, reload_array=False):
        url = self.base_url() + '/matches.json'
        if include_attachments: url += '?include_attachments=1'

        async with session.get(url, params={'api_key': challonge.api_key}) as r:
            if r.status == 200:
                data = await r.json()
                plist = self.build_matches(data)
                if reload_array:
                    setattr(self, 'matches', plist)
                return plist
            else:
                error.raise_error(r)

    async def match(self, session, mid, include_attachments=False):
        url = self.base_url() + '/matches/' + str(mid) + '.json'
        if include_attachments: url += '?include_attachments=1'

        async with session.get(url, params={'api_key': challonge.api_key}) as r:
            if r.status == 200:
                data = r.json()
                return Match(data=data)
            else:
                error.raise_error(r)

    def build_participants(self, data={}):
        result = []
        for p in data: result.append(Participant(data=p))
        return result

    def build_matches(self, data={}):
        result = []
        for p in data: result.append(Match(data=p))
        return result
