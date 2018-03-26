from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required
from rebels.crawler_queries import RSStoCrawl, CrawledRSSFeeds
from rebels.forms import UserForm  #, UserProfileForm
from datetime import datetime
from django.core.urlresolvers import reverse
from django.views.generic.edit import CreateView

import re
import json

from django.http import JsonResponse



#code taken from: https://tutorialedge.net/python/removing-html-from-string/
def remove_tags(text):
    TAG_RE = re.compile(r'<[^>]+>')
    return TAG_RE.sub('', text)


def get_first_link_to_crawl(request):
    #https://docs.djangoproject.com/en/1.9/ref/csrf/
    response = None
    data = {}
    print(request)
    if request.is_ajax():
        if request.method == 'POST':
            #print(request.body)
            response = json.loads(request.body)
            print("Check fr crawl: %s", response["getLink"])
            if response:

                ### Pros Paulo
                rss_toCrawl = RSStoCrawl(response["getLink"])
                ### epestrepse apo th bash to rss p exei ton pio polu kairo na ginei crawled
                ### epishs ama exei ginei crawled thn teleutaia wra mh to ksanakaneis
                ### kai apla epestrepse data["status"] = notOk
                print(rss_toCrawl[0])
                print(rss_toCrawl[1])
                data["link"] = rss_toCrawl[0]

                data["status"] = rss_toCrawl[1]

                return JsonResponse(data)
            else:
                data["status"] = "notOk"
                data["message"] = "the response was empty"
                return JsonResponse(data)
        else:
            data["status"] = "notOk"
            data["message"] = "this is not a get method, post needed"
            return JsonResponse(data)
    else:
        data["status"] = "notOk"
        data["message"] = "this is not an ajax request"
        return JsonResponse(data)


def crawl_rss_feeds(request):
    #https://docs.djangoproject.com/en/1.9/ref/csrf/
    response = None
    data = {}
    print("This is the request %s",request)
    if request.is_ajax():
        if request.method == 'POST':
            #print(request.body)
            response = json.loads(request.body)
            print(response["response"]["feed"]["title"])
            if response:

                ### Pros Paulo
                rss_url = response['rss_url']
                ### mesa sto parakatw loop kane insert ta kainourgia article
                for ele in response["response"]["items"]:
                    print("Does the element has author? %s",ele["author"])
                    print(ele["title"])
                    print(remove_tags(ele["description"]) )
                    print(ele["link"])
                    print(ele["thumbnail"])
                    print("\n")
                    # Now add the article to the base.
                    CrawledRSSFeeds(ele, rss_url)


                ### Pros Paulo (auth h leitourgeia einai idia me thn panw)
                #element = response["response"]["items"]
                next_toCrawl = True
                rss_toCrawl = RSStoCrawl(next_toCrawl)
                ### epestrepse apo th bash to rss p exei ton pio polu kairo na ginei crawled
                ### epishs ama exei ginei crawled thn teleutaia wra mh to ksanakaneis
                ### kai apla epestrepse data["status"] = notOk

                data["status"] = rss_toCrawl[1]
                data["link"] = rss_toCrawl[0]

                ### Pros Paulo
                ### auto to notOk to ebala apla gia na mh spamaroume tis uphresies me ta rss esu otan kaneis ta queries tha to bgaleis
                #data["status"] = "notOk"

                return JsonResponse(data)
            else:
                data["status"] = "notOk"
                data["message"] = "the response was empty"
                return JsonResponse(data)
        else:
            data["status"] = "notOk"
            data["message"] = "this is not a get method, post needed"
            return JsonResponse(data)
    else:
        data["status"] = "notOk"
        data["message"] = "this is not an ajax request"
        return JsonResponse(data)
