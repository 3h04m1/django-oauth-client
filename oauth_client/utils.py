from django.db import models
from .models import OAuth2Account
import datetime


def has_social_account(provider:models.Model, provider_id:str) -> bool:
    return OAuth2Account.objects.filter(provider_id=provider_id).exists() and OAuth2Account.objects.get(provider_id=provider_id).user is not None

def faceit_time_to_datetime(date:str) -> datetime.datetime:
    date = date.split('/')
    print(date)
    return datetime.date(int(date[2]), int(date[1]), int(date[0]))

def calculate_token_expiration(expires_in:int) -> datetime.datetime:
    return datetime.datetime.now() + datetime.timedelta(seconds=expires_in)
