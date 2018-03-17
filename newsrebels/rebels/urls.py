from django.conf.urls import url
from rebels import views
from django.conf.urls import include

urlpatterns = [
	url(r'^$', views.index, name = 'index'),
	url(r'^about/$', views.about, name = 'about'),
    url(r'^terms_and_conditions/$', views.terms_and_conditions, name='termsConditions'),
    url(r'^suggested/$', views.suggested, name='suggested'),
    url(r'^article/$', views.article, name='article'),
    url(r'^latest_read/$', views.latest_read, name='latest_read'),
    url(r'^search/$', views.search, name='search'),
	url(r'^register/$', views.register, name='register'),
	url(r'^login/$', views.user_login, name='login'),
	url(r'^restricted/', views.restricted, name='restricted'),
	url(r'^logout/$', views.user_logout, name='logout'),
	url(r'^accounts/', include('registration.backends.simple.urls')),
	url(r'^oauth/', include('social_django.urls', namespace='social')), #<-- for social login
]
