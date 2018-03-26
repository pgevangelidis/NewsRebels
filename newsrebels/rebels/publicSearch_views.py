from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required
from rebels.crawler_queries import PublicAllArticles
from rebels.forms import UserForm  #, UserProfileForm
from datetime import datetime
from django.core.urlresolvers import reverse
from django.views.generic.edit import CreateView

import re
import json

from django.core.serializers.json import DjangoJSONEncoder
from django.http import JsonResponse

from rebels.IR_function import return_indexs_of_the_most_relevant_articles

def publicSearch(request):
	request.session.set_test_cookie()
	return render(request, 'rebels/publicSearch.html',)



def public_search_for_relevant_articles(request):

	response = None
	data = {}
	print(request)
	if request.is_ajax():
		if request.method == 'POST':
			#print(request.body)
			response = json.loads(request.body)
			print("the query to be searched is: " ,  response["query"]  )
			if response:

				### Pros Paulo
				allArticles_dict = PublicAllArticles(0)
				### fortwse ola ta arthra p exei o xrhsths

				json_articles = json.dumps(return_indexs_of_the_most_relevant_articles({ "articles": allArticles_dict } ,  response["query"]  ), cls=DjangoJSONEncoder)

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
