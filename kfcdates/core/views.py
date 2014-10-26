from django.shortcuts import render, render_to_response, get_object_or_404, redirect
from django.template import RequestContext
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
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
                        gender = get_user_gender(request.user.first_name)
                        is_buyer = False,
                        is_recipient = True
                        if gender == 'male':
                            is_buyer = True
                            is_recipient = False

                        new_mongo_user = {
                            "id": request.user.id,
                            "photoURL": get_user_pic(a['uid']),
                            "username": request.user.first_name + " " + request.user.last_name[0] + ".",
                            "firstname": request.user.first_name,
                            "lastname": request.user.last_name,
                            "facebookID": a['uid'],
                            "locationLatitude": 0,
                            "locationLongitude": 0,
                            "isBuyer": is_buyer,
                            "isRecipient": is_recipient,
                            "email": request.user.email
                        }
                        db.users.insert(new_mongo_user)

                        mongo_user = db.users.find_one({"uid": a['uid']})

                    
                    uid = a['uid']
                    context['user'] = request.user.social_auth.values
                    
                    context['pic'] = uid #request.get("http://graph.facebook.com/%s/picture" % uid)
                    return render_to_response('core/index.html', context)
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

def index(request):
    context = RequestContext(request)
    return render_to_response('core/index.html', context)


def test_users(request):

    params = request.GET.get('id', None)
    #print "PARAMS + " , params  
    #print "UserID", request.user.id

    if (params == None):
        try: 
            params = request.path.split("/")[2]
        except:
            pass
    print params       
    
    if (params != None):
        try:
            o = db.users.find_one({"id": int(params) });
            if o:
                o['_id'] = str(o['_id'])
                c = {'users': [o]}
            else:
                o = db.users.find_one({"facebookID": str(params) });
                if o:
                    o['_id'] = str(o['_id'])
                    o['id'] = str(o['facebookID'])
                    c = {'users': o}
        except ValueError:
            try:
                o = db.users.find_one({"id": int(request.user.id) });
                o['_id'] = str(o['_id'])
                c = {'users': [o]}
            except TypeError:
                return redirect('login')
    else:
        o = { 'id': '1', 'photoURL': "http://x.com/x.jpg", 'username': 'dioptre', 'firstname': 'Andy', 'lastname': 'G', 'facebookID': 'mrdioptre', 'locationLatitude': '61.4', 'locationLongitude': '120.2', 'isBuyer': 'true', 'isRecipient': 'false', 'email': 'dioptre@gmail.com', 'meetups': [] },
        c = {'users' : o}


    data = json.dumps(c)

    return HttpResponse(data, mimetype='application/json')


def proposals(request):
    context = RequestContext(request)

    kfc_dates = []

    try:
        for a in request.user.social_auth.values():
            if a['provider'] == 'facebook':
                kfc_dates_iterator = db.dates.find({"recipient" : None})
                for kfc_date in kfc_dates_iterator:
                    kfc_date['_id'] = str(kfc_date['_id'])
                    kfc_date['id'] = kfc_date['_id']
                    kfc_date['recipient'] = []
                    kfc_date['buyer'] = [kfc_date['buyer']]
                    kfc_dates.append(kfc_date)

    except AttributeError:
        pass

    data = json.dumps({'proposals' : kfc_dates})

    return HttpResponse(data, mimetype='application/json')

@csrf_exempt
def slots(request):
    if request.method == "POST":
        context = RequestContext(request)
        kfc_date = None
        #print request.body
        try:
            for a in request.user.social_auth.values():
                if a['provider'] == 'facebook':
                    data = json.loads(request.body)['slot']
                    location_longitude = data['locationLongitude']
                    location_latitude = data['locationLatitude']
                    address = data['address']
                    date = data['date']
                    time = data['time']
                    new_date = {
                                    "locationLatitude": location_latitude,
                                    "locationLongitude": location_longitude,
                                    "address": address,
                                    "buyer": a['uid'],
                                    "date": date,
                                    "time": time,
                                    "state": "new",
                                    #"recipient": [],
                                }
                    date_id = db.dates.insert(new_date)
                    #kfc_date = db.dates.find_one({"_id" : date_id})
                    #data = json.dumps(kfc_date)
                    #return HttpResponse(data, mimetype='application/json')
                    return HttpResponse(status=201);
        except AttributeError:
            pass
    return HttpResponse(status=200);
    





