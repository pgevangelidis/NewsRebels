from django.shortcuts import render, redirect
import datetime
from django.contrib.auth import authenticate
# This script contains QUERIES for the database
import sqlite3 as lite
# This script contains QUERIES for the database
from django.db import connection
import sys
import os
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DB_PATH = os.path.join(BASE_DIR, 'db.sqlite3')


# This query returns the user details. 1 row all attributes

def UserDetails(user_id):

    #if request.user.is_authenticated():
        # bring the user's rss id
        try:

            try:
                con = lite.connect(DB_PATH)

                with connection.cursor() as cursor:
                    cursor.execute("SELECT username,first_name,last_name, email, date_joined FROM auth_user WHERE id=%s", [user_id])
                    # This list contains the RSS title and Link of the user RSS.
                    user_details = cursor.fetchone()

                con.commit()
            except Exception as e:
                print("Error: ", e.args[0])
                #sys.exit(1)
            finally:
                if con:
                    con.close()

        except TypeError:
            pass

        return user_details
##########################################3
# This query returns a query set of all RSS for a specific user.
def UserRSS(user_id):
    #if request.user.is_authenticated():
        # bring the user's rss id
        try:

            try:
                con = lite.connect(DB_PATH)
                user_rssList = []

                with connection.cursor() as cursor:
                    cursor.execute("SELECT link,title FROM rebels_rss INNER JOIN rebels_userrss ON rebels_rss.rssId=rebels_userrss.rssId_id WHERE rebels_userrss.is_deleted=1 AND rebels_userrss.userId_id= %s ORDER BY date_rss DESC", [user_id])
                    # This list contains the RSS title and Link of the user RSS.
                    rssList = cursor.fetchall()

                    for r in rssList:
                        user_rssList.append({"rss_url" : r[0], "rss_name" : r[1]})


                con.commit()
            except Exception as e:
                print("Error: ", e.args[0])
                #sys.exit(1)
            finally:
                if con:
                    con.close()

        except TypeError:
            pass

        return user_rssList

#########################

# This query returns the recent articles regarding the user's id. Sorted with descending date order.
def UserArticles(request):
    if request.user.is_authenticated():
        # bring the user's rss id
        try:
            user_id = request.user.id

            try:
                con = lite.connect(DB_PATH)

                with connection.cursor() as cursor:
                    cursor.execute("SELECT * FROM rebels_article INNER JOIN rebels_rank ON rebels_article.articleId=rebels_rank.articleId_id WHERE rebels_rank.is_deleted=1 AND rebels_rank.userId_id=%s ORDER BY date DESC", [user_id])
                    # This list contains the RSS title and Link of the user RSS.
                    user_articleList = cursor.fetchall()



                con.commit()
            except Exception as e:
                print("Error: ", e.args[0])
                #sys.exit(1)
            finally:
                if con:
                    con.close()
        except TypeError:
            pass

    return user_articleList

###############################
# This query returns the top suggested RSS
def SuggestedRSS(user_id):

    #if request.user.is_authenticated():
        # bring the user's rss id
        try:
            try:
                con = lite.connect(DB_PATH)

                user_suggestedList=[]
                popularRSS_cont = []
                userRssList_cont = []

                with connection.cursor() as cursor:
                    #cursor.execute("SELECT   link, title, COUNT(rssId_id) AS dupe_cnt FROM rebels_userrss INNER JOIN rebels_rss ON rebels_rss.rssId=rebels_userrss.rssId_id WHERE rebels_userrss.userId_id<>%s GROUP BY rssId_id HAVING COUNT(rssId_id) >= 1 ORDER BY COUNT(rssId_id) DESC", [user_id])
                    # This list contains the RSS title and Link of the user RSS.
                    cursor.execute("SELECT COUNT(rssId_id), rssId_id FROM rebels_userrss GROUP BY rssId_id ORDER BY COUNT(rssId_id) DESC")
                    popularRSS = cursor.fetchall()
                    for p in popularRSS:
                        popularRSS_cont.append([p[0], p[1]])

                    cursor.execute("SELECT rssId_id FROM rebels_userrss WHERE userId_id=%s", [user_id])
                    userRssList = cursor.fetchall()
                    for u in userRssList:
                        userRssList_cont.append(u[0])


                    for p in range(0, len(popularRSS_cont)):
                        flag=True
                        #print("check outer loop")
                        pa = popularRSS_cont[p][1]
                        for u in range(0, len(userRssList_cont)):
                            ua = userRssList_cont[u]
                            #print("check inner loop")
                            if ua==pa:
                                #print("check"+str(u)+str(p))
                                flag=False
                                break
                        if flag:
                            cursor.execute("SELECT link, title FROM rebels_rss WHERE rssId=%s", [pa])
                            s = cursor.fetchone()
                            user_suggestedList.append({"rss_url" : s[0], "rss_name" : s[1]})


                con.commit()
            except Exception as e:
                print("Error: ", e.args[0])
                #sys.exit(1)
            finally:
                if con:
                    con.close()

        except TypeError:
            pass

        return user_suggestedList
