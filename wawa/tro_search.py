import os
os.environ['DJANGO_SETTINGS_MODULE'] = 'wawa.settings'

from pygraph.classes import digraph
from pygraph.algorithms.minmax import shortest_path


from trotro.models import Route, Route_stop, Station, Stop



def pesewa_weight_function(route):
	  return route.fare 



def route_arriving_stop_weight_function(stop, route):
	return (stop.accumulated_distance/route.total_distance) * route.fare

def route_departing_stop_weight_function(stop, route):
	return route.fare - route_arriving_stop_weight_function(stop, route)

def get_trograph(weight_function):
	trograph = digraph.digraph()
	allRoutes = Route.objects.all()
	allStations = Station.objects.all()
	
	for station in allStations:
		trograph.add_node(station.id)
	
	for route in allRoutes:
		trograph.add_edge(
			(route.departure.id, route.arrival.id),
			wt = weight_function(route),
			label = route,		
		)

	return trograph


def path(start, end):

	WEIGHT_FUNCTION = pesewa_weight_function
	
	trograph = get_trograph(WEIGHT_FUNCTION)

	if isinstance(start, Station):
		root = start.id		

	elif isinstance(start, Stop):
		root = "stop:%i" % start.id
		trograph.add_node(root)
		
		start_included_routes = Route.objects.filter(stops__id=start.id)
		for route in start_included_routes:
			trograph.add_edge(
				(root, route.arrival.id),
				wt = route_departing_stop_weight_function(start, route),
				label = route,
			)
		

	if isinstance(end, Station):
		end_node = end.id

	elif isinstance(end, Stop):
		end_node = "stop:%i" % end.id
		trograph.add_node(end_node)
		
		stop_included_routes = Route.objects.filter(stops__id=end.id)
		for route in stop_included_routes:
			trograph.add_edge(
				(route.departure.id, end_node),
				wt = route_arriving_stop_weight_function(end, route),
				label = route,			
			)

        #checking for same route start and stop
        routes = {}
        start_included_routes = Route.objects.filter(stops__id=start.id)
        for route in start_included_routes:
            routes[route] = 1

        stop_included_routes = Route.objects.filter(stops__id=end.id)
        for route in stop_included_routes:
            if route in routes:
                routes[route] += 1

        duplicated_routes = [route for route, count in routes.items() if count == 2]

        if duplicated_routes:
            if len(duplicated_routes) == 1:
                return duplicated_routes
            
            smallest_distance = None
            best_route = None

            for route in duplicated_routes:

                start_route_stop = route.stops.get(stop=start)
                stop_route_stop = route.stops.get(stop=end)

                distance = stop_route_stop - start_route_stop

                if distance < 0:
                    continue

                if smallest_distance is None or distance < smallest_distance:
                    smallest_distance = distance
                    best_route = route

            if best_route is None:
                raise ValueError("No positive distance route from %s to %s... weird." % str(start), str(end))
            else:
                return [best_route]
        
	#ok i have now fully transformed the graph

	#djisktra!
	spanning_tree, shortest_distance = shortest_path(trograph, root)

	#lets make sure that we found it
	if end_node not in spanning_tree:
		raise ValueError("Unable to find a path from %s to %s" % 
			(str(start), str(end)))
	
	routes = []
	
	current = end_node
	

	while spanning_tree[current] is not None:
		previous = spanning_tree[current]
		routes.append(trograph.edge_label((previous,current)))
		current = previous

	return routes[::-1]


def routes_to_messages(routes, start, end):
	routes = routes[:] #copy it so we don't change things

	messages = []	
	if isinstance(start, Stop):
		embark_message = "At %s, get on a TroTro heading towards %s station"
		first_route = routes.pop(0)
		embark_message = embark_message % (start.name, first_route.arrival.name)
		messages.append(embark_message)

	for route in routes:
		message = "At %s station, get on a TroTro to %s station"
		message = message % (route.departure.name, route.arrival.name)
		messages.append(message)
		
	if isinstance(end, Stop):
		
		if routes:
			the_route = routes[-1]
		else:
			the_route = first_route

		route_stop = Route_stop.objects.filter(
			route=the_route,
			stop=end,
		)[0]
		
		message = "Get off at %s, stop number %i" %(end.name, route_stop.order)

		messages.append(message)


	return messages
	
		
		
		
	
