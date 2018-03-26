from django.shortcuts import render, redirect
from django.contrib.auth import authenticate
# This script contains QUERIES for the database
import sqlite3 as lite
# This script contains QUERIES for the database
from django.db import connection
from datetime import timedelta, datetime
import sys
import os
import re
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DB_PATH = os.path.join(BASE_DIR, 'db.sqlite3')


def remove_tags(text):
    TAG_RE = re.compile(r'<[^>]+>')
    return TAG_RE.sub('', text)


def RSStoCrawl(next_toCrawl):
    if next_toCrawl==True:
    # bring the user's rss id
        try:

            try:
                con = lite.connect(DB_PATH)
                rss_tocrawl=[]

                d = timedelta()
                with connection.cursor() as cursor:
                    cursor.execute("SELECT link, title, date_rss, rssId FROM rebels_rss ORDER BY date_rss ASC")
                    # This list contains the RSS title and Link of the user RSS.
                    lastTimeCrawled = cursor.fetchone()
                    print(lastTimeCrawled)

                    if lastTimeCrawled[2] is None:
                        last = datetime.now()
                        print(last)
                        cursor.execute("UPDATE rebels_rss SET date_rss=%s WHERE rssId=%s", [last, lastTimeCrawled[3]])
                    else:
                        last = lastTimeCrawled[2].replace(second=0, microsecond=0)

                    recentTimeCrawled = datetime.now()

                    recent = recentTimeCrawled.replace(second=0, microsecond=0)
                    print(recent)
                    d = recent-last
                    print(d)
                    minutes = d.days*1440 + d.seconds/60
                    print(minutes)

                    if minutes > 59:
                        rss_tocrawl=[lastTimeCrawled[0],"ok"]
                        ## Now I will update the crawling time:
                        cursor.execute("UPDATE rebels_rss SET date_rss=%s WHERE rssId=%s", [recentTimeCrawled, lastTimeCrawled[3]])
                    else:
                        rss_tocrawl=["","notOk"]

                    con.commit()
            except Exception as e:
                print("Error: ", e.args[0])
                #sys.exit(1)
            finally:
                if con:
                    con.close()

        except TypeError:
            pass
        return rss_tocrawl
    else:
        rss_tocrawl=["","notOk"]
        return rss_tocrawl

####################### crawl rss feeds #################################
# This query returns the top suggested RSS
def CrawledRSSFeeds(response, rss_url):
    # the attirbutes in response are:
    # 'url' 'desciption' 'title' 'thumbnail' 'body'
    print("\n================================\n")
    print("\nHere is the prints from the CrawledRSSFeeds the query:\n")
    title = response["title"]
    print(title)
    description = remove_tags(response["description"])
    print(description)
    url = response["link"]
    print(url)
    thumbnail = response["thumbnail"]
    print(thumbnail)
    add_date = datetime.now()
    print(add_date)
    print("Also the rss url: ", rss_url)
    print("\n================================\n")
    # bring the user's rss id
    try:
        try:
            con = lite.connect(DB_PATH)

            with connection.cursor() as cursor:
                # find the rss Id from url

                cursor.execute("SELECT rssId FROM rebels_rss WHERE link=%s",[rss_url])
                rssId = cursor.fetchone()
                #check if url exists!!

                if rssId is not None:
                    #check if article exists in the database:
                    cursor.execute("SELECT articleId FROM rebels_article WHERE url=%s", [url])
                    exist = cursor.fetchone()

                    print("******does the article exists?: %s*******", exist)

                    if exist is None:
                        cursor.execute("INSERT INTO rebels_article (title, description, url, thumbnail, date, body, author) VALUES (%s, %s, %s, %s, %s, '', '')", [title, description, url, thumbnail, add_date])

                    else:
                        cursor.execute("SELECT rssId_id FROM rebels_articlerss WHERE articleId_id=%s", [exist[0]])
                        is_rss_inlist = cursor.fetchone()

                        if is_rss_inlist is None:
                            cursor.execute("INSERT INTO rebels_articlerss (rssId_id, articleId_id, is_deleted) VALUES(%s, %s, 1) ", [rssId[0], exist[0]])

            con.commit()
        except Exception as e:
            print("Error: ", e.args[0])
            #sys.exit(1)
        finally:
            if con:
                con.close()

    except TypeError:
        pass

