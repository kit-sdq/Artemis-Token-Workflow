from django.shortcuts import redirect, reverse
from django.http import HttpRequest, HttpResponseNotAllowed, JsonResponse
from django.conf import settings
from django.urls.exceptions import Http404

from secrets import token_urlsafe

from django.views.decorators.csrf import csrf_exempt

from app.models import APP_PASSWORD_FLOW_TOKEN_LENGTH, AppPasswordRequest


def _get_random_token(length: int):
    token = token_urlsafe(length)  # only expected: len(token) == length * 1.3
    while len(token) < length:
        token += token_urlsafe()
    return token[:length]


def index(request: HttpRequest):
    return redirect(settings.ARTEMIS_SERVER_URL)


@csrf_exempt
def flow_init(request: HttpRequest):
    """
    Called by an application to request an app password.
    """
    if request.method != "POST":
        return HttpResponseNotAllowed(["POST"])

    app_password_request = AppPasswordRequest(
        login_token=_get_random_token(APP_PASSWORD_FLOW_TOKEN_LENGTH),
        poll_token=_get_random_token(APP_PASSWORD_FLOW_TOKEN_LENGTH),
    )
    app_password_request.save()

    data = {
        "poll": {
            "token": app_password_request.poll_token,
            "endpoint": request.build_absolute_uri(reverse("flow_poll")),
        },
        "login": request.build_absolute_uri(reverse("flow_login", args=[app_password_request.login_token])),
    }
    return JsonResponse(data)


def flow_poll(request: HttpRequest):
    """
    Called by an application to check if the authentication was performed.
    """
    if request.method != "POST":
        return HttpResponseNotAllowed(["POST"])

    flow_complete = False
    if not flow_complete:
        raise Http404()

    data = {"server": "", "loginName": "", "appPassword": ""}
    return JsonResponse(data)


def flow_login(request: HttpRequest, token: str):
    """
    Called by an user to perform authentication to an AppPasswordRequest.
    """
    ...
