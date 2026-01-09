from django.db import models
from django.contrib.auth.models import AbstractUser
from django.conf import settings


class CustomUser(AbstractUser):
    """拡張ユーザーモデル"""
    nickname = models.CharField(max_length=50, blank=True)
    class Meta:
        verbose_name_plural = "CustomUser"


#class Profile(models.Model):
#    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
#    # settings.pyに AUTH_USER_MODEL = "accounts.CustomUser"に書いてある
#    # CustomUserと書かないでsettings.AUTH_USER_MODELと書く
#    nickname = models.CharField(max_length=50, blank=True)

#    def __str__(self):
#        return f"{self.user.username}のプロフィール"