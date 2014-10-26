from django.shortcuts import render, render_to_response, get_object_or_404, redirect
from django.template import RequestContext
from django.http import HttpResponse
from open_facebook import OpenFacebook
import json
from django.conf import settings
from bson import ObjectId
import pymongo as pymongo
from pymongo import Connection
from datetime import datetime
import requests

from django.contrib.auth import logout as auth_logout

db = Connection(
    host=getattr(settings, "MONGODB_HOST", None),
    port=getattr(settings, "MONGODB_PORT", None)
)[settings.MONGODB_DATABASE]

if getattr(settings, "MONGODB_USERNAME", None):
    db.authenticate(getattr(settings, "MONGODB_USERNAME", None), getattr(settings, "MONGODB_PASSWORD", None))


def get_user_pic(uid):

	url = "http://graph.facebook.com/%s/picture?type=large" % uid
	pic = requests.get(url)
	return pic.url


# Create your views here.
def login(request):
    context = RequestContext(request)
    try:
	    for a in request.user.social_auth.values():
	    	if a['provider'] == 'facebook':
                
                    mongo_user = db.users.find_one({"uid": a['uid'] })
                    if not mongo_user:
                        new_mongo_user = {
                            "uid": a['uid'],
                            "name": request.user.first_name + " " + request.user.last_name[0] + ".",
                            "pic": get_user_pic(a['uid'])
                        }
                        db.users.insert(new_mongo_user)

                        mongo_user = db.users.find_one({"uid": a['uid']})

                    
                    uid = a['uid']
                    context['user'] = request.user.social_auth.values
    			    
                    context['pic'] = uid #request.get("http://graph.facebook.com/%s/picture" % uid)

                    return redirect('home')
	   	
                
    except AttributeError:
		pass

    return render_to_response('core/login.html', context)

def logout(request):
    auth_logout(request)
    return redirect('login')

def home(request):
    context = RequestContext(request)
    user = request.user

    print request.user.first_name
  

    #context['user'] = user.facebook_name
    #context['gender'] = user.gender

    return render_to_response('core/home.html', context)