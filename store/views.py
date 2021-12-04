from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
import cx_Oracle
from elkhan.settings import DATABASES
import os
 
_user = DATABASES['default']['USER']
_password = DATABASES['default']['PASSWORD']
_dsn = DATABASES['default']['HOST']+":"+DATABASES['default']['PORT']

def getInfo():
    connection = cx_Oracle.connect(
        user=_user,
        password=_password,
        dsn=_dsn)
    cursor = connection.cursor()
    movie = "SELECT * FROM movie"
    cursor.execute(movie)
    res = cursor.fetchall()
    for row in res:
        print(row)
    return res

# Create your views here.
@csrf_exempt
def index(request):
    res = getInfo()
    #return HttpResponse("Hello, world. You're at the employee index.")
    randomThing = {'int2k': 10}
    if(request.method == "POST"):
        print(request.headers['query']) #json
        # print(request.GET.get)
    return render(request, 'templates/index.html', randomThing)