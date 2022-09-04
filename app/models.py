from django.db import models

# Create your models here.


APP_PASSWORD_FLOW_TOKEN_LENGTH = 128


class AppPasswordRequest(models.Model):
    poll_token = models.CharField(max_length=APP_PASSWORD_FLOW_TOKEN_LENGTH)
    login_token = models.CharField(max_length=APP_PASSWORD_FLOW_TOKEN_LENGTH)
    date_created = models.DateTimeField(auto_now_add=True)


class AuthenticatedAppPasswordRequest(AppPasswordRequest):
    # https://github.com/ls1intum/Artemis/blob/9f5fffe974adbc4ca250ef36fa6ab6a88425a792/src/main/java/de/tum/in/www1/artemis/config/Constants.java#L10
    artemis_user = models.CharField(max_length=50)
