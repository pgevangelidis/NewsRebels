from django.conf.urls import url
from rebels import views
from django.conf.urls import include

from rebels import profile_views
from rebels import crawler_views
from rebels import suggested_views
from rebels import read_more_btn_view
from rebels import latest_read_views
from rebels import search_views
from rebels import publicSearch_views

urlpatterns = [
	url(r'^$', views.index, name = 'index'),
	url(r'^readMore/$', views.about, name = 'readMore'),
    url(r'^terms_and_conditions/$', views.terms_and_conditions, name='termsConditions'),
    url(r'^article/$', views.article, name='article'),
	url(r'^register/$', views.register, name='register'),
	url(r'^login/$', views.user_login, name='login'),
	url(r'^logout/$', views.user_logout, name='logout'),
	url(r'^accounts/', include('registration.backends.simple.urls')),
	url(r'^oauth/', include('social_django.urls', namespace='social')), #<-- for social login


	#add search search_views
	url(r'^search/$', search_views.search, name='search'),
	url(r'^search_for_relevant_articles/$', search_views.search_for_relevant_articles, name='search_for_relevant_articles'),

	#add public search search_views
	url(r'^publicSearch/$', publicSearch_views.publicSearch, name='publicSearch'),
	url(r'^public_search_for_relevant_articles/$', publicSearch_views.public_search_for_relevant_articles, name='public_search_for_relevant_articles'),

	#add read more button view
	url(r'^read_more_btn/$', read_more_btn_view.read_more_btn, name='suggested'),


	#add suggested views
    url(r'^suggested/$', suggested_views.suggested, name='suggested'),
	url(r'^suggested_load_more_articles/$', suggested_views.suggested_load_more_articles, name='suggested_load_more_articles'),

	#add latest read views
    url(r'^latest_read/$', latest_read_views.latest_read, name='latest_read'),
	url(r'^latest_read_load_more_articles/$', latest_read_views.latest_read_load_more_articles, name='latest_read_load_more_articles'),


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
