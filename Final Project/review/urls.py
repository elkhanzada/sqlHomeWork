from django.conf.urls import url
from . import views
from django.urls import include, path
from django.contrib import admin
admin.autodiscover()
from rest_framework import routers

router = routers.DefaultRouter()

urlpatterns = [
     path('<str:userName>', views.index),

]