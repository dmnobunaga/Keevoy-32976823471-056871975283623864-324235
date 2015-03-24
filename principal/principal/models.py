# coding=utf-8
__author__ = 'Dmitry'
from django.db import models
from decimal import Decimal
from django.utils import timezone
from django.contrib.auth.models import User


class ClientProfile(models.Model):
    user = models.ForeignKey(User)
    balance = models.DecimalField(max_digits=15, decimal_places=4, default=Decimal('0.00'))


class Billing(models.Model):
    client_profile = models.ForeignKey(ClientProfile)
    created = models.DateTimeField(default=timezone.now())
    value = models.DecimalField(max_digits=15, decimal_places=4, default=Decimal('0.00'))
    refill_method = models.CharField(max_length=255, default='Yandex Money')


class Keywords(models.Model):
    keyword = models.CharField(max_length=1024)
    price = models.DecimalField(max_digits=15, decimal_places=4, default=Decimal('0.00'))
    category = models.CharField(max_length=255, default="Unknown")
    region = models.CharField(max_length=255, default='Moscow')
    language = models.CharField(max_length=255, default='RU')


class Campaign(models.Model):
    client_profile = models.ForeignKey(ClientProfile)
    created = models.DateTimeField(default=timezone.now())
    campaign_id = models.CharField(max_length=1024)
    campaign_host = models.CharField(max_length=1024)
    volume = models.IntegerField(default=0)
    budget = models.DecimalField(max_digits=15, decimal_places=4, default=Decimal('0.00'))


class CampaignKeywords(models.Model):
    campaign = models.ForeignKey(Campaign)
    keyword = models.ForeignKey(Keywords)

