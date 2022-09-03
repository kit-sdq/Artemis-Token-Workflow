from django.shortcuts import redirect
from django.http import HttpRequest
from django.conf import settings


def index(request: HttpRequest):
    return redirect(settings.ARTEMIS_URL)


def flow_init(request: HttpRequest):
    """
    Called by an application to request an app password.
    """
    ...


def flow_poll():
    ...


def login():
    ...
