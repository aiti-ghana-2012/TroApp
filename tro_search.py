from pygraph.classes import digraph
from pygraph.algorithms.minmax import shortest_path


from models import Route, RouteStop, Station, Stop


def pesewa_weight_function(route):
	return route.cost

def route_arriving_stop_weight_function(stop, route):
	return (stop.accumlated_distance/route.total_distance) * route.cost

def route_departing_stop_weight_function(stop, route):
	return route.cost - route_arriving_stop_weight_function(stop, route)

def get_trograph(weight_function):
	trograph = digraph.digraph()
	
	allRoutes = Route.objects.all()
	allStations = Staion.objects.all()
	
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
		
		included_routes = Route.objects.filter(route_stop__id=start.id)
		for route in included_routes:
			trograph.add_edge(
				(root, route.arrival),
				wt = route_departing_stop_weight_function(start, route),
				label = route,
			)
		

	if isinstance(end, Station):
		end_node = end.id

	elif isinstance(end, Stop):
		end_node = "stop:%i" % end.id
		trograph.add_node(end_node)
		
		included_routes = Route.objects.fileter(route_stop__id=end.id)
		for route in included_routes:
			trograph.add_edge(
				(route.departure, end_node),
				wt = route_arriving_stop_weight_function(end, route),
				label = route,			
			)

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
		routes.append(trograph.edge_label((previous,current))
		current = previous

	return routes[::-1]


def routes_to_messages(routes, start, end):
	routes = routes[:] #copy it so we don't change things

	messages = []	
	if isinstance(start, Stop):
		embark_message = "At %s, get on a TroTro heading towards %s station"
		first_route = routes.pop(0)
		embark_message = embark_messages % 
			(start.name, first_route.arrival.name)
	
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

		route_stop = RouteStop.objects.filter(
			route=routes[-1],
			stop=end,
		)[0]
		
		message = "Get off at %s, stop number %i" %
			(end.name, route_stop.order)

		messages.append(message)


	return messages
	
		
		
		
	
