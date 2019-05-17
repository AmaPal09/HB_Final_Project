# For all transportation agencies use below API: 
# curl http://webservices.nextbus.com/service/publicJSONFeed?command=agencyList > seed_data/agencies.json

import json
import requests
from datetime import datetime
from sqlalchemy import and_, or_, not_

from model import Agency, Route, Stop, Bus, Bus_Route_Stop
from model import connect_to_db, db 

from server import app

from pprint import pprint


print("Start of seed file")


def load_agency(): 
    """ Load all agencies available from the next bus API """

    print("Agencies")

    # Read agencies from the API JSON file
    agencies_info = open("seed_data/agencies.json").read()
    agencies_json = json.loads(agencies_info)

    # Extract and load details for each of the agencies
    for i in range(len(agencies_json['agency'])): 
        # check if record present for the agency in agencies table. 
        dup_agency = Agency.query.filter(
            and_(
                Agency.agency_tag == agencies_json['agency'][i]['tag'], 
                Agency.agency_title == agencies_json['agency'][i]['title']
                )
            ).first()

        if dup_agency: 
            # if agency is present in table, go to next agency
            continue
        else: 
            # Add the agency to the table as it is not alreaty present
            new_agency = Agency(
                agency_tag=agencies_json['agency'][i]['tag'], 
                agency_short_title=agencies_json['agency'][i].get('shortTitle',None),
                agency_title=agencies_json['agency'][i]['title'],
                region=agencies_json['agency'][i]['regionTitle']
                ) 
            db.session.add(new_agency)

    # Commit all the newly added agencies to the DB
    db.session.commit()

    print("Agencies loaded")


def load_route(): 
    """ Load all route for SF-Muni """ 

    print("Routes")

    # currently only for SF so set agency id to SF (49). 
    agency_id = 49 
    route_info = open("seed_data/sfmuni_routes.json").read()
    route_json = json.loads(route_info)

    for i in range(len(route_json['route'])): 
        # check if route is already present
        dup_route = Route.query.filter(
            and_(
                Route.agency_id==agency_id, 
                Route.route_tag==route_json['route'][i]['tag'], 
                Route.route_title==route_json['route'][i]['title']
                )
            ).first() 

        if dup_route: 
            # if route is present in table, go to next route
            continue
        else: 
            # Add the route to the table as it is not alreaty present
            new_route = Route(
                agency_id=agency_id,
                route_tag=route_json['route'][i]['tag'],
                route_title=route_json['route'][i]['title']
                )
            db.session.add(new_route)

    db.session.commit()

    print("Routes loaded")


def get_route_json(route): 
    """ Return the JSON for route details from API
    INPUT: Route instance
    OUTPUT: JSON of API
    
    Called from: load_bus() 
    """ 

    # create parameter dict for the API request
    payload = {"command":"routeConfig", 
    "a":route.route_agency.agency_tag,
    "r":route.route_tag
    }

    req = requests.get("http://webservices.nextbus.com/service/publicJSONFeed?", 
                        params = payload)

    # convert API string into json
    return req.json()


def check_bus_dup_load(bus_route, route): 
    """ Load bus instance if duplicate not present
    INPUT: bus_route dict from API, Route instance
    OUTPUT: None 

    Called from: load_bus() 
    """
    
    #Check if bus route is already present in the table    
    dup_bus = Bus.query.filter(
                    and_(
                        Bus.bus_tag == bus_route["tag"], 
                        Bus.bus_direction == bus_route["name"]
                        )
                    ).first()

    if dup_bus: 
        # bus is already present, don't load it 
        return
    else: 
        # bus route is not present, so load it. 
        new_bus = Bus(bus_title = bus_route["title"],
            bus_tag = bus_route["tag"] ,
            route_id = route.route_id , 
            bus_direction =  bus_route["name"]
            )

        db.session.add(new_bus)
        db.session.commit()        
        return


