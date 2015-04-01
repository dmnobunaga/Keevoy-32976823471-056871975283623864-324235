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
from django.shortcuts import render, redirect
from PIL import BmpImagePlugin, PngImagePlugin, Image
from decimal import Decimal
from django.http import JsonResponse
from models import Campaign, CampaignKeywords, ClientProfile, Keywords, Billing



def load_icon(file, index=None):
    """
    Load Windows ICO image.

    See http://en.wikipedia.org/w/index.php?oldid=264332061 for file format
    description.
    """
    if isinstance(file, basestring):
        file = open(file, 'rb')

    header = struct.unpack('<3H', file.read(6))

    # Check magic
    if header[:2] != (0, 1):
        raise SyntaxError('Not an ICO file')

    # Collect icon directories
    directories = []
    for i in xrange(header[2]):
        directory = list(struct.unpack('<4B2H2I', file.read(16)))
        for j in xrange(3):
            if not directory[j]:
                directory[j] = 256

        directories.append(directory)

    if index is None:
        # Select best icon
        directory = max(directories, key=operator.itemgetter(slice(0, 3)))
    else:
        directory = directories[index]

    # Seek to the bitmap data
    file.seek(directory[7])

    prefix = file.read(16)
    file.seek(-16, 1)

    if PngImagePlugin._accept(prefix):
        # Windows Vista icon with PNG inside
        image = PngImagePlugin.PngImageFile(file)
    else:
        # Load XOR bitmap
        image = BmpImagePlugin.DibImageFile(file)
        if image.mode == 'RGBA':
            # Windows XP 32-bit color depth icon without AND bitmap
            pass
        else:
            # Patch up the bitmap height
            image.size = image.size[0], image.size[1] >> 1
            d, e, o, a = image.tile[0]
            image.tile[0] = d, (0, 0) + image.size, o, a

            # Calculate AND bitmap dimensions. See
            # http://en.wikipedia.org/w/index.php?oldid=264236948#Pixel_storage
            # for description
            offset = o + a[1] * image.size[1]
            stride = ((image.size[0] + 31) >> 5) << 2
            size = stride * image.size[1]

            # Load AND bitmap
            file.seek(offset)
            string = file.read(size)
            mask = Image.fromstring('1', image.size, string, 'raw',
                                    ('1;I', stride, -1))

            image = image.convert('RGBA')
            image.putalpha(mask)

    return image


def get_random_price():
    return Decimal(round(random.uniform(0.3, 5), 2))


def main(request):
    return render(request, "front-end/index.html")


@login_required(login_url='/login')
def cabinet(request):
    return render(request, "cabinet/index.html")


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
                return redirect("cabinet")
            else:
                return HttpResponse(u"Error")
        else:
            return HttpResponse(u"User not exist")
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
        if campaign_id and url and keywords and regions and budget:
            client_profile = ClientProfile.objects.filter(user=request.user).first()
            record_campaign, created = Campaign.objects.get_or_create(
                client_profile=client_profile,
                campaign_id=campaign_id,
                campaign_host=url,
                budget=budget
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
                record_campaign.volume = round(Decimal(budget) / (medium_price / len(keywords)))
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


