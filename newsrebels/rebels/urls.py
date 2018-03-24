from django.conf.urls import url
from rebels import views
from django.conf.urls import include

from rebels import profile_views
from rebels import crawler_views

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
	url(r'^logout/$', views.user_logout, name='logout'),
	url(r'^accounts/', include('registration.backends.simple.urls')),
	url(r'^oauth/', include('social_django.urls', namespace='social')), #<-- for social login


	#add profile views
	url(r'^profile/$', profile_views.profile, name = 'profile'),
	#profile ajax calls
	url(r'^delete_rss_from_user/$', profile_views.delete_rss_from_user, name='delete_rss_from_user'),
	url(r'^add_rss_to_user/$', profile_views.add_rss_to_user, name='add_rss_to_user'),
	url(r'^add_sug_rss_to_user/$', profile_views.add_sug_rss_to_user, name='add_sug_rss_to_user'),
	url(r'^update_user_settings/$', profile_views.update_user_settings, name='update_user_settings'),

	#add crawler views
    url(r'^crawl_rss_feed/$', crawler_views.crawl_rss_feeds, name='crawl_rss_feeds'),
	url(r'^get_first_link_to_crawl/$', crawler_views.get_first_link_to_crawl, name='get_first_link_to_crawl'),
]
