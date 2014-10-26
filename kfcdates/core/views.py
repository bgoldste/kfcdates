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


def get_user_gender(first_name):
    url = "http://api.genderize.io?name=%s" % first_name
    r = requests.get(url)
    return r.json()['gender']


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
                            "pic": get_user_pic(a['uid']),
                            "gender": get_user_gender(request.user.first_name)
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

    return render_to_response('core/home.html', context)

def get_dates(request):
    context = RequestContext(request)

    kfc_dates = []

    try:
        for a in request.user.social_auth.values():
            if a['provider'] == 'facebook':
                kfc_dates_iterator = db.dates.find({"buyer" : a['uid']})
                for kfc_date in kfc_dates_iterator:
                    kfc_dates.append(kfc_date)

    except AttributeError:
        pass

    data = json.dumps(kfc_dates)

    return HttpResponse(data, mimetype='application/json')


def get_random_dates(request):
    context = RequestContext(request)

    kfc_dates = []

    kfc_dates_iterator = db.dates.find({})
    for kfc_date in kfc_dates_iterator:
        kfc_dates.append(kfc_date)

    data = json.dumps(kfc_dates)

    return HttpResponse(data, mimetype='application/json')


def create_date(request):
    context = RequestContext(request)

    kfc_date = None

    try:
        for a in request.user.social_auth.values():
            if a['provider'] == 'facebook':
                time = request.GET.get('time', '')
                location = request.GET.get('location', '')

                new_date = {
                                "buyer": a['uid'],
                                "time": time,
                                "location": location
                            }
                date_id = db.dates.insert(new_date)
                kfc_date = db.dates.find_one({"_id" : date_id})


    except AttributeError:
        pass

    data = json.dumps(kfc_date)

    return HttpResponse(data, mimetype='application/json')

def join_date(request):
    context = RequestContext(request)

    kfc_date = None

    try:
        for a in request.user.social_auth.values():
            if a['provider'] == 'facebook':
                date_id = request.GET.get('date_id', '')
                kfc_date = db.dates.find_one({"_id" : date_id})

                kfc_date['recipient'] = a['uid']
                db.dates.save(kfc_date)


    except AttributeError:
        pass

    data = json.dumps(kfc_date)

    return HttpResponse(data, mimetype='application/json')