__author__ = 'Dmitry Panchev'
from django.shortcuts import render


def main(request):
    return render(request, "front-end/index.html")

def cabinet(request):
    return render(request, "front-end/cabinet/index.html")

def registration(request):
    return render(request, "front-end/registration.html")