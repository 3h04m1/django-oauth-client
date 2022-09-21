from django.shortcuts import render, redirect
from django.http import HttpRequest, HttpResponse, JsonResponse, HttpResponseRedirect
from django.contrib.auth import login, get_user_model, logout
from django.forms.models import model_to_dict

from .utils import has_social_account, faceit_time_to_datetime, calculate_token_expiration
from .providers import FaceitProvider, DiscordProvider, OAuth2Provider
from .models import OAuth2Account


def login(request: HttpRequest,provider:OAuth2Provider) -> HttpResponseRedirect:
    return redirect(provider.authorize_url)

def logout_user(request: HttpRequest) -> HttpResponseRedirect:
    logout(request)
    return redirect(to='/')

def authorize(request :HttpRequest,provider:OAuth2Provider) -> JsonResponse:
    provider.authorize(request)
    return redirect(to='/')
   

def discord_authorize(request :HttpRequest) -> JsonResponse:
    print('code', request.GET.get('code'))
    res = discord.get_credentials(request.GET.get('code'))
    print(res)
    # return JsonResponse(res)
    if has_social_account(OAuth2Account, res['user_data']['id']):
        user = OAuth2Account.objects.get(provider_id=res['user_data']['id']).user
        login(request, user)
        return JsonResponse({'status': 'ok'})
    else:
        discord_account = OAuth2Account.objects.get_or_create(
            provider='discord',
            provider_id=res['user_data']['id'],
            access_token=res['access_token'],
            refresh_token=res['refresh_token'],
            expires_at=calculate_token_expiration(res['expires_in']),
            account_data = res['user_data']
        )
        print(discord_account)
        user = get_user_model().objects.create_user(
            username=res['user_data']['username'],
            email=res['user_data']['email'],
            password=res['user_data']['id'],
        )
        discord_account[0].user = user
        discord_account[0].save()
        
        # login(request, user)

        return JsonResponse({'user': model_to_dict(user), 'discord_account': model_to_dict(discord_account[0])})