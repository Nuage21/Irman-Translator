from django.urls import path
from . import views
from django.conf.urls import url


urlpatterns = [
    url(r'^ajax/translate/$', views.Translate, name='Translate'),
    path('', views.index, name='index')
]