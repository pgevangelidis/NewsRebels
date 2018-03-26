from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from rebels.models import UserProfile, RSS, Article, Rank, UserRSS, RssArticle
# This script contains QUERIES for the database
from django.db import connection

# This query returns the user details. 1 row all attributes

def profile(request):
    #user_profile = None

    if request.user.is_authenticated():
        # bring the user's rss id
        try:
            user_id = request.user.id
            print(user_id)
            user_rss = UserRSS.objects.filter(userId=user_id)
            print(user_rss_id.rssId)
            #print("The user profile is: %f", [user_profile.objects.all()])
            #user_id = user_profile.get(id)
            #print(user_id)
        except TypeError:
            pass


        rss_dict = {}
        rss = RSS.objects.filter(rssId__userrss_rssId__userrss_useId=id).filter(is_deleted=1)
        rss_dict = {"title": rss.title}
        rss_dict = {"link": rss.link}
        print(rss.title)
        print(rss.link)
        print(rss_dict)
        return rss_dict

# This query returns a query set of all RSS for a specific user.
def UserRSS(userid):
    with connection.cursor() as cursor:
        cursor.execute("SELECT * FROM rebels_rss INNER JOIN rebels_rss_UserRss ON rebels_rss.rssId = rebels_rss_UserRss.rss_id WHERE rebels_rss_UserRss.user_id= %s ORDER BY rebels_rss.date_rss DESC", [userid])
        rssList = cursor.fetchall()
        return rssList

# This query returns the recent articles regarding the user's id. Sorted with descending date order.
def UserArticles(userid):
    with connection.cursor() as cursor:
        cursor.execute("SELECT * FROM rebels_article INNER JOIN rebels_rank ON rebels_article.id=rebels_rank.articleId_id WHERE rebels_rank.userId_id=1 AND rebels_article.is_deleted<>3 ORDER BY rebels_article.date DESC")
        articleList = cursor.fetchall()
        return articleList

# This query returns the top suggested RSS
def SuggestedRSS(self):
    with connection.cursor() as cursor:
        cursor.execution("SELECT * FROM rebels_rss INNER JOIN rebels_rss_UserRss ON rebels_rss.rssId = rebels_rss_UserRss.rss_id WHERE rebels_rss.is_deleted<>3 ORDER BY rebels_rss.date_rss ASC")
        suggestedList = cursor.fetchall()
        return suggestedList

######### This section is for the is_deleted param ######################
def ArticleExists(articleId):
    with connection.cursor() as cursor:
        cursor.execution("UPDATE rebels_article SET is_deleted=3 WHERE rebels_article.id=articleId")
        return

def RSSExists(rssId):
    with connection.cursor() as cursor:
        cursor.execution("UPDATE rebels_rss SET is_deleted=3 WHERE rebels_rss.rssId=rssId")
        return

######### This section is for the Insert Into query ##################
# as a parameter I will use a context_dict
# The requirement is that the context_dict must contain the following attributes:
# link, title, description, date

##
def InsertRSS(context_dict):
    # RSS table has 4 main attributes plus the is_deleted attribute which will be default==1
    # I will assign all values to parameters before the query
    link = context_dict["link"]
    title = context_dict["title"]
    desc = context_dict["description"]
    date = context_dict["date"]
    with connection.cursor() as cursor:
        cursor.execution("INSERT INTO rebels_rss(link, title, description. date_rss) VALUES(%s,%s,%s,%s)",[link],[title],[desc],[date])
        return

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
