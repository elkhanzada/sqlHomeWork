from django.shortcuts import render
from django.template import loader
from django.http import HttpResponse
# Create your views here.

def index(request):
    #return HttpResponse("Hello, world. You're at the employee index.")
    return render(request, 'templates/employee_list.html')

