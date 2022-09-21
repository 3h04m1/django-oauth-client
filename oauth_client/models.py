from tabnanny import verbose
from django.db import models

class OAuth2Account(models.Model):
    class Meta:
        unique_together = ('provider', 'provider_id')
        verbose_name = 'OAuth2 Account'
        verbose_name_plural = 'OAuth2 Accounts'
    
    user = models.ForeignKey('auth.User', on_delete=models.CASCADE, null=True, blank=True)
    provider = models.CharField(max_length=255)
    provider_id = models.CharField(max_length=255, primary_key=True)
    access_token = models.CharField(max_length=255)
    refresh_token = models.CharField(max_length=255)
    expires_at = models.DateTimeField()
    account_data = models.JSONField(null=True, blank=True)
    

    def __str__(self):
        return f'{self.user} - {self.provider}'
