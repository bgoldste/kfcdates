from django.shortcuts import render, render_to_response, get_object_or_404, redirect
from django.template import RequestContext
from django.http import HttpResponse
from open_facebook import OpenFacebook
import json
from bson import ObjectId
import pymongo as pymongo
from pymongo import Connection
from datetime import datetime
import requests


"""
db = Connection(
    host=getattr(settings, "MONGODB_HOST", None),
    port=getattr(settings, "MONGODB_PORT", None)
)[settings.MONGODB_DATABASE]

if getattr(settings, "MONGODB_USERNAME", None):
    db.authenticate(getattr(settings, "MONGODB_USERNAME", None), getattr(settings, "MONGODB_PASSWORD", None))

    """


# Create your views here.
def login(request):
    context = RequestContext(request)
    try:

	    for a in request.user.social_auth.values():
	    	if a['provider'] == 'facebook':
	    		print a['uid']
	    		uid = a['uid']
	    		context['user'] = request.user.social_auth.values
			    
		        context['pic'] = uid #request.get("http://graph.facebook.com/%s/picture" % uid)

	   	
	    context['list'] = dir(request.user.social_auth)
    except AttributeError:

		pass



    return render_to_response('core/login.html', context)

def home(request):
    context = RequestContext(request)
    user = request.user
  

    #context['user'] = user.facebook_name
    #context['gender'] = user.gender

    return render_to_response('core/home.html', context)