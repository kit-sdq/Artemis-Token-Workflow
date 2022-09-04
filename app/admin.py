from django.contrib import admin

from app.models import AppPasswordRequest, AuthenticatedAppPasswordRequest

# Register your models here.

admin.register(AppPasswordRequest, AuthenticatedAppPasswordRequest)
