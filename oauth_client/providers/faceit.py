from .oauth2 import OAuth2Provider, requests

class FaceitProvider(OAuth2Provider):
    def __init__(self):
        try:
            super().__init__(
                name='faceit',
                client_id=settings.OAUTH_PROVIDERS['faceit']['client_id'],
                client_secret=settings.OAUTH_PROVIDERS['faceit']['client_secret'],
                authorize_url='https://accounts.faceit.com/?response_type=code',
                access_token_url='https://api.faceit.com/auth/v1/oauth/token',
                user_info_url='https://api.faceit.com/auth/v1/resources/userinfo',
            )
        except KeyError or AttributeError:
            raise DJANGO_SETTINGS_NOT_CONFIGURED('Faceit OAuth2 provider is not configured')

    def get_credentials(self, code):
        data = super().get_credentials(code)
        data['user_data']['id'] = data['user_data']['guid']
        return data

    def get_authorize_url(self):
        return f'{self.authorize_url}&client_id={self.client_id}&redirect_popup=true'
