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

    # Read agencies from the API JSON file
    agencies_json = open("seed_data/agencies.json").read()
    agencies_info = json.loads(agencies_json)

    # Extract and load details for each of the agencies
    for i in range(len(agencies_info['agency'])): 
        # get region id for provided region
        region_id = Region.query.with_entities(Region.region_id).filter(Region.region == agencies_info['agency'][i]['regionTitle'] ).first()
        
        # check if record present for the agency in agencies table. 
        dup_agency = Agency.query.filter(and_(Agency.agency_tag == agencies_info['agency'][i]['tag'], Agency.agency_title == agencies_info['agency'][i]['title'])).first()

        if dup_agency: 
            # if agency is present in table, go to next agency
            continue
        else: 
            # Add the agency to the table as it is not alreaty present
            new_agency = Agency(agency_tag=agencies_info['agency'][i]['tag'], 
                agency_short_title=agencies_info['agency'][i].get('shortTitle',None),
                agency_title=agencies_info['agency'][i]['title'],
                region_id=region_id) 
            db.session.add(new_agency)

    # Commit all the newly added agencies to the DB
    db.session.commit()

    print("Agencies loaded")


def load_route(): 
    """ Load all route for SF-Muni """ 

    print("Routes")

    # Route.query.delete()
    # Bus_Route.query.delete()

    route_json = open("seed_data/sfmuni_routes.json").read()
    route_info = json.loads(route_json)

    for i in range(len(route_info['route'])): 
        agency_id = 49 

        # check if route is already present
        dup_route = Route.query.filter(and_(Route.agency_id== agency_id, Route.route_tag == route_info['route'][i]['tag'], Route.route_title == route_info['route'][i]['title'])).first() 

        if dup_route: 
            # if route is present in table, go to next route
            continue
        else: 
            # Add the route to the table as it is not alreaty present
            new_route = Route(agency_id=agency_id,
                route_tag=route_info['route'][i]['tag'],
                route_title=route_info['route'][i]['title'])
            db.session.add(new_route)

    db.session.commit()

    print("Routes loaded")


def load_bus_route(): 
    """ Load all the bus routes, stops and directions for a selected agency """
    print("Load all stops, bus routes and directions for a route")

    # load all routes from route table
    routes = Route.query.all()

    # get stops and bus route details for all routes
    print("Total routes presnet {}".format(len(routes)))
    for route in routes: 
        print("Start looping through the routes")

        ####### start of accessing the API #######
        # get the agency details for this route
        agency_tag = Agency.query.with_entities(Agency.agency_tag).filter(Agency.agency_id==route.agency_id).one()

        # create parameter dict for the API request
        payload = {"command":"routeConfig", 
        "a":agency_tag,
        "r":route.route_tag
        }

        # Get bus route details from the API
        req = requests.get("http://webservices.nextbus.com/service/publicJSONFeed?", params = payload)
        
        # convert API string into json
        route_json = req.json()

        ####### end of accessing  API #######
        
        ####### start of getting data from the API #######

        ####### start of getting stop details #######
        # get list of all the stops on this route
        stops_on_route = route_json['route']['stop']
        # print("got list of all stops on the route")

        print("title of this route is: {}".format(route_json['route']['direction'][0]['title']))
        print("start looping through the list of bus stops:- {}".format(len(stops_on_route)))
        # loop through all the stops in the route
        for stop in stops_on_route: 
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

        ####### end of getting stop details #######


        ####### start of getting route details #######
        route_directions_list = route_json['route']['direction']
        print("get route direction details")

        for route_direction in route_directions_list: 
            pprint(route_direction)

            dir_name = route_direction['name']
            print("This is a {} route".format(dir_name))

            ####### start of loading direction details #######
            #Check if direction is already present in the table
            direction_id = Direction.query.with_entities(Direction.direction_id).filter(Direction.direction == dir_name).first()

            # direction is already present, don't load it 
            if direction_id: 
                print("Direction already present in the table")
                pass 
            else: 
                # Stop not present, so load it
                print("Direction not present. Add direction: {}".format(dir_name))
                new_dir = Direction(direction = dir_name)
                db.session.add(new_dir)
            
            db.session.commit()

            ####### end of loading direction details #######


            ####### start of loading bus route #######
        
            direction_id = Direction.query.with_entities(Direction.direction_id).filter(Direction.direction == dir_name).one()
            print('The direction id is: {}'.format(direction_id))

            #Check if bus route is already present in the table
            bus_route = Bus_Route.query.filter(and_(Bus_Route.tag == route_direction['tag'], Bus_Route.route_id == route.route_id, Bus_Route.direction_id == direction_id)).first()
            
            if bus_route: 
                # bus_route is already present, don't load it 
                print("Bus route already present in the table")
                pass
            else: 
                # bus route is not present, so load it. 
                new_bus_route = Bus_Route(title = route_direction['title'],
                    tag = route_direction['tag'] , 
                    route_id = route.route_id , 
                    direction_id = direction_id 
                    )

                db.session.add(new_bus_route)
                print("Loaded bus route {}".format(new_bus_route))

            db.session.commit()
            
            ####### end of loading bus route #######

            
            ####### start of loading bus route stops #######
            stop_list = route_direction['stop']
            tag = route_direction['tag']

            bus_route_id = Bus_Route.query.with_entities(Bus_Route.bus_route_id).filter(Bus_Route.tag == tag, Bus_Route.route_id == route.route_id, Bus_Route.direction_id == direction_id ).one()

            print("Bus route id is: {} for the bus tag: {}".format(bus_route_id, tag))

            for i, stop in enumerate(stop_list): 
                          
                stop_id = Stop.query.with_entities(Stop.stop_id).filter(Stop.stop_tag == int(stop['tag']))
                print("Stop id is {}".format(stop_id))

                #Check if stop on the bus route is already present in the table
                dup_bus_route_stop = Bus_Route_Stop.query.filter(and_(Bus_Route_Stop.bus_route_id == bus_route_id , Bus_Route_Stop.stop_id == stop_id)).first()
                
                if dup_bus_route_stop: 
                    # bus_route_stop is already present, don't load it 
                    continue
                else: 
                    # bus_route_stop is not present, so load it 
                    new_bus_route_stop = Bus_Route_Stop(bus_route_id = bus_route_id,
                        stop_id = stop_id, 
                        stop_seq = i)
                    db.session.add(new_bus_route_stop)
            db.session.commit()
            print("Loaded bus route stops for a direction")

            ####### end of loading bus route stops #######



if __name__ == "__main__": 
    connect_to_db(app)

    #In case tables haven't been created, create them
    db.create_all()

    #Import data from JSON files for static tables. 
    # load_region()
    # load_agency()
    # load_route()
