from django.shortcuts import render_to_response,get_object_or_404
from trotro.models import *
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponseRedirect, HttpResponse
from django.core.urlresolvers import reverse
from django import forms
from django.forms import ModelForm
from django.contrib.auth.forms import UserCreationForm
from django.contrib import auth
from django.contrib.auth import authenticate, login

import tro_search

route_call_fare=0

class RouteForm(forms.Form):
    	class Meta:
		model = Route
     	  	#exclude=['post']

def get_route_value(depart,arrive):
	global route_call_fare
	route_call = Route.objects.all()
	station_call = Station.objects.all()
	#route_call_id = Route.objects.get(pk=)
	#print depart,route_call[0].departure.name
	#print arrive,route_call[0].arrival.name
	for route_index in range(0,len(route_call)):
		if str(route_call[route_index].departure.name) == str(depart) and str(route_call[route_index].arrival.name) == str(arrive):
			route_call_fare=route_call[route_index].fare 
			#print 'farjek'		
			#print route_call_fare
			return route_call_fare
stop_list=[]
def get_stops(depart,arrive):
	global stop_list
	route_stop = Route_stop.objects.all()
	route_call = Route.objects.all()
	for route_index in range(0,len(route_call)):
		if str(route_call[route_index].departure.name) == str(depart) and str(route_call[route_index].arrival.name) == str(arrive) and route_call[route_index].order<99:
			for i in range(0,len(route_stop)):
				stop_list.append(str(route_stop[i].stop.name))
			stop_list
			return stop_list



def welcome(request):
	return render_to_response('trotro/welcome.html',locals())

@csrf_exempt
def detail(request):
	
	if request.POST:
		#print request.POST
		form = RouteForm(request.POST)
		if form.is_valid():
			arrival = request.POST['arrival']			
			departure = request.POST['destination']			
			dept = form.cleaned_data.get('departure',None)
			arriv = form.cleaned_data.get('arrival',None)
			#print arriv
			cost = get_route_value(departure,arrival)  
			
			stop_list_post=get_stops(departure,arrival) 
			

			return render_to_response('trotro/detail.html',{'departure':departure,'arrival':arrival,'cost':cost,'stop_list_post':stop_list_post})
		else:
        		form = RouteForm() # An unbound form
     	return render_to_response('trotro/detail.html',locals())	

	
	
@csrf_exempt
def mapper(request):
	return render_to_response('trotro/map.html',locals())


@csrf_exempt
def search_route_stop(request):
	find_out = tro_search(request)
	return render_to_response('trotro/answers.html',locals())




	



'''
if request.method == 'POST': 
		form = WelcomeForm(request.POST)
		if form.is_valid():
			departure = form.cleaned_data['departure']
			arrival = form.cleaned_data['arrival']
			print 'well'
			return render_to_response('trotro/detail.html',{'form':form,'departure':departure,'arrival':arrival})
		else:
			form = WelcomeForm() # unbounded

'''        
	
