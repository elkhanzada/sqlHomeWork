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

sql_search_str = """
select * from {}
where name like '%{}%'
order by -rating
"""

# Create your views here.
def index(request, query='', category=''):
    cursor = connectToSqlServer()
    info_about_items = [category + "_id", "name"]
    if category == "movie":
        info_about_items.append("picture")
    query = query.upper()
    cmd = sql_search_str.format(category, query)
    my_query = query_db(cursor, cmd)
    json_output = json.dumps(my_query)
    randomThing = {'int2k': json_output, 'category': category}
    print(category, query)
    return render(request, 'templates/index2.html', randomThing)