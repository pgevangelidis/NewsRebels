from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required
from rebels.forms import UserForm  #, UserProfileForm
from rebels.crawler_queries import AddArticleUser
from datetime import datetime
from django.core.urlresolvers import reverse
from django.views.generic.edit import CreateView

import re
import json

from django.http import JsonResponse



@login_required(login_url='/rebels/')
def read_more_btn(request):

    response = None
    data = {}
    print(request)
    if request.is_ajax():
        if request.method == 'POST':
            #print(request.body)
            response = json.loads(request.body)
            print("the article url the user read is: " ,  response["url"] )
            if response:

                #### PROS Paulo
                AddArticleUser(request,response["url"])
                #### edw na pareis to url kai to id tou xrhsth kai pernata sth bash mazi me mia hmeromhnia gia to pote ta diavase

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
