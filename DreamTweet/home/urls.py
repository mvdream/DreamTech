from django.conf.urls import url
from .views import views

app_name = 'home'

urlpatterns = [
    # /dashboard/
    url(r'', views.m, name="home"),

]