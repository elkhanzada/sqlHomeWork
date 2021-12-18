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

sql_get_userID = """
SELECT user_id FROM users 
WHERE name = '{0}'
"""

sql_get_reviews_userID = """
SELECT * FROM review
WHERE user_id = {0}
"""
sql_delete_review_from_id = """
DELETE FROM review WHERE review_id = {0}
"""
get_user_str = """
select * from users
where name = '{0}'
"""

def get_user(username):
    cur, connection = connectToSqlServer()
    return query_db(cur, get_user_str.format(username), one=True)
def deleteReviewFromID(id):
    cursor, connection = connectToSqlServer()
    cursor.execute(sql_delete_review_from_id.format(id))
    connection.commit()

def getUserIDFromName(cur, userName=''):
    return query_db(cur, sql_get_userID.format(userName), one = True)["USER_ID"]

def getReviewsFromUserID(cur, userID=0): # dictionary
    return query_db(cur, sql_get_reviews_userID.format(userID))

# Create your views here.
@csrf_exempt
def index(request, userName=''):
    user_db_instance = get_user(userName)
    if (request.method == "POST"):
        if user_db_instance['PASSWORD'] != hashlib.sha256(bytes(request.headers['password'], encoding='utf-8')).hexdigest():
            return
        print("post request to delete review id: ", request.headers["deleteReq"])
        id = int(request.headers["deleteReq"])
        deleteReviewFromID(id)
        return
    cursor, connection = connectToSqlServer()
    myQuery = getReviewsFromUserID(cursor, getUserIDFromName(cursor, userName)) # reviews dict
    json_output = json.dumps(myQuery)
    randomThing = {'int2k': json_output, 'userName':userName}
    cursor.connection.close()
    return render(request, 'templates/reviewPage.html', randomThing)