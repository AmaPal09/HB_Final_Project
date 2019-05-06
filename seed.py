# For all transportation agencies use below API: 
# curl http://webservices.nextbus.com/service/publicJSONFeed?command=agencyList > seed_data/agencies.json

import json
import requests
from datetime import datetime
from sqlalchemy import and_, or_, not_

from model import Region, Agency, Direction, Route, Stop, Bus_Route, Bus_Route_Stop
from model import connect_to_db, db 

from server import app

from pprint import pprint

print("Start of seed file")

def load_region(): 
    """ Load all regions available from the next bus API """

    print("Regions")

    # Agency.query.delete()
    # Region.query.delete()
    
    agencies_json = open("seed_data/agencies.json").read()
    agencies_info = json.loads(agencies_json)

    for i in range(len(agencies_info['agency'])): 
        # look for region record in regions table
        dup_region = Region.query.filter(Region.region == agencies_info['agency'][i]['regionTitle']).first()
        
        if dup_region: 
            # if region is present in table, go to next region
            continue
        else: 
            # Add the region to the table as it is not alreaty present
            region = Region(region=agencies_info['agency'][i]['regionTitle'])
            db.session.add(region)

    # Commit all the newly added users to the regions table 
    db.session.commit()

    print("Regions loaded")


def load_agency(): 
    """ Load all regions available from the next bus API """

    print("Agencies")

    # Delete all rows in table to avoid duplicate data over multiple runs.  
    # Route file refers to region_id as a foreign key, so delete data from that as well. 
    Route.query.delete()
    Agency.query.delete()
    
    # Read agencies from the API JSON file
    agencies_json = open("seed_data/agencies.json").read()
    agencies_info = json.loads(agencies_json)

    # Extract and load details for each of the agencies
    for i in range(len(agencies_info['agency'])): 
        # extract agency attributes
        tag = agencies_info['agency'][i]['tag']
        title = agencies_info['agency'][i]['title']
        region_title = agencies_info['agency'][i]['regionTitle']
        short_title = agencies_info['agency'][i].get('shortTitle',None)
        
        # get region id for provided region
        region = Region.query.filter(Region.region == region_title ).first()
        # print(region.region_id, region.region)
        
        # create agency instance
        agency = Agency(agency_tag=tag, 
            agency_short_title=short_title,
            agency_title=title,
            region_id=region.region_id)
        
        # Add the instance to the session or it wont be stored in the DB
        db.session.add(agency)

    # Commit all the newly added users to the DB 
    db.session.commit()

    print("Agencies loaded")


def load_route(): 
    """ Load all route for SF-Muni """ 

    print("Routes")

    Route.query.delete()
    Bus_Route.query.delete()


    route_json = open("seed_data/sfmuni_routes.json").read()
    route_info = json.loads(route_json)

    for i in range(len(route_info['route'])): 
        tag = route_info['route'][i]['tag']
        title = route_info['route'][i]['title']
        agency_id = 49 

        route = Route(agency_id=agency_id,
            route_tag=tag,
            route_title=title)

        db.session.add(route)

    db.session.commit()

    print("Routes loaded")



