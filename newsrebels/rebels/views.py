from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required
from rebels.forms import UserForm  #, UserProfileForm
from datetime import datetime
from django.core.urlresolvers import reverse
from django.views.generic.edit import CreateView
from aylienapiclient import textapi
import re
import json




# Create your views here.
def index(request):
	if not request.user.is_authenticated():
		show_burger = True
		request.session.set_test_cookie()
		response = render(request, 'rebels/index.html', {'show_burger':show_burger})
		return response
	else:
		return HttpResponseRedirect(reverse('suggested'))

def about(request):
    request.session.set_test_cookie()
    return render(request, 'rebels/about.html',)

def register(request):
	if not request.user.is_authenticated():
		registered = False

		if request.method == 'POST':
			user_form = UserForm(data=request.POST)
			#profile_form = UserProfileForm(data=request.POST)

			if user_form.is_valid(): #and profile_form.is_valid():
				user = user_form.save()
				user.set_password(user.password)
				user.save()

				##profile = profile_form.save(commit=False)
				##profile.user = user
				#profile.save()
				#profile.user = user
				registered = True
				# Make the successful registration authenticated
				username = user_form.cleaned_data.get('username')
				password = user_form.cleaned_data.get('password')

				#user = authenticate(request, username=username, password=password)
				login(request, user, backend="django.contrib.auth.backends.ModelBackend")
				return redirect(reverse('suggested'))

			else:
				print(user_form.errors)
		else:
			user_form = UserForm()
			#profile_form = UserProfileForm()

		return render(request,'rebels/register.html', {'user_form': user_form, 'registered': registered})
	else:
		return HttpResponseRedirect(reverse('suggested'))

def user_login(request):
	#If the request is HTTP POST try to pull out the relevant information.
	if request.method == 'POST':
		# Gather the username and password provided by the user.
		# This information is obtained from the login form.
		# We use request.POST.get('<variable>') as opposed
		# to request.POST['<variable>'], because the
		# request.POST.get('<variable>') returns None if the
		# value does not exist, while request.POST['<variable>']
		# will raise a KeyError exception.
		username = request.POST.get('email')
		password = request.POST.get('password')

		# Use Django's machinery to attempt to see if the username/password
		# combination is valid - a User object is returned if it is.
		user = authenticate(username=username, password=password)
		# If we have a User object, the details are correct.
		# If None (Python's way of representing the absence of a value), no user
		# with matching credentials was found.
		if user:
			# Is the account active? It could have been disabled.
			if user.is_active:
				# If the account is valid and active, we can log the user in.
				# We'll send the user back to the homepage.
				login(request, user, backend='rebels.backends.EmailOrUsernameModelBackend')
				return HttpResponseRedirect(reverse('suggested'))
			else:
				# An inactive account was used - no logging in!
				return render(request, 'rebels/index.html' ,{'error_message': "Your rebels account is disabled!"})
		else:
			# Bad login details were provided. So we can't log the user in.
			print("Invalid login details: {0}, {1}".format(username, password))
			return render(request, 'rebels/index.html' ,{'error_message': "Invalid login details!"})

	# The request is not a HTTP POST, so display the login form.
	# This scenario would most likely be a HTTP GET.
	else:
		# No context variables to pass to the template system, hence the
		# blank dictionary object...
		return render(request, 'rebels/index.html', {})

#def some_view(request):
#	if not request.user.is_authenticated():
#		return HttpResponse("You are logged in.")
#	else:
#		return HttpResponse("You are not logged in.")


@login_required(login_url='/rebels/')
def suggested(request):
	request.session.set_test_cookie()
	return render(request, 'rebels/suggested.html')


@login_required(login_url='/rebels/')
def article(request):
	request.session.set_test_cookie()
	if request.method == 'GET' and 'target_url' in request.GET:
		target_url = request.GET['target_url']

		#here we are using Alyien API to extract info from pages
		aylien_app_id = "ba5b50f4"
		aylien_app_key = "8f80ac427e1bd4e6cadc5a153816441e"
		client = textapi.Client(aylien_app_id , aylien_app_key)
		extract = client.Extract({"url":target_url, "best_image": False})

		print(extract)

		if extract["image"] is  "":
			img = "http://maiamthienan.org/public/images/no_image.png"
		else:
			img = extract["image"]

		paras = re.split(r'[\r\n]+', extract["article"] )
		paras = ['<p>{}</p>'.format(p.strip())  for p in paras]


		return render(request,'rebels/article.html', {
														'title': extract["title"],
														'article_body': '\n'.join(paras),
														"author": extract["author"] ,
														'date': extract["publishDate"] ,
														'link': target_url ,
														'image':img
													 })
	else:
		return render(request,'rebels/missing_article.html')


#@login_required
def search(request):
	request.session.set_test_cookie()
	if request.user.is_authenticated():
		return render(request, 'rebels/search.html',)
	else:
		return HttpResponseRedirect(reverse('register'))

@login_required(login_url='/rebels/')
def latest_read(request):
    request.session.set_test_cookie()
    return render(request, 'rebels/latest_read.html',)

def terms_and_conditions(request):
    request.session.set_test_cookie()
    return render(request, 'rebels/terms_and_conditions.html',)

# Use the login_required() decorator to ensure only those logged in can
# access the view.
@login_required(login_url='/rebels/')
def user_logout(request):
	# Since we know the user is logged in, we can now just log them out.
	logout(request)
	# Take the user back to the homepage.
	return HttpResponseRedirect(reverse('index'))
