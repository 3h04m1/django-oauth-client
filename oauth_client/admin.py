from django.contrib import admin
from .models import OAuth2Account

admin.site.register(OAuth2Account)
class OAuth2AccountAdmin(admin.ModelAdmin):
    # name in admin panel
    
    list_display = ('user', 'provider', 'provider_id', 'access_token', 'refresh_token', 'expires_at', 'account_data')
    list_filter = ('user', 'provider', 'provider_id', 'access_token', 'refresh_token', 'expires_at', 'account_data')
    search_fields = ('user', 'provider', 'provider_id', 'access_token', 'refresh_token', 'expires_at', 'account_data')
    ordering = ('user', 'provider', 'provider_id', 'access_token', 'refresh_token', 'expires_at', 'account_data')
    filter_horizontal = ()
    list_per_page = 25


# Register your models here.
