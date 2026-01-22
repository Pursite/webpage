from django.db import models
from django.contrib.auth.models import User
from django.utils.translation import gettext_lazy as _
from apps.lib.basemodel import BaseModel


class UserProfile(BaseModel):

    username = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        max_length=150,
        related_name='profile',
        verbose_name=_('Username')
    )

    phone_number = models.CharField(
        max_length=11,
        unique=True,
        verbose_name=_('Phone Number')
    )
    full_name = models.CharField(max_length=255, verbose_name=_('First Name'), blank=True, null=True)


    national_code = models.CharField(
        max_length=10,
        unique=True,
        null=True,
        blank=True,
        verbose_name=_('National Code')
    )
    email = models.EmailField(unique=True, null=True, blank=True, verbose_name=_('Email'))
    address = models.TextField(blank=True, null=True, verbose_name=_('Address'))

    is_verified = models.BooleanField(default=False, verbose_name=_('Is Verified'))

    class Meta:
        verbose_name = _("User Profile")
        verbose_name_plural = _("User Profiles")

    def __str__(self):
        return f"{self.phone_number} - {self.username.username}"

