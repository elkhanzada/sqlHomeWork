from django.conf.urls import url
from . import views
from django.urls import include, path
from django.contrib import admin
admin.autodiscover()
from rest_framework import routers

router = routers.DefaultRouter()

urlpatterns = [
     path('<str:category>/<str:genre>/<str:rating>/<str:publisher>/<str:query>', views.index),
     path('<str:category>/<str:genre>/<str:rating>/<str:query>', views.index_movie),
]