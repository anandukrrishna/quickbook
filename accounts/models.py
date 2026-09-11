from django.db import models
from django.contrib.auth.models import AbstractUser
import uuid

class User(AbstractUser):
    ROLE_CHOICES = [
    ('CUSTOMER', 'Customer'),
    ('VENDOR', 'Vendor'),
    ]

    role = models.CharField(
        max_length=10,
        choices=ROLE_CHOICES,
        default='CUSTOMER'
    )

    referral_code = models.CharField(
        max_length=20,
        unique=True,
        blank=True,
        null=True
    )
    referred_by = models.ForeignKey(
        'self',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='referrals'
    )
    referral_position = models.CharField(
        max_length=5,
        choices=[
            ('LEFT', 'Left'),
            ('RIGHT', 'Right'),
        ],
        null=True,
        blank=True
    )

    def save(self, *args, **kwargs):
        if not self.referral_code:
            self.referral_code = str(uuid.uuid4()).replace('-', '')[:10].upper()

        super().save(*args, **kwargs)

    def __str__(self):
        return self.username
