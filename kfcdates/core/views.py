from django.shortcuts import render, render_to_response, get_object_or_404, redirect
from django.template import RequestContext
from django.http import HttpResponse
from open_facebook import OpenFacebook
import json


# Create your views here.
def login(request):
    context = RequestContext(request)
    print request.user
    return render_to_response('core/login.html', context)

def home(request):
    context = RequestContext(request)
    user = request.user
  

    #context['user'] = user.facebook_name
    #context['gender'] = user.gender

    return render_to_response('core/home.html', context)