from django.shortcuts import redirect
from django.http import HttpRequest, HttpResponseNotAllowed, JsonResponse
from django.conf import settings
from django.urls.exceptions import Http404


def index(request: HttpRequest):
    return redirect(settings.ARTEMIS_SERVER_URL)


def flow_init(request: HttpRequest):
    """
    Called by an application to request an app password.
    """
    if request.method != "POST":
        return HttpResponseNotAllowed(["POST"])

    data = {
        "poll" : {
            "token": "",
            "endpoint": ""
        },
        "login": ""
    }
    return JsonResponse(data)


def flow_poll(request: HttpRequest):
    if request.method != "POST":
        return HttpResponseNotAllowed(["POST"])

    flow_complete = False
    if not flow_complete:
        raise Http404()

    data = {
        "server": "",
        "loginName": "",
        "appPassword": ""
    }
    return JsonResponse(data)



def flow_login(request: HttpRequest, token: str):
    ...
