# -*- coding: utf-8 -*-

from django.shortcuts import render_to_response,get_object_or_404
from trotro.models import *
import sys
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
     	  	

def get_stops(depart,arrive):
        latlng_list = []
	demo_list = []
	stop_list=[]
        route_count_list =[]
	route_count = 0
	route_count_list = [route_count]
	route_stop = Route_stop.objects.all()
	route_call = Route.objects.all()
	for i in range(0,len(route_stop)):
		if str(route_stop[i].route.departure.name) == str(depart) and str(route_stop[i].route.arrival.name) == str(arrive):
				#print 
				#demo_list.append(str(route_stop[i].route))
				#print demo_list
				stop_list.append(str(route_stop[i].stop))
			
				raw_cord = str(route_stop[i].stop.gpsLocation)
				raw_cord_split = raw_cord.split(',')
				tuple_of_cord = (float(raw_cord_split[0]),float(raw_cord_split[1]))

        			latlng_list.append(tuple_of_cord)

		elif str(route_stop[i].route.departure.name) == str(depart) and str(route_stop[i].stop.name) == str(arrive):
				
				#print route_stop[i].route
				demo_list.append(str(route_stop[i].route))
				#print demo_list
				
				stop_list = [[] for i in range(len(demo_list))]
				#print demo_list
				latlng_list = [[] for i in range(len(demo_list))]
				for j in range(len(demo_list)):
					for i in range(0,len(route_stop)): 
		
						ask= Route_stop.objects.all()
			
						if str(ask[i].route) == str(demo_list[j]):
							marker=str(ask[i].stop)
							stop_list[j].append(marker)
							raw_cord = str(ask[i].stop.gpsLocation)	                             
                                			raw_cord_split = raw_cord.split(',')
							tuple_of_cord = (float(raw_cord_split[0]),float(raw_cord_split[1]))
							latlng_list[j].append(tuple_of_cord)
				
				
				
		elif str(route_stop[i].stop.name) == str(depart) and str(route_stop[i].route.arrival.name) == str(arrive):
				#print route_stop[i].route
				demo_list.append(str(route_stop[i].route))
				#print demo_list

				stop_list = [[] for i in range(len(demo_list))]
				#print demo_list
	
				for j in range(len(demo_list)):
					for i in range(0,len(route_stop)): 
		
						ask= Route_stop.objects.all()
			
						if str(ask[i].route) == str(demo_list[j]):
							marker=str(ask[i].stop)	                             
                                			stop_list[j].append(marker)
							raw_cord = str(ask[i].stop.gpsLocation)	                             
                                			raw_cord_split = raw_cord.split(',')
							tuple_of_cord = (float(raw_cord_split[0]),float(raw_cord_split[1]))
							latlng_list[j].append(tuple_of_cord)

				
		elif str(route_stop[i].stop.name) == str(depart):
				#print route_stop[i].route
				demo_list.append(str(route_stop[i].route))
				#print demo_list
				
				stop_list = [[] for i in range(len(demo_list))]
				#print demo_list
	
				for j in range(len(demo_list)):
					for i in range(0,len(route_stop)): 
		
						ask= Route_stop.objects.all()
			
						if str(ask[i].route) == str(demo_list[j]):
							marker=str(ask[i].stop)	                             
                                			stop_list[j].append(marker)
							raw_cord = str(ask[i].stop.gpsLocation)	                             
                                			raw_cord_split = raw_cord.split(',')
							tuple_of_cord = (float(raw_cord_split[0]),float(raw_cord_split[1]))
							latlng_list[j].append(tuple_of_cord)

	
	
                                
	if len(stop_list)>8:
		return (stop_list,latlng_list,demo_list)
			

        return (stop_list,latlng_list,demo_list)





def welcome(request):
	return render_to_response('trotro/welcome.html',locals())




@csrf_exempt
def detail(request):
	
	if request.POST:
		form = RouteForm(request.POST)
		if form.is_valid():
			arrival = request.POST['arrival']			
			departure = request.POST['destination']			
			dept = form.cleaned_data.get('departure',None)
			arriv = form.cleaned_data.get('arrival',None)
			 
			
			(stop_list_post,route_count_post)=get_stops(departure,arrival) 
			return render_to_response('trotro/detail.html',{'departure':departure,'arrival':arrival,'cost':cost,'stop_list_post':stop_list_post,'route_count_post':route_count_post})
		else:
        		form = RouteForm() # An unbound form
     	return render_to_response('trotro/detail.html',locals())	

	
	


@csrf_exempt
def mapper(request):
	return render_to_response('trotro/map.html',locals())



