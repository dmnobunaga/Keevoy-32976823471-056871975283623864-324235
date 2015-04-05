# coding=utf-8

__author__ = 'Dmitry Panchev'
import operator
import struct
import random
import json
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login
from django.shortcuts import render, redirect, render_to_response
from PIL import BmpImagePlugin, PngImagePlugin, Image
from decimal import Decimal
from django.http import JsonResponse
from models import Campaign, CampaignKeywords, ClientProfile, Keywords, Billing, Order
from yandex_money.forms import PaymentForm
from yandex_money.models import Payment
from django.contrib import messages


def get_random_price():
    return Decimal(round(random.uniform(0.3, 5), 2))


def main(request):
    return render(request, "front-end/index.html")


def mobile(request):
    return render(request, "front-end/mobile.html")


@login_required(login_url='/login')
def cabinet(request):
    client_profile = ClientProfile.objects.filter(user=request.user).first()
    campaigns = Campaign.objects.filter(client_profile=client_profile).all()
    return render(request, "cabinet/index.html", locals())


@login_required(login_url='/login')
def billing(request):
    client_profile = ClientProfile.objects.filter(user=request.user).first()
    orders = Order.objects.filter(client_profile=client_profile).all()
    return render(request, "cabinet/billing.html", locals())


@login_required(login_url='/login')
def payment_yandex(request):
    campaign_id = request.GET.get('campaign', None)
    if not campaign_id:
        messages.add_message(request, messages.ERROR, u'Выберите рекламную кампанию')
        return redirect(cabinet)

    client_profile = ClientProfile.objects.filter(user=request.user).first()
    campaign = Campaign.objects.filter(client_profile=client_profile, campaign_id=campaign_id).first()
    if campaign:
        return render(request, "cabinet/yandex_payment_form.html", locals())
    else:
        messages.add_message(request, messages.ERROR, u'Рекламная кампания не существует')
        return redirect(cabinet)


@login_required(login_url='/login')
def faq(request):
    return render(request, "cabinet/faq.html")


@login_required(login_url='/login')
def campaign(request):
    return render(request, "cabinet/campaign.html")


def user_login(request):
    if request.method == u"POST":
        username = request.POST.get(u"username", None)
        password = request.POST.get(u"password", None)
        email_username = User.objects.filter(email=username).first()
        if email_username:
            user = authenticate(username=email_username.username, password=password)
        else:
            user = authenticate(username=username, password=password)
        if user is not None:
            if user.is_active:
                login(request, user)
                next = request.GET.get('next', None)
                if next:
                    return redirect(next)
                else:
                    return redirect(cabinet)
            else:
                messages.add_message(request, messages.ERROR, u'Проверьте логин и пароль')
                return redirect(user_login)
        else:
            messages.add_message(request, messages.ERROR, u'Пользователь не существует')
            return redirect(user_login)
    return render(request, u"cabinet/login.html")


def registration(request):
    url = request.GET.get('site', None)
    if not url:
        url = "http://"
    return render(request, "front-end/registration.html", locals())


@csrf_exempt
def campaign_save(request):
    if request.method == "POST":
        campaign_id = request.POST.get("campaign_id", None)
        url = request.POST.get("url", None)
        keywords = request.POST.getlist("keywords[]", None)
        regions = request.POST.getlist("regions[]", None)
        budget = request.POST.get("budget", None)
        specialist = request.POST.get("specialist", False)
        if campaign_id and url and keywords and regions and budget:
            client_profile = ClientProfile.objects.filter(user=request.user).first()
            record_campaign, created = Campaign.objects.get_or_create(
                client_profile=client_profile,
                campaign_id=campaign_id,
                campaign_host=url,
                budget=budget,
                specialist=specialist
            )
            if created:
                record_campaign.region = json.dumps(regions)
                medium_price = Decimal(0.0)
                for keyword in keywords:
                    record_keyword, keyword_created = Keywords.objects.get_or_create(
                        keyword=keyword,
                    )
                    if keyword_created:
                        record_keyword.new = True
                        record_keyword.price = get_random_price()
                        record_keyword.save()
                        medium_price += record_keyword.price
                    else:
                        medium_price += record_keyword.price
                    campaign_keyword, created = CampaignKeywords.objects.get_or_create(
                        keyword=record_keyword,
                        campaign=record_campaign
                    )
                try:
                    volume = round(Decimal(budget) / (medium_price / len(keywords)))
                except:
                    volume = 0
                record_campaign.volume = volume
                record_campaign.save()
                return JsonResponse({u"success": u"РК создана", })
            else:
                return JsonResponse({u"error": u"РК уже существует!", })
        else:
            return JsonResponse({u"error": u"Не все поля заполнены!", })
    else:
        return JsonResponse({u"error": u"Wrong method", })


@csrf_exempt
def create_user(request):
    if request.method == "POST":
        username = request.POST.get("username", None)
        userpass = request.POST.get("userpass", None)
        usermail = request.POST.get("usermail", None)
        if username and userpass and usermail:
            if User.objects.filter(email=usermail).first():
                return JsonResponse({u'error': u'Email уже зарегистрирован!'})
            if User.objects.filter(username=username).first():
                return JsonResponse({u'error': u'Пользователь существует!'})
            user = User.objects.create_user(
                email=usermail,
                username=username,
                password=userpass)
            client_profile, created = ClientProfile.objects.get_or_create(user=user)
            if user:
                user_auth = authenticate(username=username, password=userpass)
                if user_auth:
                    login(request, user_auth)
                    return JsonResponse({
                        u"success": u"Пользователь создан!",
                        u"user": user.username,
                        u"email": user.email,
                        u"balance": client_profile.balance
                    })
                else:
                    return JsonResponse({
                        u"error": u"Can't login with new user",
                    })

            else:
                return JsonResponse({u'error': u'Ошибка создания пользователя. user'})
        else:
            return JsonResponse({u'error': u'Ошибка создания пользователя.username and userpass and usermail'})
    else:
        return JsonResponse({u'error': u'Неверный метод'})


