from django.conf.urls import url
from . import views
from django.urls import include
from django.urls import path
from employee.models import Employee
# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = [
     path('', views.index, name='index'),
]