################# Function for Stefanos ############################
#### This query returns all the articles of the user RSS #######
def UserAllArticles(request, loaded_data):
    if request.user.is_authenticated():
        try:
            user_id=request.user.id
            allArticles_dict = []
            try:
                con = lite.connect(DB_PATH)
                with connection.cursor() as cursor:
                    cursor.execute("SELECT thumbnail, title, description, url, date FROM rebels_article INNER JOIN rebels_articlerss ON rebels_article.articleId=rebels_articlerss.articleId_id INNER JOIN rebels_userrss ON rebels_articlerss.rssId_id=rebels_userrss.rssId_id WHERE userId_id=%s LIMIT %s, 10", [user_id, loaded_data])
                    allArticles = cursor.fetchall()

                    for ar in allArticles:
                        allArticles_dict.append({"image" : ar[0], "title" : ar[1], "description" : ar[2], "source" : ar[3], "date" : ar[4]})

                loaded_data = loaded_data + 10
                con.commit()
            except Exception as e:
                print("Error: ", e.args[0])
            finally:
                if con:
                    con.close()

        except TypeError:
            pass
        return allArticles_dict
##########################################
##########################################
def LatestReadArticles(request,loaded_data):
    if request.user.is_authenticated():
        try:
            user_id=request.user.id
            latestRead_dict = []
            try:
                con = lite.connect(DB_PATH)
                with connection.cursor() as cursor:
                    cursor.execute("SELECT thumbnail, title, description, url, date FROM rebels_article INNER JOIN rebels_hasread ON rebels_article.articleId=rebels_hasread.articleId_id WHERE userId_id=%s AND has_read=1 LIMIT %s, 10 ORDER BY date DESC", [user_id, loaded_data])
                    allArticles = cursor.fetchall()

                    for ar in allArticles:
                        latestRead_dict.append({"image" : ar[0], "title" : ar[1], "description" : ar[2], "source" : ar[3], "date" : ar[4]})

                loaded_data = loaded_data + 10
                con.commit()
            except Exception as e:
                print("Error: ", e.args[0])
            finally:
                if con:
                    con.close()

        except TypeError:
            pass
        return latestRead_dict
##########################################
##########################################
def AddArticleUser(request,url):
    if request.user.is_authenticated():
        try:
            h=0
            url = url.split('http://localhost:8000/rebels/article/?target_url=')
            print("the new url is: ", url[1])
            user_id=request.user.id
            try:
                con = lite.connect(DB_PATH)
                with connection.cursor() as cursor:
                    cursor.execute("SELECT articleId FROM rebels_article WHERE url=%s", [url[1]])
                    artId = cursor.fetchone()
                    print("is artId still none: ",)
                    cursor.execute("SELECT has_read FROM rebels_hasread WHERE userId_id=%s AND articleId_id=%s", [user_id, url[1]])
                    hr_o = cursor.fetchone()

                    if hr_o is None:
                        hr = 1
                        print("Is none")
                    else:
                        hr = hr_o[0] + 1
                        print("is not none")

                    read_date = datetime.now()
                    cursor.execute("INSERT INTO rebels_hasread (userId_id, articleId_id, has_read, has_read_date) VALUES (%s, %s, %s, %s) ", [user_id, artId[0], hr, read_date])

                con.commit()
            except Exception as e:
                print("Error: ", e.args[0])
            finally:
                if con:
                    con.close()

        except TypeError:
            pass
#############################################
#############################################
def PublicAllArticles(loaded_data):

    try:
        allArticles_dict = []
        try:
            con = lite.connect(DB_PATH)
            with connection.cursor() as cursor:
                cursor.execute("SELECT thumbnail, title, description, url, date FROM rebels_article LIMIT %s, 50", [loaded_data])
                allArticles = cursor.fetchall()

                for ar in allArticles:
                    allArticles_dict.append({"image" : ar[0], "title" : ar[1], "description" : ar[2], "source" : ar[3], "date" : ar[4]})

            loaded_data = loaded_data + 10
            con.commit()
        except Exception as e:
            print("Error: ", e.args[0])
        finally:
            if con:
                con.close()

    except TypeError:
        pass
    return allArticles_dict