def information_function(departure,arrival):
                        route_call = Route_stop.objects.all()
                        for route_index in range(0,len(route_call)):
                                #for station to station	
                                if str(route_call[route_index].route.departure.name) == str(departure) and str(route_call[route_index].route.arrival.name) == str(arrival):
                                        route = tro_search.path(route_call[route_index].route.departure,route_call[route_index].route.arrival)
                                        info = tro_search.routes_to_messages(route,route_call[route_index].route.departure,route_call[route_index].route.arrival )
                                        cost=route_call[route_index].route.fare

                                        depart = route_call[route_index].route.departure.name
                                        arrive = route_call[route_index].route.arrival.name

                                        stop_list,latlng_list,demo_list=get_stops(depart,arrive)

                                        return (route,info,cost,stop_list,latlng_list,demo_list)

                                                
                                #for station to stop                
                                if str(route_call[route_index].route.departure.name) == str(departure) and str(route_call[route_index].stop.name) == str(arrival):
                                        route = tro_search.path(route_call[route_index].route.departure,route_call[route_index].stop)
                                        info = tro_search.routes_to_messages(route,route_call[route_index].route.departure,route_call[route_index].stop)
                                        cost = route_call[route_index].stop_fare

                                        depart = route_call[route_index].route.departure.name
                                        arrive = route_call[route_index].stop.name

                                        stop_list,latlng_list,demo_list=get_stops(depart,arrive)

                                        return (route,info,cost,stop_list,latlng_list,demo_list)

                                #for stop to station
                                if  str(route_call[route_index].stop.name) == str(departure) and str(route_call[route_index].route.arrival.name) == str(arrival):
                                        #info matter
                                        
                                        route = tro_search.path(route_call[route_index].stop,route_call[route_index].route.arrival)
                                        info = tro_search.routes_to_messages(route,route_call[route_index].stop,route_call[route_index].route.arrival)

                                        #money matter

                                        route_cost = route_call[route_index].route.fare
                                        stop_cost = route_call[route_index].stop_fare
                                        nothing = 'No standard fare between these stops, ' 
                                        tails ='but from %s to %s is %s ,' %(route_call[route_index].route.departure.name,arrival,route_cost)
                                        inner = 'and from %s to %s is %s' %(route_call[route_index].route.departure.name,departure,stop_cost)
                                        cost = nothing + ' ' + tails + ' ' + inner

                                        depart = route_call[route_index].stop.name
                                        arrive = route_call[route_index].route.arrival.name

                                        stop_list,latlng_list,demo_list=get_stops(depart,arrive)

                                        return (route,info,cost,stop_list,latlng_list,demo_list)



                                #for stop to stop
                                for route_index_two in range(0,len(route_call)):
                                        if  str(route_call[route_index].stop.name) == str(departure) and str(route_call[route_index_two].stop.name) == str(arrival):
                                                route = tro_search.path(route_call[route_index].stop,route_call[route_index_two].stop)
                                                info = tro_search.routes_to_messages(route,route_call[route_index].stop,route_call[route_index_two].stop)

                                                route_cost = route_call[route_index].route.fare
                                                first_stop_cost = route_call[route_index].stop_fare 
                                                second_stop_cost = route_call[route_index_two].stop_fare
                                                nothing = 'No standard fare between these stops, ' 
                                                tails ='but from %s to %s is %s ,' %(route_call[route_index].route.departure.name,route_call[route_index].route.arrival.name,route_cost)
                                                inner = 'and from %s to %s is %s ,' %(route_call[route_index].route.departure.name,departure,first_stop_cost)
                                                second_inner = 'and from %s to %s is %s ,' %(route_call[route_index].route.departure.name,arrival,second_stop_cost)
                                                cost = nothing + ' ' + tails + ' ' + inner + ' ' +  second_inner

                                                depart = route_call[route_index].stop.name
                                                arrive = route_call[route_index_two].stop.name

                                                stop_list,latlng_list,demo_list=get_stops(depart,arrive)

                                        	return (route,info,cost,stop_list,latlng_list,demo_list)



                                
        

@csrf_exempt
def search_route_stop(request):
	#find_out = tro_search(request)
        if request.POST:
		form = RouteForm(request.POST)
		if form.is_valid():
			arrival = request.POST['arrival']			
			departure = request.POST['destination']
                        route,info,cost,stop_list,latlng_list,demo_list=information_function(departure,arrival)
			#one = latlng_list[0]
			#two = latlng_list[1]
			size_of_list = len(stop_list)
			size_of_info = len(info)                        
              		advice = info[(len(info)-1)]
			info = info[0:(len(info)-1)]
			
			print demo_list
                else:
        		form = RouteForm() # An unbound form
                                
	return render_to_response('trotro/answers.html',locals())




	