def load_stop(stops_on_route): 
    """ Load stops from input list into stops table. 

    I/P: List of stops
    O/P: None
    Called from: load_bus()

    Loop over all the stops provided in the input stop list and load the stops
    to the stops table. 

    """

    #print("load_stops")
    # loop through all the stops in the route
    for stop in stops_on_route: 
        print("Load stop to DB")
        # check if stop is already present in the table. 

        dup_stop = Stop.query.filter(
            and_(
                Stop.stop_tag==int(stop['tag']), 
                Stop.stop_id_tag==int(stop['stopId']), 
                Stop.stop_title==stop['title'] 
                ) 
            ).first()

        # if stop already present, dont load it
        if dup_stop: 
            print("Stop {} already present".format(dup_stop))
            pass
        else: 
            # stop not present, so load it
            print("Load new stop {}".format(dup_stop))
            new_stop = Stop(
                stop_tag = int(stop['tag']),  
                stop_id_tag = int(stop['stopId']),
                stop_title = stop['title'], 
                stop_lon = float(stop['lon']), 
                stop_lat = float(stop['lat'])
                )

        db.session.add(new_stop)

    db.session.commit()

    # print("all stops loaded")


def load_bus_route_stop(bus_route, route): 
    """ Load the sequence of stops on a bus route for seleted bus. 

    I/P1: Dict with bus route direction details 
    I/P2: Instance of Route 

    O/P: None 

    Get the bus_id and route_id for the provided bus route, and
    for all the stops provided, load the stop_ids for them in the provided 
    sequence. 
    """

    route_stop_list = bus_route["stop"]

    bus_id = Bus.query.with_entities(
        Bus.bus_id
        ).filter(
        Bus.bus_tag==bus_route["tag"], 
        Bus.route_id==route.route_id, 
        Bus.bus_direction==bus_route["name"]
        ).one()

    for i, stop in enumerate(route_stop_list): 
        stop_id = Stop.query.with_entities(
            Stop.stop_id
            ).filter(
            Stop.stop_tag==int(stop["tag"])
            ).one()

        #Check if stop on the bus route is already present in the table
        dup_bus_route_stop = Bus_Route_Stop.query.filter(
            and_(
                Bus_Route_Stop.bus_id==bus_id, 
                Bus_Route_Stop.stop_id==stop_id)
            ).first()
                
        if dup_bus_route_stop: 
            # bus_route_stop is already present, don't load it 
            continue
        else: 
            # bus_route_stop is not present, so load it 
            new_bus_route_stop = Bus_Route_Stop(
                bus_id = bus_id,
                stop_id = stop_id, 
                stop_seq = i)
            db.session.add(new_bus_route_stop)
    db.session.commit()
    print("Loaded bus route stops for a direction")


def load_bus(): 
    """ Load all the bus routes, stops and directions for a selected agency """
    print("Load all bus routes")

    # load all routes from route table
    routes = Route.query.options(db.joinedload("route_agency")).all()

    # get bus route details for all routes
    for route in routes: 
        print("Start looping through the routes")

        #get data from the API               
        route_json = get_route_json(route)

        # get list of all the stops on this route
        stops_on_route = route_json["route"]["stop"]
        load_stop(stops_on_route)

        #start of getting route details 
        if isinstance(route_json["route"]["direction"], list): 
            bus_route_list = route_json["route"]["direction"]
            for bus_route in bus_route_list: 
                check_bus_dup_load(bus_route, route)
                load_bus_route_stop(bus_route, route)
        else: 
            bus_route_dict = route_json["route"]["direction"]
            check_bus_dup_load(bus_route_dict, route)
            load_bus_route_stop(bus_route_dict, route)

    print("All bus routes loaded")



if __name__ == "__main__": 
    connect_to_db(app)

    #In case tables haven't been created, create them
    db.create_all()

    #Import data from JSON files for static tables. 
    # load_region()
    # load_agency()
    # load_route()
    # load_bus_route()
    