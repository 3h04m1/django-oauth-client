from .oauth2 import OAuth2Provider, requests
from django.conf import settings

class DiscordProvider(OAuth2Provider):
    def __init__(self):
        try:
            super().__init__(
                name='discord',
                client_id=settings.OAUTH_PROVIDERS['discord']['client_id'],
                client_secret=settings.OAUTH_PROVIDERS['discord']['client_secret'],
                authorize_url=settings.OAUTH_PROVIDERS['discord']['authorize_url'],
                access_token_url='https://discord.com/api/oauth2/token',
                user_info_url='https://discord.com/api/users/@me',
            )
        except KeyError or AttributeError:
            raise DJANGO_SETTINGS_NOT_CONFIGURED('Discord OAuth2 provider is not configured')

    def get_credentials(self, code):
        data = {
            'client_id': str(self.client_id),
            'client_secret': str(self.client_secret),
            'grant_type': 'authorization_code',
            'code': str(code),
            'redirect_uri': 'http://localhost:8000/oauth/discord/authorize/',
            'scope': 'identify email connections'
        }
        headers = {
            'Content-Type': 'application/x-www-form-urlencoded',
        }
        res = requests.post(self.access_token_url, data=data, headers=headers)
        print(res.text)
        print(res.status_code)
        if res.status_code != 200:
            raise Exception('STATUS CODE '+str(res.status_code) + ' ' +res.json()['error']+': '+res.json()['error_description'])
        credentials = requests.get(self.user_info_url, headers={
            'Authorization': f'Bearer {res.json()["access_token"]}'
        }).json()

        ret = {
            'access_token': res.json()['access_token'],
            'refresh_token': res.json()['refresh_token'],
            'expires_in': res.json()['expires_in'],
            'user_data': credentials
        }

        return ret