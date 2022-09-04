from django.urls import path

from . import views

urlpatterns = [
    path('<str:token>/', views.flow_login, name="flow_login"),
    path('flow/init/', views.flow_init, name="flow_init"),
    path('flow/poll/', views.flow_poll, name="flow_poll")
]
