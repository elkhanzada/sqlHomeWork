from django.shortcuts import render

# Create your views here.
def index(request):
    #return HttpResponse("Hello, world. You're at the employee index.")
    return render(request, 'templates/index.html')