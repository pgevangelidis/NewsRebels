import os
import sys
import os
import sqlite3 as lite
from datetime import datetime
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DB_PATH = os.path.join(BASE_DIR, 'db.sqlite3')
# This script contains QUERIES for the database
from django.db import connection
os.environ.setdefault('DJANGO_SETTINGS_MODULE' , 'newsrebels.settings')
import django
django.setup()


from rebels.models import UserProfile, RSS, Article, Rank, HasRead, UserRSS, ArticleRss
##edw kane import ta models



import random
from faker import Faker
from urllib.request import urlopen
from  urllib.parse import quote_plus
import json

def insert_user_to_db(fName , lName , usr , email , pwd):
    print("############  USER  ###################")
    print("First name: {}".format(fName))
    print("Last name: {}".format(lName))
    print("Username: {}".format(usr))
    print("Email: {}".format(email))
    print("Password: {}".format(pwd))

    print("\n")
    ############### the query for each user #########################
    ### edw otan kaneis insert prosekse mh o generator mas exei dosei duo fores ta idia stoixeia (ekseretika spaneia periptwsh)
        # bring the user's rss id
    try:
        try:
            con = lite.connect(DB_PATH)

            with connection.cursor() as cursor:
                ##email check
                cursor.execute("SELECT id FROM auth_user WHERE email=%s", [email])
                e = cursor.fetchone()
                cursor.execute("SELECT id FROM auth_user WHERE username=%s", [usr])
                p = cursor.fetchone()
                if e is not None:
                    if e[0] > 0:
                        print("User already exist!")
                        return
                ##usename check
                elif p is not None:
                    if p[0] > 0:
                        print("User already exists!")
                        return
                #update each field seperately
                else:
                    date_joined= datetime.now()
                    cursor.execute("INSERT INTO auth_user (first_name, last_name, username, email, password, is_superuser, is_staff, is_active, date_joined) VALUES (%s,%s,%s,%s,%s, 0, 0, 1, %s)", [fName , lName , usr , email , pwd, date_joined])
                    print(" Insertion ok")
            con.commit()
        except Exception as e:
            print("Error: ", e.args[0])
        finally:
            if con:
                con.close()

    except TypeError:
        pass

    ############################################
def insert_new_rss(url , title , description):
    print("############  RSS ###################")
    print("the url of the new rrs is: {}".format(url))
    print("the title of the new rrs is: {}".format(title))
    print("the description of the new rrs is: {}".format(description))

    print("\n")
    ############################################

    try:
        try:
            con = lite.connect(DB_PATH)
            rss_date=datetime.now()

            with connection.cursor() as cursor:
                cursor.execute("INSERT INTO rebels_rss (link, title, description, date_rss) VALUES (%s,%s,%s, %s)", [url , title , description, rss_date])
                print(" RSS insertion ok")
            con.commit()
        except Exception as e:
            print("Error: ", e.args[0])
        finally:
            if con:
                con.close()

    except TypeError:
        pass

    ############################################

def get_first_two_letters(strTemp):
    return ( len(strTemp) > 2) and  strTemp[:2] or  strTemp

def populate(rss_lib , num=10 ):
    fake_gener = Faker()
    for i in range(num):
        fName = fake_gener.first_name()
        lName = fake_gener.last_name()
        email =  fake_gener.email()
        usr = get_first_two_letters(fName) +"_"+get_first_two_letters(lName) +"_"+ get_first_two_letters(email) +"_"+str(random.randint(1,1001))

        insert_user_to_db(fName=fName , lName=lName , usr = usr , email =email , pwd = "Password@1A")

        ran_picks = random.sample(range(0, len(rss_lib)), 7)
        for i in ran_picks:
            url = "https://api.rss2json.com/v1/api.json?rss_url=" + quote_plus(rss_lib[i])
            response = urlopen(url)
            data = json.loads(response.read());

            insert_new_rss(url=rss_lib[i] , title=data['feed']['title'] , description=data['feed']['description'])

            #### PROS PAULOS:
            #### edw kane thn eisagwgh sth bash th sxesh anamesa se url kai userId
            ############################################
            try:
                try:
                    con = lite.connect(DB_PATH)

                    with connection.cursor() as cursor:
                        print("############ User RSS ###################")
                        print("I want to see the url: ", rss_lib[i])
                        cursor.execute("SELECT rssId FROM rebels_rss WHERE link=%s", [rss_lib[i]])
                        rssId_id = cursor.fetchone()
                        print("the rss id: ",rssId_id)
                        cursor.execute("SELECT id FROM auth_user WHERE username=%s", [usr])
                        userId_id = cursor.fetchone()

                        print("And the User: ", usr)
                        print("the user id: ",userId_id[0])

                        cursor.execute("INSERT INTO rebels_userrss (userId_id, rssId_id, is_deleted) VALUES (%s,%s,1)", [userId_id[0] , rssId_id[0]])
                        print(" USER RSS insertion ok")
                    con.commit()
                except Exception as e:
                    print("Error: ", e.args[0])
                finally:
                    if con:
                        con.close()

            except TypeError:
                pass

            ############################################


if __name__ == '__main__':
    rss_lib = [
                'http://feeds.bbci.co.uk/news/video_and_audio/news_front_page/rss.xml?edition=uk',
                'http://feeds.bbci.co.uk/news/rss.xml?edition=uk',
                'http://feeds.bbci.co.uk/news/world/rss.xml?edition=uk',
                'http://feeds.bbci.co.uk/news/england/rss.xml?edition=uk',
                'http://feeds.bbci.co.uk/news/northern_ireland/rss.xml?edition=uk',
                'http://feeds.bbci.co.uk/news/scotland/rss.xml?edition=uk',
                'http://feeds.bbci.co.uk/news/business/rss.xml?edition=uk',

                'http://rss.cnn.com/rss/edition.rss',
                'http://rss.cnn.com/rss/edition_world.rss',
                'http://rss.cnn.com/rss/edition_africa.rss',
                'http://rss.cnn.com/rss/edition_americas.rss',
                'http://rss.cnn.com/rss/edition_asia.rss',
                'http://rss.cnn.com/rss/edition_europe.rss',
                'http://rss.cnn.com/rss/edition_meast.rss',
                'http://rss.cnn.com/rss/edition_us.rss',
                'http://rss.cnn.com/rss/money_news_international.rss',
                'http://rss.cnn.com/rss/edition_space.rss',
                'http://rss.cnn.com/rss/edition_entertainment.rss',
                'http://rss.cnn.com/rss/edition_sport.rss',
                'http://rss.cnn.com/rss/edition_football.rss',
                'http://rss.cnn.com/rss/edition_golf.rss',
                'http://rss.cnn.com/rss/edition_motorsport.rss',

                'http://www.independent.co.uk/news/rss',
                'http://www.independent.co.uk/voices?service=rss',
                'http://www.independent.co.uk/environment/rss',
                'http://www.independent.co.uk/sport/rss',
                'http://www.independent.co.uk/life-style/rss',
                'http://www.independent.co.uk/arts-entertainment/rss',
                'http://www.independent.co.uk/travel/rss',
                'http://www.independent.co.uk/money/rss',
    ]

    populate(  rss_lib=list(set(rss_lib)) , num=2 )
