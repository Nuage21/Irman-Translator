from django.urls import path
from . import views
from .classes import ajax_translate
from django.conf.urls import url


urlpatterns = [
    url(r'^ajax/translate/$', ajax_translate.translate, name='translate'),
    path('', views.index, name='index')
]
