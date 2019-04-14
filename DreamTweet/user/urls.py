from django.conf.urls import url
from .views import user_views

app_name = 'user'

urlpatterns = [
    # /dashboard/
    url(r'^topic', user_views.get_user, name="topic"),
	url(r'^tweets', user_views.get_tweets, name="tweets"),
]