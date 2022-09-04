from django.db import models

# Create your models here.


class AuthenticationRequest(models.Model):
    poll_token = models.CharField(max_length=128)
    login_token = models.CharField(max_length=128)
    date_created = models.DateField(auto_now_add=True)


class ArtemisLogin(models.Model):
    request = models.ForeignKey(AuthenticationRequest, on_delete=models.CASCADE)
    # https://github.com/ls1intum/Artemis/blob/9f5fffe974adbc4ca250ef36fa6ab6a88425a792/src/main/java/de/tum/in/www1/artemis/config/Constants.java#L10
    artemis_user = models.CharField(max_length=50)
    artemis_password = models.CharField(max_length=50)
    date_created = models.DateField(auto_now_add=True)
