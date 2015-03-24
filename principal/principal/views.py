# coding=utf-8
__author__ = 'Dmitry Panchev'
from django.views.decorators.csrf import csrf_exempt
from models import ClientProfile
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login
from django.shortcuts import render
from PIL import BmpImagePlugin, PngImagePlugin, Image
import operator
import struct
from django.http import JsonResponse


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


def main(request):
    return render(request, "front-end/index.html")


def cabinet(request):
    return render(request, "cabinet/index.html")


def registration(request):
    url = request.GET['site']
    return render(request, "front-end/registration.html", locals())


@csrf_exempt
def create_user(request):
    if request.method == "POST":
        username = request.POST.get('username', None)
        userpass = request.POST.get('userpass', None)
        usermail = request.POST.get('usermail', None)
        if username and userpass and usermail:
            if User.objects.filter(email=usermail).first():
                return JsonResponse({u'error': u'Email уже зарегистрирован!'})
            if User.objects.filter(username=username).first():
                return JsonResponse({u'error': u'Пользователь существует!'})
            user = User.objects.create_user(
                email=usermail,
                username=username,
                password=userpass)
            client_profile = ClientProfile.objects.get_or_create(user=user)
            if user:
                user_auth = authenticate(username=username, password=userpass)
                if user_auth:
                    login(request, user_auth)
                    return JsonResponse({
                        u"success": u"Пользователь создан!",
                        u"user": user.username
                    })
            else:
                return JsonResponse({u'error': u'Ошибка создания пользователя. user'})
        else:
            return JsonResponse({u'error': u'Ошибка создания пользователя.username and userpass and usermail'})
    else:
        return JsonResponse({u'error': u'Неверный метод'})


