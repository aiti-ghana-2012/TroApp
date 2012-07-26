import math
import os
os.environ['DJANGO_SETTINGS_MODULE'] = 'wawa.settings'

from trotro.models import Station, Stop, Route, Route_stop    



def gps_coords(gps_string):
        coords = gps_string.split(',')
        first_setter = [float(i.strip()) for i in coords]
	x1= first_setter[0]
	y1= first_setter[1]
	return (x1, y1)

def gps_distance(coords1, coords2):
        x1, y1 = coords1
        x2, y2 = coords2
        return abs(math.hypot((x2-x1),(y2-y1)))

def nodal_distance_Cal(first, last):
	first_coords = gps_coords(first.gpsLocation)
        last_coords = gps_coords(last.gpsLocation)        
	return gps_distance(first_coords, last_coords)



def main():
        # for every route,
        # get its route stops
        # iterate through the route stops, keeping track of accumulated distance
        # then save the total accumulated distance as the total distance of the route route


        allRoutes = Route.objects.all()

        for route in allRoutes:
                print "Computing distances for route: %s" % str(route)
                route_stops = list(route.stops.all())  #assigns a stop to route_stops

                if not route_stops:   
                        distance = nodal_distance_Cal(
                                route.departure,
                                route.arrival,
                        )
                        print "No stops!"
                else:
                        distance = nodal_distance_Cal(
                                route.departure,
                                route_stops[0].stop
                        )
                        print "distance from station %s to stop %s is %f" % (
                                str(route.departure),
                                str(route_stops[0].stop),
                                distance,
                        )

                for i in range(0, len(route_stops)):
                        print "accumulated distance is %f" % distance
                        
                        current_route_stop = route_stops[i]
                        current_route_stop.accumulated_distance = distance #assigns distance to accumD
                        current_route_stop.save()

                        current_stop = current_route_stop.stop
                        
                        try:
                                next_stop = route_stops[i+1].stop
                        except IndexError:
                                next_stop = route.arrival

                        new_distance = nodal_distance_Cal(
                                current_stop,
                                next_stop,
                        )

                        print "distance from %s to %s is %f" % (
                                str(current_stop),
                                str(next_stop),
                                new_distance,
                        )

                        distance += new_distance

                print "Total route distance approximation is %f" % distance
                route.total_distance = distance
                route.save()
                print "-"*50


if __name__ == "__main__":
        main()



