from django.urls import include, path
from . import views
from .providers import OAuth2Provider
# from .utils import get_provider_by_name

urlpatterns = [
    path('logout/', views.logout_user, name='logout'),
]
# print(OAuth2Provider.get_providers().keys())

for provider in OAuth2Provider.get_registred_providers():
    urlpatterns.append(path(f'{provider.name}/login/', views.login, {'provider': provider}, name=f"{provider.name}_login"))
    urlpatterns.append(path(f'{provider.name}/authorize/', views.authorize, {'provider': provider}, name=f'{provider.name}_authorize'))

