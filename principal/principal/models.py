__author__ = 'Dmitry'
from django.db import models
from decimal import Decimal
from django.utils import timezone
from django.contrib.auth.models import User


class Keywords(models.Model):
    keyword = models.CharField(max_length=1024)
    price = models.DecimalField(max_digits=15, decimal_places=4, default=Decimal('0.00'))
    category = models.CharField(max_length=255, default="Unknown")
    region = models.CharField(max_length=255, default='Moscow')
    language = models.CharField(max_length=255, default='RU')


class Campaign(models.Model):
    user = models.ForeignKey(User)
    created = models.DateTimeField(default=timezone.now())
    campaign_id = models.CharField(max_length=1024)
    campaign_host = models.CharField(max_length=1024)
    volume = models.IntegerField(default=0)
    budget = models.DecimalField(max_digits=15, decimal_places=4, default=Decimal('0.00'))


class CampaignKeywords(models.Model):
    campaign = models.ForeignKey(Campaign)
    keyword = models.ForeignKey(Keywords)

