import os
os.environ['DJANGO_SETTINGS_MODULE'] = 'wawa.settings'

from pygraph.classes import digraph
from pygraph.algorithms.minmax import shortest_path
from pygraph.classes.exceptions import AdditionError


from trotro.models import Route, Route_stop, Station, Stop


class PathResult(list):

    def __init__(self, *args, **kwargs):
        is_same_route = kwargs.get('is_same_route', False)
        list.__init__(self, *args)
        self.is_same_route = is_same_route

    def __getslice__(self, start, end):
        return PathResult(
            list.__getslice__(self, start, end),
            is_same_route=self.is_same_route
            )



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

        # a dictionary mapping a station id to the number of times
        # that it has been mocked
	mock_node_ids = {}
	
	for station in allStations:
		trograph.add_node(station.id)
	
	for route in allRoutes:
            try:
		trograph.add_edge(
			(route.departure.id, route.arrival.id),
			wt = weight_function(route),
			label = route,		
		)
            except AdditionError:
                # this is the case for two routes that have the same start
                # and end points, but differ in their routes

                # create a mock node for the end, which will have
                # a zero-weight edge to the actual end
                mock_node_count = mock_node_ids.get(route.arrival.id, 0)
                mock_node = "%i:mock:%d" % (route.arrival.id, mock_node_count)
                mock_node_ids[route.arrival.id] = mock_node_count + 1

                trograph.add_node(mock_node)
                trograph.add_edge(
                    (route.departure.id, mock_node),
                    wt = weight_function(route),
                    label = route,
                )

                trograph.add_edge(
                    (mock_node, route.arrival.id),
                    wt = 0,
                    label = mock_node,
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
        start_included_routes = Route.objects.filter(stops__stop=start)
        for route in start_included_routes:
            routes[route] = 1

        stop_included_routes = Route.objects.filter(stops__stop=end)
        for route in stop_included_routes:
            if route in routes:
                routes[route] += 1

        duplicated_routes = [route for route, count in routes.items() if count == 2]

        if duplicated_routes:

            out_routes = []
            for route in duplicated_routes:

                start_route_stop = route.stops.get(stop=start)
                stop_route_stop = route.stops.get(stop=end)

                distance = stop_route_stop.accumulated_distance - start_route_stop.accumulated_distance

                if distance >= 0:
                    out_routes.append(route)

            return PathResult(out_routes, is_same_route=True)
        
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
		if not ":mock:" in str(previous):
        		routes.append(trograph.edge_label((previous,current)))
		current = previous

	return PathResult(routes[::-1])


def routes_to_messages(routes, start, end):
	routes = routes[:] #copy it so we don't change things

        if routes.is_same_route:
            messages = ["You have %d options to go from %s to %s" % (
                len(routes),
                str(start),
                str(end)
                )
            ]
            
            messages.extend([str(r) for r in routes])
            


	messages = []	
	if isinstance(start, Stop):
		embark_message = "At %s, get on a TroTro heading towards %s station"
		first_route = routes.pop(0)
		embark_message = embark_message % (start.name, first_route.arrival.name)
		messages.append(embark_message)

	for route in routes:
		message = "At %s, get on a TroTro to %s station "
		message = message % (start.name, route.arrival.name)
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
		
		message = " In all the option(s), get off at %s" %(end.name)

		messages.append(message)


	return messages
	
		
		
		
	