######### This section is for the is_deleted param ######################
def ArticleExists(articleId):
    with connection.cursor() as cursor:
        cursor.execution("UPDATE rebels_article SET is_deleted=3 WHERE rebels_article.id=articleId")
        return

def DeleteRSSfromList(request, rss_url):
    if request.user.is_authenticated():
        # bring the user's rss id
        try:
            use_id = request.user.id
            try:
                con = lite.connect(DB_PATH)

                with connection.cursor() as cursor:
                    cursor.execute("SELECT rssId FROM rebels_rss WHERE link=%s", [rss_url])
                    # This list contains the RSS title and Link of the user RSS.
                    rss_id = cursor.fetchone()

                    cursor.execute("UPDATE rebels_userrss SET is_deleted=3 WHERE rssId_id=%s AND userId_id=%s", [rss_id], [user_id])

                con.commit()

            except Exception as e:
                print("Error: ", e.args[0])
                #sys.exit(1)
            finally:
                if con:
                    con.close()

        except TypeError:
            pass

        #return user_suggestedList

############ Add suggested Rss to the user ###########################
def AddSuggestedRss(request, rss_url):
    if request.user.is_authenticated():
        # bring the user's rss id
        try:
            use_id = request.user.id
            try:
                con = lite.connect(DB_PATH)

                with connection.cursor() as cursor:
                    cursor.execute("SELECT rssId FROM rebels_rss WHERE link=%s", [rss_url])
                    # This list contains the RSS title and Link of the user RSS.
                    rss_id = cursor.fetchone()
                    # check if RSS exists
                    cursor.execute("SELECT is_deleted FROM rebels_userrss WHERE rssId_id=%s AND userId_id=%s", [rss_id], [user_id])
                    check = cursor.fetchone()
                    if check==3:
                        cursor.execute("UPDATE rebels_userrss SET is_deleted=1 WHERE rssId_id=%s AND userId_id=%s", [rss_id], [user_id])
                    else:
                        cursor.execute("INSERT INTO rebels_userrss (rssId_id, userId_id, is_deleted) VALUES (%s, $s, 1)", [rss_id], [user_id])

                con.commit()

            except Exception as e:
                print("Error: ", e.args[0])
                #sys.exit(1)
            finally:
                if con:
                    con.close()

        except TypeError:
            pass

        #return user_suggestedList

######### This section is for the Insert Into query ##################
# as a parameter I will use a context_dict
# The requirement is that the context_dict must contain the following attributes:
# link, title, description, date

