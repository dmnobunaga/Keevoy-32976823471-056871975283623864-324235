__author__ = 'Dmitry Panchev'
from django.shortcuts import render


def main(request):
    return render(request, "front-end/index.html")


def cabinet(request):
    return render(request, "cabinet/index.html")


def registration(request):
    url = request.GET['site']
    return render(request, "front-end/registration.html", locals())