def load_bus_route(): 
    """ Load all the bus routes, stops and directions for a selected agency """
    print("Start load bus route")

    # load all routes from route table
    routes = Route.query.all()


    print("Load all stops, bus routes and directions")

    # get stops and bus route details for all routes
    print("Total routes presnet {}".format(len(routes)))
    for route in routes: 
        print("Start looping through the routes")

        # get the agency details for this route
        agency_tag = Agency.query.with_entities(Agency.agency_tag).filter(Agency.agency_id==route.agency_id).one()

        # create parameter dict for the API request
        payload = {"command":"routeConfig", 
        "a":agency_tag,
        "r":route.route_tag
        }

        # Get bus route details from the API
        req = requests.get("http://webservices.nextbus.com/service/publicJSONFeed?", params = payload)
        
        # conver API string into json
        route_json = req.json()
        
        # get list of all the stops on this route
        stops_on_route = route_json['route']['stop']
        print("got list of all stops on the route")


        print("title of this route is: {}".format(route_json['route']['direction'][0]['title']))
        print("start looping through the list of bus stops:- {}".format(len(stops_on_route)))
        # loop through all the stops in the route
        for stop in stops_on_route: 
            # get stop tag
            # check if stop is already present in the table. 
            stop_id = Stop.query.with_entities(Stop.stop_id).filter(and_(Stop.stop_tag == int(stop['tag']), Stop.stop_id_tag ==int(stop['stopId']), Stop.stop_title == stop['title'] )).first()

            # if stop already present, dont load it
            if stop_id: 
                print("Stop {} already present".format(stop_id))
                pass
            else: 
                # stop not present, so load it
                print("Load new stop {}".format(stop))
                new_stop = Stop(stop_tag = int(stop['tag']),  
                    stop_id_tag = int(stop['stopId']),
                    stop_title = stop['title'], 
                    stop_lon = float(stop['lon']), 
                    stop_lat = float(stop['lat']))

                db.session.add(new_stop)

        db.session.commit()

        print("all stops loaded")

        route_directions_list = route_json['route']['direction']
        print("get route direction details")

        for route_direction in route_directions_list: 
            pprint(route_direction)

            name = route_direction['name']
            print("This is a {} route".format(name))

            #Check if direction is already present in the loop 
            direction_id = Direction.query.with_entities(Direction.direction_id).filter(Direction.direction == name).first()

            # if direction is not present then load it. 
            if direction_id: 
                print("Direction already present in the table")
                pass 
            else: 
                # Stop not present, so load it
                print("Direction not present. Add direction: {}".format(name))
                new_dir = Direction(direction = name)
                db.session.add(new_dir)
                db.session.commit()

            direction_id = Direction.query.with_entities(Direction.direction_id).filter(Direction.direction == name).one()
            print('The direction id is: {}'.format(direction_id))

            bus_route_id = Bus_Route.query.with_entities(Bus_Route.bus_route_id).filter(and_(Bus_Route.tag == route_direction['tag'], Bus_Route.route_id == route.route_id, Bus_Route.direction_id == direction_id)).first()

            if bus_route_id: 
                print("Bus route already present in the table")
                pass
            else: 
                new_bus_route = Bus_Route(title = route_direction['title'],
                    tag = route_direction['tag'] , 
                    route_id = route.route_id , 
                    direction_id = direction_id 
                    )

                db.session.add(new_bus_route)
                db.session.commit()
                print("Loaded bus route {}".format(new_bus_route))

            

            stop_list = route_direction['stop']
            tag = route_direction['tag']

            bus_route_id = Bus_Route.query.with_entities(Bus_Route.bus_route_id).filter(Bus_Route.tag == tag, Bus_Route.route_id == route.route_id, Bus_Route.direction_id == direction_id ).one()

            print("Bus route id is: {} for the bus tag: {}".format(bus_route_id, tag))

            for i, stop in enumerate(stop_list): 
                print(i)
                print(type(i))
                print("Stop seq number is {}".format(i))
                print(type(stop['tag']))
                print(stop['tag'])
                
                stop_id = Stop.query.with_entities(Stop.stop_id).filter(Stop.stop_tag == int(stop['tag']))
                print("Stop id is {}".format(stop_id))
                


                new_bus_route_stop = Bus_Route_Stop(bus_route_id = bus_route_id,
                    stop_id = stop_id, 
                    stop_seq = i)
                db.session.add(new_bus_route_stop)
            db.session.commit()
            print("Loaded bus route stops for a direction")

        break


       







if __name__ == "__main__": 
    connect_to_db(app)

    #In case tables haven't been created, create them
    db.create_all()

    #Import data from JSON files for static tables. 
    # load_region()
    # load_agency()
    # load_route()
