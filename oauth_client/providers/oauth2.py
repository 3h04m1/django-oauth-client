import base64
import requests
from django.conf import settings
from django.http import HttpRequest, JsonResponse
from .errors import DJANGO_SETTINGS_NOT_CONFIGURED
from django.contrib.auth import get_user_model, login
from colorama import init, Fore
from ..utils import has_social_account, calculate_token_expiration
from ..models import OAuth2Account



init()


class OAuth2Provider:
    def __init__(self, name, client_id=None, client_secret=None, authorize_url=None, access_token_url=None, user_info_url=None):
        self.name = name
        self.client_id = client_id
        self.client_secret = client_secret
        self.authorize_url = authorize_url
        self.access_token_url = access_token_url
        self.user_info_url = user_info_url
        print(f'{self.name} initialized')

    def get_credentials(self, code):
        secret = f'{self.client_id}:{self.client_secret}'
        secret = base64.b64encode(str.encode(secret))
        print('secret', secret)
        res:requests.Response = requests.post(self.access_token_url, data={
            'code': code,
            'grant_type': 'authorization_code'
        }, headers={
            'Content-Type': 'application/x-www-form-urlencoded',
            'Authorization':f'Basic {str(secret, "utf-8")}',
            })
        
        data = res.json()
        print('data', data)
        data['user_data'] = requests.get(self.user_info_url, headers={
            'Authorization': f'Bearer {data["access_token"]}'
        }).json()

        return data

    def authorize(self, request: HttpRequest):
        res = self.get_credentials(code=request.GET.get('code'))
        print('res', res)
        if has_social_account(self, res["user_data"]['id']):
            user = OAuth2Account.objects.get(provider_id=res["user_data"]['id']).user
            if user is not None:
                login(request, user)    
            return JsonResponse({
                'status': 'success',
                'message': 'User logged in',
                'user': user.username
            })
        else:
            social_account = OAuth2Account.objects.get(provider_id=res["user_data"]['id'])
            if social_account is None:
                social_account = OAuth2Account.objects.get_or_create(
                    provider=self.name,
                    provider_id=res['user_data']['id'],
                    access_token=res['access_token'],
                    refresh_token=res['refresh_token'],
                    expires_at=calculate_token_expiration(res['expires_in']),
                    account_data = res['user_data']
                )
                try:
                    email = res['user_data']['email']
                except KeyError:
                    email = None
                user = get_user_model().objects.create_user(
                    username=res['user_data']['username'],
                    email=email,
                    password=res['user_data']['id'],
                )
                social_account.user = user
                if social_account.user != None:
                    social_account.save()
                    login(request, user)
                else:
                    raise Exception('User not found')
            else:
                try:
                    email = social_account.account_data['email']
                except KeyError:
                    email = None
                user = get_user_model().objects.create_user(
                    username=social_account.account_data['username'],
                    email=email,
                    password=social_account.account_data['id'],
                )
            social_account.user = user
            social_account.save()
            login(request, user)
                
            return JsonResponse({
                'status': 'success',
                'message': 'Account created',
                'user': user.username
            })

        
    
    @classmethod
    def get_provider_names(cls):
        # list of providers
        providers = []
        # get all providers that inherit from OAuth2Provider
        for provider in cls.__subclasses__():
            # get provider name
            name = provider.__name__.lower().replace('provider', '')
            provider_class = provider
            # get provider settings
            # create provider instance
            providers.append((name, provider_class))
        return providers

    @classmethod
    def get_providers(cls):
        try:
            return [provider for provider in settings.OAUTH_PROVIDERS]
        except AttributeError as e:
            raise DJANGO_SETTINGS_NOT_CONFIGURED(Fore.RED+ 'OAUTH_PROVIDERS not configured')

    @classmethod
    def get_registred_providers(self):
        providers = []
        for provider in self.get_providers():
            for provider_name, provider_class in self.get_provider_names():
                if provider_name == provider:
                    providers.append(provider_class())
        print('providers', providers)
        return providers