##
def AddNewRSS(request, response):
    # RSS table has 4 main attributes plus the is_deleted attribute which will be default==1
    # I will assign all values to parameters before the query
    link = response["add_url"]
    title = response["rss_title"]
    desc = response["rss_desc"]
    date = datetime.datetime.now()

    if request.user.is_authenticated():
        # bring the user's rss id
        try:
            use_id = request.user.id
            try:
                con = lite.connect(DB_PATH)

                with connection.cursor() as cursor:
                    cursor.execution("INSERT INTO rebels_rss(link, title, description. date_rss) VALUES(%s,%s,%s,%s)",[link],[title],[desc],[date])
                    # bring the rss id to add it to userRssList
                    cursor.execute("SELECT rssId FROM rebels_rss WHERE link=%s",[link])
                    rss_id = cursor.fetchone()
                    cursor.execute("INSERT INTO rebels_userrss (rssId_id, userId_id, is_deleted) VALUES (%s, $s, 1)", [rss_id], [user_id])
                con.commit()

            except Exception as e:
                print("Error: ", e.args[0])
                #sys.exit(1)
            finally:
                if con:
                    con.close()

        except TypeError:
            pass


def InsertArticle(context_dict):
    url = context_dict["url"]
    title = context_dict["title"]
    description = context_dict["description"]
    body = context_dict["body"]
    author = context_dict["author"]
    date = context_dict["date"]
    with connection.cursor() as cursor:
        cursor.execution("INSERT INTO (url,title,description,body,author,date) VALUES(%s,%s,%s,%s,%s,%s)",[url],[title],[description],[body],[author],[date])
        return
######################## Update user details #############################3
def UpdateUserDetails(request, response):
    # RSS table has 4 main attributes plus the is_deleted attribute which will be default==1
    # I will assign all values to parameters before the query
    first = response["first_name"]
    last = response["last_name"]
    username = response["username"]
    email = response["email"]
    password = response["password"]

    flag = 0
    if request.user.is_authenticated():
        # bring the user's rss id
        try:
            user_id = request.user.id
            try:
                con = lite.connect(DB_PATH)

                with connection.cursor() as cursor:
                    ##email check
                    cursor.execute("SELECT id FROM auth_user WHERE email=%s", [email])
                    e = cursor.fetchone()
                    if e is not None:
                        if e[0] > 0:
                            flag=2
                            return flag
                    ##usename check
                    cursor.execute("SELECT id FROM auth_user WHERE username=%s", [username])
                    p = cursor.fetchone()
                    if p is not None:
                        if p[0] > 0:
                            flag=False
                            return 1
                    #update each field seperately
                    if not first=="":
                        cursor.execute("UPDATE auth_user SET first_name=%s WHERE id=%s", [first, user_id])
                        print(" first name ok")
                    if not last=="":
                        cursor.execute("UPDATE auth_user SET last_name=%s WHERE id=%s", [last, user_id])
                        print(" last name ok")
                    if not username=="":
                        cursor.execute("UPDATE auth_user SET username=%s WHERE id=%s", [username, user_id])
                        print(" username name ok")
                    if not email=="":
                        cursor.execute("UPDATE auth_user SET email=%s WHERE id=%s", [email, user_id])
                        print(" email name ok")
                    if not password=="":
                        cursor.execute("UPDATE auth_user SET password=%s WHERE id=%s", [password, user_id])
                        print(" password name ok")
                con.commit()

            except Exception as e:
                print("Error: ", e.args[0])
                #sys.exit(1)
            finally:
                if con:
                    con.close()

        except TypeError:
            pass

        return flag


########################## Registration check #################################
def CheckForUniqueEmail(email):
    # RSS table has 4 main attributes plus the is_deleted attribute which will be default==1
    # I will assign all values to parameters before the query
    flag = False

    # bring the user's rss id
    try:

        try:
            con = lite.connect(DB_PATH)

            with connection.cursor() as cursor:
                ##email check
                #print(email)
                if not email=="":
                    cursor.execute("SELECT id FROM auth_user WHERE email=%s", [email])
                    e = cursor.fetchone()
                    #print("the query returned: "+str(e))
                    if e is not None:
                        if e[0] > 0:
                            flag=True
                            return flag
                else:
                    flag=True
                    return flag
            con.commit()

        except Exception as e:
            print("Error: ", e.args[0])

        finally:
            if con:
                con.close()

    except TypeError:
        pass

    return flag
