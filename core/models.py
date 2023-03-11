from django.db import models

from django.contrib.auth.models import User
from django.db.models.fields import CharField, TextField
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.utils import timezone, tree
# from psycopg2 import Timestamp
from taggit.managers import TaggableManager
from django.db import models

# Choices
SUBSCRIPTION_CHOICES = (
    ('free', 'Free'),
    ('premium', 'Premium')
)

HTTP_CHOICES = (
    ('http', 'http'),
    ('https', 'https')
)

# Models
class UserProfile(models.Model):
    """
    User Profile Model
    """
    class Params:
        """
        User Profile Parameters
        """
        db = 'default'
    id = models.AutoField(
        db_column='id', primary_key=True)
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    contact_mobile = models.CharField(max_length=256, blank=True, null=True)
    marketing_choice = models.BooleanField(default=True)
    notes = models.TextField(blank=True, null=True)
    subscription = models.CharField(max_length=50, choices=SUBSCRIPTION_CHOICES, null=True)
    subscription_active = models.BooleanField(default=False, null=False)
    # 2FA
    # privacy settings

@receiver(post_save, sender=User)
def create_user_profile(instance, created, **kwargs):
    """
    Create the User
    """
    if created:
        UserProfile.objects.create(user=instance)


class Redirects(models.Model):
    """
    Redirects Model
    """
    class Params:
        """
        Redirects Parameters
        """
        db = 'default'
    id = models.AutoField(
        db_column='id', primary_key=True)
    user = models.ForeignKey(User, null=False, on_delete=models.CASCADE, related_name='user_redirects')
    timestamp = models.DateTimeField(default=timezone.now)
    url_from = models.CharField(max_length=512, null=False)
    url_to = models.CharField(max_length=512, null=False)
    http_https = models.CharField(max_length=5, null=False, choices=HTTP_CHOICES)

    def __str__(self):
        return self.url_to