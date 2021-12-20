from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
import cx_Oracle
from elkhan.settings import DATABASES
import os
import sys
import json
 
_user = DATABASES['default']['USER']
_password = DATABASES['default']['PASSWORD']
_dsn = DATABASES['default']['HOST']+":"+DATABASES['default']['PORT']

def sqlCount(tableName):
    res = "select count(*) from " + tableName
    return res

def sqlGet(tableName, things):
    res = "select "
    for i, item in enumerate(things):
        if(i + 1< len(things)):
            res = res + item + ", "
        else:
            res = res + item + " " 
    res = res + "from " + tableName
    return res

def connectToSqlServer():
    connection = cx_Oracle.connect(
        user=_user,
        password=_password,
        dsn=_dsn)
    cursor = connection.cursor()
    return cursor

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

def query_db(cur, query, args=(), one=False):
    cur.execute(query, args)
    r = [dict((cur.description[i][0], value) \
               for i, value in enumerate(row)) for row in cur.fetchall()]
    cur.connection.close()
    return (r[0] if r else None) if one else r

# Create your views here.
@csrf_exempt
def index(request):
    cursor = connectToSqlServer()
    cmd = sqlGet("movie", ["movie_id", "picture", "name"])
    my_query = query_db(cursor, cmd)
    json_output = json.dumps(my_query)
    randomThing = {'int2k': json_output}
    if(request.method == "POST"):
        print(request.headers['query']) #json
        # print(request.GET.get)
    return render(request, 'templates/index.html', randomThing)