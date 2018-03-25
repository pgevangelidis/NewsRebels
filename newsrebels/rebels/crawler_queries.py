from django.shortcuts import render, redirect
import datetime
from django.contrib.auth import authenticate
# This script contains QUERIES for the database
import sqlite3 as lite
# This script contains QUERIES for the database
from django.db import connection
from datetime import timedelta
import sys
import os
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DB_PATH = os.path.join(BASE_DIR, 'db.sqlite3')

def RSStoCrawl(request):
    # if request.user.is_authenticated():
    # bring the user's rss id
    try:

        try:
            con = lite.connect(DB_PATH)
            rss_tocrawl=[]
            d = timedelta()
            with connection.cursor() as cursor:
                cursor.execute("SELECT link, title, date_rss FROM rebels_rss ORDER BY date_rss ASC")
                # This list contains the RSS title and Link of the user RSS.
                lastTimeCrawled = cursor.fetchone()
                print(lastTimeCrawled)
                recentTimeCrawled = datetime.now()
                last = lastTimeCrawled.replace(second=0, microsecond=0)
                recent = recentTimeCrawled.replace(second=0, microsecond=0)
                d = recent-last
                minutes=d.days*1440+d.second/60
                print(minutes)

                if minutes > 30:
                    rss_tocrawl=[lastTimeCrawled[0],"ok"]
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
