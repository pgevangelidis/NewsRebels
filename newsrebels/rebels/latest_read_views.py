from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required
from rebels.forms import UserForm  #, UserProfileForm
from rebels.crawler_queries import LatestReadArticles
from datetime import datetime
from django.core.urlresolvers import reverse
from django.views.generic.edit import CreateView

import re
import json
from django.core.serializers.json import DjangoJSONEncoder
from django.http import JsonResponse


@login_required(login_url='/rebels/')
def latest_read(request):

    latestArticles_dict = LatestReadArticles(request,0)

    json_latest_read_articles = json.dumps({ "articles": latestArticles_dict }, cls=DjangoJSONEncoder)
    print("kati")
    print(json_latest_read_articles)
    return render(request, 'rebels/latest_read.html' , {'json_latest_read_articles' : json_latest_read_articles})



@login_required(login_url='/rebels/')
def latest_read_load_more_articles(request):
    latest_read=0
    response = None
    data = {}
    print(request)
    if request.is_ajax():
        if request.method == 'POST':
            #print(request.body)
            response = json.loads(request.body)
            print("the number of elements that are already loaded: " ,  len(response["articles"]) )
            if response:
                ### Pros Paulo
                print("the next are the urls that are already loaded and you should not retrieve them from the base")
                for ele in response["articles"]:
                    print("url: " , ele["url"])
                    loaded_data = loaded_data + 1


                latestArticles_dict = LatestReadArticles(request,loaded_data)
                json_articles = json.dumps({ "articles": latestArticles_dict}, cls=DjangoJSONEncoder)

                data["json_articles"] = json_articles
                data["status"] = "ok"

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
