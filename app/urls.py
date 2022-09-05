from django.urls import path, include

from . import views

urlpatterns = [
    path('flow/auth/<str:token>/', views.flow_login, name="flow_login"),
    path('flow/init/', views.flow_init, name="flow_init"),
    path('flow/poll/', views.flow_poll, name="flow_poll"),
    path("saml2/", include('djangosaml2.urls'), name="saml2_prefix"),
]
