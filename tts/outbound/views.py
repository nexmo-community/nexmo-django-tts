import os
from hashlib import md5
from time import time
import random
import requests
from django.utils.html import strip_tags
from django.views.generic import TemplateView


class MarvelView(TemplateView):
    template_name = 'outbound/marvel.json'
    content_type = 'application/json'

    @staticmethod
    def get_marvel_data():
        marvel_api_url = 'https://gateway.marvel.com:443/v1/public/characters'
        private_key = os.environ['MARVEL_PRIVATE_KEY']
        api_key = os.environ['MARVEL_API_KEY']

        timestamp = str(time())
        hashed_key = md5(
            str(timestamp + private_key + api_key).encode('utf-8')
        )

        response = requests.get(
            marvel_api_url,
            params={
                'series': '22547',  # Avengers (2016 - Present)
                'apikey': api_key,
                'ts': timestamp,
                'hash': hashed_key.hexdigest()
            },
            headers={
                'Accept': 'application/json'
            }
        )
        marvel_response_data = response.json()
        return [{
            'name': x['name'],
            'description': x['description']
        } for x in marvel_response_data['data']['results'] if x['description']]
    
    @staticmethod
    def random_voice_name():
        # https://developer.nexmo.com/api/voice/ncco#voice-names
        return random.choice([
            'Salli', 'Joey', 'Nicole', 'Russell', 'Amy', 'Brian', 'Emma',
            'Gwyneth', 'Geraint', 'Raveena', 'Chipmunk', 'Eric', 'Ivy', 
            'Jennifer', 'Justin', 'Kendra', 'Kimberly',
        ])

    def get_context_data(self, **kwargs):
        marvel_data = self.get_marvel_data()
        random_character = random.choice(marvel_data)

        kwargs['voice_name'] = self.random_voice_name()
        kwargs['marvel_message'] = "{name} - {description}".format(
            name=strip_tags(random_character['name']),
            description=strip_tags(random_character['description'])
        )

        return super(MarvelView, self).get_context_data(**kwargs)
        