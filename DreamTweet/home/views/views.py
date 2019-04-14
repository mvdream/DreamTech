from django.shortcuts import render
from django.http import HttpResponseRedirect, HttpResponse
from django.urls import reverse
import urllib
import json
import pandas as pd
from django.db import connection
from sqlalchemy import create_engine
from DreamTweet.settings import USERNAME, PASSWORD, MEDIA_ROOT

def m(request):
	return render(request, "home/home.html")