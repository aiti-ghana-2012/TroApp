import math
import os
os.environ['DJANGO_SETTINGS_MODULE'] = 'wawa.settings'

from trotro.models import Station

def distanceCal():
		
	stationVal = Station.objects.all()
	stopVal = Stop.obj
	first = stationVal[0]
	first_id = stationVal[0].id
	location_of_first = stationVal[0].gpsLocation.split(',')
	first_setter = [float(i.strip()) for i in location_of_first]
	x1= first_setter[0]
	y1= first_setter[1]

	first = stationVal[1]
	first_id = stationVal[1].id
	location_of_first = stationVal[1].gpsLocation.split(',')
	first_setter = [float(i.strip()) for i in location_of_first]
	x2= first_setter[0]
	y2= first_setter[1]

	node_distance = math.hypot((x2-x1),(y2-y1))
	print node_distance

	return node_distance
	
distanceCal()
