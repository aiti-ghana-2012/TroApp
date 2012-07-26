from django.shortcuts import render_to_response,get_object_or_404
from trotro.models import *
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponseRedirect, HttpResponse
from django.core.urlresolvers import reverse
from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib import auth
from django.contrib.auth import authenticate, login


def welcome(request):
	return render_to_response('trotro/welcome.html',locals())

@csrf_exempt
def detail(request):
	return render_to_response('trotro/detail.html',locals())
	
@csrf_exempt
def mapper(request):
	return render_to_response('trotro/map.html',locals())





	

        
	
