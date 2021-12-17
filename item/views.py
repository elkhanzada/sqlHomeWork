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

#get_item_str = """
#SELECT * FROM {0}
#WHERE {1}_id = {2}
#FETCH FIRST 10 ROWS ONLY
#"""

get_item_str = """
SELECT * FROM {0}
WHERE {1}_id = {2}
ORDER BY -rating
"""

get_cat_str = """
SELECT * FROM {0}
WHERE {1}_id = {2}
"""

def sql_get_item(table_name, id):
    return get_item_str.format(table_name, table_name, id)

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
    print(query)
    cur.execute(query, args)
    r = [dict((cur.description[i][0], value) \
               for i, value in enumerate(row)) for row in cur.fetchall()]
    return (r[0] if r else None) if one else r


def get_genre(cur, res, category):
    print("GET GENRE")
    if category == "movie":
        return query_db(cur, get_cat_str.format("category_mov_book", "cat", res["CAT_ID"]), one=True)["NAME"]
    if category == "book":
        return query_db(cur, get_cat_str.format("category_mov_book", "cat", res["CAT_ID"]), one=True)["NAME"]
    if category == "game":
        return query_db(cur, get_cat_str.format("category_game", "cat", res["CAT_ID"]), one=True)["NAME"]

def get_author(cur, res, category):
    if category == "movie":
        return ""
    if category == "book":
        return query_db(cur, get_cat_str.format("author", "author", res["AUTHOR_ID"]), one=True)["NAME"]
    if category == "game":
        return query_db(cur, get_cat_str.format("developer", "dev", res["DEV_ID"]), one=True)["NAME"]

def get_in_same_genre(cur, res, category):
    print("GET GENRE")
    if category == "movie":
        return query_db(cur, get_item_str.format("movie", "cat", res["CAT_ID"]))
    if category == "book":
        return query_db(cur, get_item_str.format("book", "cat", res["CAT_ID"]))
    if category == "game":
        return query_db(cur, get_item_str.format("game", "cat", res["CAT_ID"]))


def get_in_same_author(cur, res, category):
    if category == "movie":
        return []
    if category == "book":
        return query_db(cur, get_item_str.format("book", "author", res["AUTHOR_ID"]))
    if category == "game":
        return query_db(cur, get_item_str.format("game", "dev", res["DEV_ID"]))

get_item_str2 = """
SELECT AVG(rating) FROM review
WHERE {0}_id = {1}
"""

get_default_rating = """
SELECT rating FROM {0}
WHERE {0}_id = {1}
"""

def get_rating(cur, res, category):
    print(get_item_str2.format(category, res[category.upper() + "_ID"]))
    a = query_db(cur, get_item_str2.format(category, res[category.upper() + "_ID"]), one=True)['AVG(RATING)']
    b = query_db(cur, get_default_rating.format(category, res[category.upper() + "_ID"]), one=True)['RATING']
    if a is None:
        a = b
    return a

# Create your views here.
def index(request, category='', id=0):
    cursor = connectToSqlServer()
    cmd = sql_get_item(category, id)
    my_query = query_db(cursor, cmd)
    json_output = json.dumps(my_query + get_in_same_genre(cursor, my_query[0], category) + get_in_same_author(cursor, my_query[0], category))
    randomThing = {'int2k': json_output, 'category': category, 'genre': get_genre(cursor, my_query[0], category),  'author': get_author(cursor, my_query[0], category), 'rating': get_rating(cursor, my_query[0], category)}
    cursor.connection.close()
    return render(request, 'templates/index3.html', randomThing)