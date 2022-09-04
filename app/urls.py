from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='flow_index'),
    path('init', views.flow_init, name="flow_init"),
    path('poll', views.flow_poll, name="flow_poll"),
    path('login/<str:token>', views.flow_login, name="flow_login")
]
