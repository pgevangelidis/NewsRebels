from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required
from rebels.forms import UserForm  #, UserProfileForm
from datetime import datetime
from django.core.urlresolvers import reverse
from django.views.generic.edit import CreateView
from rebels.queries import UserDetails, UserRSS, SuggestedRSS, DeleteRSSfromList, AddSuggestedRss, AddNewRSS, UpdateUserDetails
import re
import json

# A helper method
@login_required(login_url='/rebels/')
def get_server_side_cookie(request, cookie, default_val=None):
	val = request.session.get(cookie)
	if not val:
		val = default_val
	return val

@login_required(login_url='/rebels/')
def visitor_cookie_handler(request):
	# Get the number of visits to the site.
	# We use the COOKIES.get() function to obtain the visits cookie.
	# If the cookie exists, the value returned is casted to an integer.
	# If the cookie doesn't exist, then the default value of 1 is used.
	visits = int(get_server_side_cookie(request,'visits', '1'))
	last_visit_cookie = get_server_side_cookie(request,'last_visit', str(datetime.now()))
	last_visit_time = datetime.strptime(last_visit_cookie[:-7],	'%Y-%m-%d %H:%M:%S')
	# If it's been more than a day since the last visit...
	if (datetime.now() - last_visit_time).days > 0:
		visits = visits + 1
		# Update the last visit cookie now that we have updated the count
		request.session['last_visit'] = str(datetime.now())
	else:
		visits = 1
		# Set the last visit cookie
		request.session['last_visit'] = last_visit_cookie
	# Update/set the visits cookie
	request.session['visits'] = visits
    # response.set_cookie('visits', visits)

## Username field validation in register view, with ajax
#class SignUpView(CreateView):
#	template_name = 'templates/rebels/register.html'
#	form_class = UserCreationForm

@login_required(login_url='/rebels/')
def profile(request):
	request.session.set_test_cookie()

	#### PROS paulo:
	if request.user.is_authenticated():
		user_id = request.user.id
		user_details = UserDetails(user_id)
		#### -----> edw na kaneis load ta dedomena apo th vash
		usrName = user_details[0]
		fName = user_details[1]
		lName = user_details[2]
		date = user_details[4]

		user_rssList = UserRSS(user_id)
		user_suggestedList = SuggestedRSS(user_id)

		data = user_rssList
		sug_data = user_suggestedList

	return render(request, 'rebels/profile.html', {'username': usrName, 'fname': fName, 'lname': lName , 'date': date , 'data' : data , 'sug_data': sug_data })

from django.http import JsonResponse

'''
#if you want to exempt a view from csrf use the next two lines
from django.views.decorators.csrf import csrf_exempt
@csrf_exempt
'''
@login_required(login_url='/rebels/')
def add_sug_rss_to_user(request):
    #https://docs.djangoproject.com/en/1.9/ref/csrf/
	response = None
	data = {}
	print(request)
	if request.is_ajax():
		if request.method == 'POST':
			#print(request.body)
			response = json.loads(request.body)
			print("the suggested url for add is: " ,  response["sug_url_to_add"])
			if response:
				#### PROS paulo:
				#### -----> edw na peraseis ta suggested sth bash prwta omws elegkse oti autos o user den exei hdh auto to rss
				AddSuggestedRss(request, response["sug_url_to_add"])
				#### -----> (elegkse kai oti de tha erthoun apo th javascript parapanw apo ena (se periptwsh epitheshs))

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

@login_required(login_url='/rebels/')
def add_rss_to_user(request):
    #https://docs.djangoproject.com/en/1.9/ref/csrf/
	response = None
	data = {}
	print(request)
	if request.is_ajax():
		if request.method == 'POST':
			print(request.body)
			response = json.loads(request.body)
			print("\n\nthe new rss url to be added is: " , response["add_url"])
			print("the new rss title to be added is: " , response["rss_title"])
			print("the new rss description to be added is: " , response["rss_desc"])
			print("\n\n")
			if response:
				#### PROS paulo:
				#### -----> edw na peraseis to rss sth bash prwta omws elegkse oti autos o user den exei hdh auto to rss
				AddNewRSS(request, response)
				#### -----> (elegkse kai oti de tha erthoun apo th javascript parapanw apo ena (se periptwsh epitheshs))

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


@login_required(login_url='/rebels/')
def delete_rss_from_user(request):
	#https://docs.djangoproject.com/en/1.9/ref/csrf/
	response = None
	data = {}
	print(request)
	if request.is_ajax():
		if request.method == 'POST' and request.user.is_authenticated():
			#print(request.body)
			response = json.loads(request.body)
			print("eleos")
			print("the url for delete is: " ,  response["url_to_delete"])


			if response:
				print("check")
				#### PROS paulo:
				#### -----> edw na diegrapse to rss apo th  bash (isDeleted = numOfDelete) prwta omws elegkse oti autos o user den exei hdh auto to rss
				DeleteRSSfromList(request, response["url_to_delete"])
				#### -----> (elegkse kai oti de tha erthoun apo th javascript parapanw apo ena (se periptwsh epitheshs))

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


@login_required(login_url='/rebels/')
def update_user_settings(request):
    #https://docs.djangoproject.com/en/1.9/ref/csrf/
	response = None
	data = {}
	print(request)
	if request.is_ajax():
		if request.method == 'POST':
			print(request.body)
			response = json.loads(request.body)
			print("\n\nthe user's first name to be updated is: " , response["first_name"])
			print("the user's last name to be updated is: " , response["last_name"])
			print("the user's username to be updated is: " , response["username"])
			print("the user's email to be updated is: " , response["email"])
			print("the user's password to be updated is: " , response["password"])
			print("\n\n")
			if response:
				#### PROS paulo:
				#### -----> edw kane update ta dedomena tou xrhsth  (ama kaneis update to password elegkse oti ta duo password p erxontai tairiazoun)
				flag = UpdateUserDetails(request, response)

				### an uparxei to usename h to email na epistrepseis:
				if flag==1:
					data["status"] = "notOk"
					data["message"] = "Username not available! Someone else has this Username."
				elif flag==2:
					data["status"] = "notOk"
					data["message"] = "Email not available! Someone else has this Email."
				else:
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
