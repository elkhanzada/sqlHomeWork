from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
import cx_Oracle
from elkhan.settings import DATABASES
import os
import sys
import json
import hashlib

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
    return cursor, connection

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
    print(query)
    cur.execute(query, args)
    r = [dict((cur.description[i][0], value) \
               for i, value in enumerate(row)) for row in cur.fetchall()]
    return (r[0] if r else None) if one else r

get_max_user_id_str = """
SELECT MAX(USER_ID) from USERS
"""

sql_get_userID = """
SELECT user_id FROM users 
WHERE name = '{0}'
"""

def getUserIDFromName(cur, userName=''):
    return query_db(cur, sql_get_userID.format(userName), one = True)

create_user_str = """
insert into users (user_id, name, password, email) values({0}, '{1}', '{2}', '{3}')
"""

create_review_str = """
insert into review (user_id, game_id, book_id, movie_id, review_id, comment_txt, rating) values({0}, {1}, {2}, {3}, {4}, '{5}', {6})
"""

def get_max_user_id(cur):
    res = query_db(cur, get_max_user_id_str, one=True)
    res = res['MAX(USER_ID)']
    if res is None:
        res = 0
    return res

def find_user_id_by_name(cur, connection, name, password):
    res = getUserIDFromName(cur, name)
    if res is None:
        # Create user
        user_id = get_max_user_id(cur) + 1
        email = 'hello@professor.unist.ac.kr'
        cur.execute(create_user_str.format(user_id, name, hashlib.sha256(bytes(password, encoding='utf-8')).hexdigest(), email), ())
        connection.commit()
        res = None
        while(res == None):
            res = getUserIDFromName(cur, name)
    return res['USER_ID']

# Create your views here.
@csrf_exempt
def index(request):
    cursor, connection = connectToSqlServer()

    if (request.method == "POST"):
        print("post request to create user", request.headers["username"], request.headers["password"])
        find_user_id_by_name(cursor, connection, request.headers['username'], request.headers['password'])
        return
    return render(request, 'templates/registration.html')