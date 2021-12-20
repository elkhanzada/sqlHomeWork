from django.conf.urls import url
from . import views
from django.urls import include, path
from django.contrib import admin
admin.autodiscover()
from rest_framework import routers
from store import views

router = routers.DefaultRouter()

urlpatterns = [
     path('', views.index, name='index'),
]