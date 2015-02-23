__author__ = 'Dmitry Panchev'
from django.shortcuts import render


def main(request):
    return render(request, "front-end/index.html")