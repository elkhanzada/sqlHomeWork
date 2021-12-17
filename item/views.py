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
    #print(query)
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

get_review_for_item = """
SELECT * FROM review
WHERE {0}_id = {1}
"""

get_max_review_id_str = """
SELECT MAX(REVIEW_ID) from REVIEW
"""

get_max_user_id_str = """
SELECT MAX(USER_ID) from USERS
"""

sql_get_userID = """
SELECT user_id FROM users 
WHERE name = '{0}'
"""

def getUserIDFromName(cur, userName=''):
    return query_db(cur, sql_get_userID.format(userName), one = True)

def get_review(cur, ID, category):
    return query_db(cur, get_review_for_item.format(category, ID))

def get_rating(cur, res, category):
    #print(get_item_str2.format(category, res[category.upper() + "_ID"]))
    a = query_db(cur, get_item_str2.format(category, res[category.upper() + "_ID"]), one=True)['AVG(RATING)']
    b = query_db(cur, get_default_rating.format(category, res[category.upper() + "_ID"]), one=True)['RATING']
    if a is None:
        a = b
    return a

create_user_str = """
insert into users (user_id, name, password, email) values({0}, '{1}', '{2}', '{3}')
"""

create_review_str = """
insert into review (user_id, game_id, book_id, movie_id, review_id, comment_txt, rating) values({0}, {1}, {2}, {3}, {4}, '{5}', {6})
"""

def get_max_review_id(cur):
    res = query_db(cur, get_max_review_id_str, one=True)
    #wtf = query_db(cur, 'select count(*) from review')
    #print("wtf: ", wtf)
    res = res['MAX(REVIEW_ID)']
    if res is None:
        res = 0
    return res

def get_max_user_id(cur):
    res = query_db(cur, get_max_user_id_str, one=True)
    res = res['MAX(USER_ID)']
    if res is None:
        res = 0
    return res

def find_user_id_by_name(cur, connection, name):
    res = getUserIDFromName(cur, name)
    if res is None:
        # Create user
        user_id = get_max_user_id(cur) + 1
        password = 'some nonsense'
        email = 'hello@professor.unist.ac.kr'
        cur.execute(create_user_str.format(user_id, name, password, email), ())
        connection.commit()
        res = None
        while(res == None):
            res = getUserIDFromName(cur, name)
    return res['USER_ID']

# Create your views here.
@csrf_exempt
def index(request, category='', id=0):
    cursor, connection = connectToSqlServer()
    if(request.method=="POST"):
        print("Add review post request: ", request.headers['reviewText'], " ", request.headers['reviewRating'], 
        " ", request.headers['reviewUserName'])
        review_id = get_max_review_id(cursor) + 1
        user_id = find_user_id_by_name(cursor, connection, request.headers['reviewUserName'])
        game_id = book_id = movie_id = "\'\'"
        if category == 'game':
            game_id = id
        if category == 'book':
            book_id = id
        if category == 'movie':
            movie_id = id
        comment_txt = request.headers['reviewText']
        rating = int(request.headers['reviewRating'])
        #  (user_id, game_id, book_id, movie_id, review_id, comment_txt, rating)
        print("CREATE REVIEW:", create_review_str.format(user_id, game_id, book_id, movie_id, review_id, comment_txt, rating))
        cursor.execute( create_review_str.format(user_id, game_id, book_id, movie_id, review_id, comment_txt, rating), ())
        connection.commit()
    
        return
    cmd = sql_get_item(category, id)
    my_query = query_db(cursor, cmd)
    my_reviews = get_review(cursor, id, category)
    json_output = json.dumps(my_query + get_in_same_genre(cursor, my_query[0], category) + get_in_same_author(cursor, my_query[0], category))
    my_reviews_json = json.dumps(my_reviews)

    randomThing = {
        'int2k': json_output, 
        'reviews': my_reviews_json,
        'category': category, 
        'genre': get_genre(cursor, my_query[0], category),  
        'author': get_author(cursor, my_query[0], category), 
        'rating': get_rating(cursor, my_query[0], category),
    }
    cursor.connection.close()
    return render(request, 'templates/index3.html', randomThing)