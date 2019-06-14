from flask import (Flask, render_template, redirect, request, flash, session, jsonify)
from model import connect_to_db, db, Route, Bus, User, User_Rating, Rating, Stop

from geopy.geocoders import Nominatim
from geopy.distance import geodesic
import requests
import json


from werkzeug.security import generate_password_hash

app = Flask(__name__)
app.secret_key = 'abc'

geolocator = Nominatim(user_agent='HB_final_project')

@app.route('/')
def index(): 
    """ Homepage """

    return render_template("homepage.html")


@app.route('/buses')
def bus_list(): 
    """ Display list of all Muni Buses present in SF"""

    buses = Bus.query.options(db.joinedload("bus_route")).order_by(Bus.bus_id).all() 
    
    return render_template("bus_list.html", buses=buses)


@app.route('/buses/<bus_id>')
def bus_details(bus_id): 
    """ Display the bus details for the selected bus """ 
    
    bus = Bus.query.filter(
        Bus.bus_id==int(bus_id)
        ).options(db.joinedload("bus_ratings_details")
        ).first()
    # print(bus)

    session['bus'] = bus.to_dict()

    # Assemble all the labels for the chart
    chart_labels = ['crowd_rating', 'time_rating', 'cleanliness_rating', 
                    'safety_rating', 'outer_view_rating']
    
    #Get the average of the bus ratings in a list
    avg_ratings = get_rating_avg(bus.bus_ratings_details)

    return render_template(
        "bus_details.html", 
        bus = bus, 
        labels = chart_labels, 
        values = avg_ratings
        )


@app.route('/bus-route/map')
def bus_route_map(): 
    # print('start the route for json')
    map_data = {}
    # print(map_data)
    map_data['bus_id'] = session['bus']['bus_id']
    map_data['stop_list'] = []
    # print(map_data)


    bus = Bus.query.filter(
        Bus.bus_id==int(session['bus']['bus_id'])
        ).options(db.joinedload("bus_stops")
        ).first()

    map_data['start_lat'] = bus.bus_stops[0].stop_lat
    map_data['start_lng'] = bus.bus_stops[0].stop_lon
    map_data['end_lat'] = bus.bus_stops[0].stop_lat
    map_data['end_lng'] = bus.bus_stops[0].stop_lon

    for stop in bus.bus_stops: 
        map_data['stop_list'].append(stop.to_dict())

    return jsonify(map_data)




def get_rating_avg(ratings):
    """ Return list of average ratings for all 5 parameters 
    I/P: List
    O/P: List
    Called from: bus_details
    """ 

    if len(ratings) == 0: 
        return [0,0,0,0,0]
    else: 
        total_crowd_rating = 0 
        total_time_rating = 0
        total_cleanliness_rating = 0
        total_safety_rating = 0
        total_outer_view_rating = 0

        for rating in ratings: 
            total_crowd_rating += rating.crowd_rating
            total_time_rating += rating.time_rating
            total_cleanliness_rating += rating.cleanliness_rating
            total_safety_rating += rating.safety_rating
            total_outer_view_rating += rating.outer_view_rating

        return [total_crowd_rating/len(ratings),
                total_time_rating/len(ratings),
                total_cleanliness_rating/len(ratings),
                total_safety_rating/len(ratings),
                total_outer_view_rating/len(ratings)]


@app.route('/user_geolocation' , methods=['POST'])
def users_geolocation(): 
    """ Get the lat and long of the system user is using and display closest
        stops """

    # user_lat = request.json.get("lat")
    # user_lng = request.json.get("lng")

    user_lat = request.form.get("lat")
    user_lng = request.form.get("lng")

    user_cord_str = str(user_lat) + " , " + str(user_lng)

    user_location = geolocator.reverse(user_cord_str)
    # print(user_location)
    # print(user_location.address)

    if is_in_SF(user_location.address): 
        # print("user is in SF")
        distances, stop_dict, stop_dict_2 = get_ten_closest_stops((user_lat, 
                                user_lng))
        # print(stop_dict[distances[0]][0].stop_buses)    
    else: 
        # print("user not in SF")
        flash("Enter a location in SF")
        return redirect("/")

    # print(distances)
    # print(stop_dict)
    session['user_lat'] = user_lat
    session['user_lng'] = user_lng
    # session['distances'] = distances
    session['stop_list'] = []
    for key in stop_dict_2.keys(): 
        for stop in stop_dict_2[key]:
            session['stop_list'].append(stop.to_dict()) 

    return render_template("stop_details.html", 
                            distances = distances,
                            stop_dict = stop_dict)

@app.route('/stop-details/map')
def stop_details_map(): 
    map_data = {}
    map_data['user_lat'] = session['user_lat']
    map_data['user_lng'] = session['user_lng']
    map_data['stop_list'] = session['stop_list']

    return jsonify(map_data)


@app.route('/stops_address', methods = ['POST'])
def stops_address(): 
    """ Get the lat and long of the system user is using and display closest
        stops """
    # Get address details from user
    block = request.form.get("block")
    street = request.form.get("street")

    # create address string for San Fransico
    address = block+' '+street+' '+'SF'
    # print(address)
    # Get the address geocode details from geopy
    user_start_point = geolocator.geocode(address)
    # print(user_start_point.latitude)
    # print(user_start_point.longitude)
    # print(user_start_point.raw)   

    if is_in_SF(user_start_point.raw['display_name']): 
        distances, stop_dict, stop_dict_2 = get_ten_closest_stops((user_start_point.latitude, 
                                user_start_point.longitude))
    else: 
        flash("Enter a location in SF")
        return redirect("/")
    
    # print(stop_dict[distances[0]][0].stop_buses)    

    session['user_lat'] = user_start_point.latitude
    session['user_lng'] = user_start_point.longitude
    # session['distances'] = distances
    session['stop_list'] = []
    for key in stop_dict_2.keys(): 
        for stop in stop_dict_2[key]:
            session['stop_list'].append(stop.to_dict()) 

    return render_template("stop_details.html", 
                            distances = distances,
                            stop_dict = stop_dict)

def is_in_SF(address_string):
    """ Check is given address is in SF 
    I/P: String 
    O/P: Boolean 
    Called from: stops_address
    """

    # print('Started is_in_SF')
    address_list = address_string.split(', ')
    # print(address_list)
    return (('SF' in address_list) or ('San Francisco' in address_list))


def get_ten_closest_stops(user_loc_tuple): 
    """ Get the closest 10 stop to user location 
    I/P: latitude & longitude (float values) 
    O/P: list of 10 lats and longs
    called from: stops_addres
    Sample: (37.7895479795918, -122.406717877551)
    """
    # print("user_lat & user_long is: ", user_loc_tuple)

    # get all the stops
    stops = Stop.query.options(db.joinedload("stop_buses")).all()
    # dict to stops stops for their dist from the user
    dist_stop_dict = {} 

    # print(stops[0])
    for stop in stops: 
        # get dist of a stop from user in miles upto 1 decimal position
        dist = round(
            geodesic(
                user_loc_tuple,(stop.stop_lat, stop.stop_lon)
                ).miles,1 
            )

        # load the stop for to the dict depending on the dist. 
        if dist in dist_stop_dict: 
            dist_stop_dict[dist].append(stop)
        else: 
            dist_stop_dict[dist] = [stop]

    # print(dist_stop_dict.keys()) 
    dist_stop_ordered = merge_sort(list(dist_stop_dict.keys()))
    
    dist_ordered_dict = {}

    for i in range(0,10):
        # print(i)
        if i == 0: 
            dist_ordered_dict[dist_stop_ordered[i]] = \
            dist_stop_dict[dist_stop_ordered[i]]
        elif i == 1: 
            dist_ordered_dict[dist_stop_ordered[i]] = \
            dist_stop_dict[dist_stop_ordered[i]][:3]
        elif i == 2: 
            dist_ordered_dict[dist_stop_ordered[i]] = \
            dist_stop_dict[dist_stop_ordered[i]][:2]
        else: 
            dist_ordered_dict[dist_stop_ordered[i]] = \
            dist_stop_dict[dist_stop_ordered[i]][:1]

    dist_ordered_dict_2 = {}
    for i in range(0,10):
        # print(i)
        if i == 0: 
            dist_ordered_dict_2[str(dist_stop_ordered[i])] = \
            dist_stop_dict[dist_stop_ordered[i]]
        elif i == 1: 
            dist_ordered_dict_2[str(dist_stop_ordered[i])] = \
            dist_stop_dict[dist_stop_ordered[i]][:3]
        elif i == 2: 
            dist_ordered_dict_2[str(dist_stop_ordered[i])] = \
            dist_stop_dict[dist_stop_ordered[i]][:2]
        else: 
            dist_ordered_dict_2[str(dist_stop_ordered[i])] = \
            dist_stop_dict[dist_stop_ordered[i]][:1]
    
    return dist_stop_ordered[:10] , (dist_ordered_dict), dist_ordered_dict_2

        
def merge_sort(dist_list): 
    """ Merge sort list and return result
    I/P: List 
    O/P: List 
    Called from: get_ten_closest_stops
    """

    # Break everything down into a list of one
    if len(dist_list) < 2:  # if length of lst is 1, return lst
        # print("returning", dist_list)
        return dist_list

    mid = int(len(dist_list) / 2)  # index at half the list
    list1 = merge_sort(dist_list[:mid])  # divide list in half
    list2 = merge_sort(dist_list[mid:])  # assign other half

    return make_merge(list1, list2)


def make_merge(list1, list2):
    """Merge lists
    I/P: 2 Lists
    O/P: 1 merged List
    Called from: merge_sort """

    result_list = []
    # print(list1, list2)
    while len(list1) > 0 or len(list2) > 0:
        # if items left in both lists
        # compare first items of each list
        if list1 == []:
            result_list.append(list2.pop(0))
        elif list2 == []:
            result_list.append(list1.pop(0))
        elif list1[0] < list2[0]:
            # append and rm first item of lst1
            result_list.append(list1.pop(0))
        else:
            # append and rm first item of lst2
            result_list.append(list2.pop(0))

    # print("returning merge", result_list)
    return result_list


    

@app.route('/login', methods=['GET'])
def login_form(): 
    """User login form"""

    return render_template("login_form.html")


@app.route('/login', methods=['POST'])
def user_login(): 
    """ Validate email id and password and log the user in"""
    
    if is_logged_in(): 
        flash("User already logged in")
        return redirect("/")
    else: 
        email = request.form.get("email")
        password = request.form.get("password")

        user = User.query.filter(User.user_email == email).first()

        if user is not None and user.check_user_pwd(password): 
            session['user_id'] = user.user_id
            flash("Logged in")
            session.modified = True
            return redirect("/")
        else: 
            if user is None: 
                flash("User does not exist. Please signin")
                return redirect("/")
            else: 
                flash("Log in unsuccessful")
                return redirect("/")


@app.route('/logout')
def logout(): 
    # print(session)

    if is_logged_in(): 
        session.pop('user_id')
        flash("Logged out")
        # print(session)
    else: 
        flash("No user logged in currently")
        # print(session)

    return redirect("/")


@app.route('/signin', methods=['GET'])
def signin_form(): 
    """ Render form for user signin"""

    return render_template("user_signin.html")


@app.route('/signin', methods=['POST'])
def user_signin(): 
    """ Add new user """

    email = request.form.get("email")

    if User.query.filter(User.user_email == email).first(): 
        flash("User already exsits. Login here")
        # print("User exists")
        return redirect("/login")
    else: 
        new_user = User(
            user_fname = request.form.get("fname"), 
            user_lname = request.form.get("lname"), 
            user_email = email, 
            user_pwd_hash = generate_password_hash(
                request.form.get("password")
                )
            )
        db.session.add(new_user)
        db.session.commit()
        flash("Sign in successful")
        # print("Sign in success")
        return redirect("/")


@app.route('/rate_bus/<bus_id>', methods=['POST'])
def rate_bus(bus_id):
    """ Rate the bus id selected by user
        If the user is logged in add rating to the ratings table and generate the
        rating id and use that rating id load the user_rating table
    """
    # print(bus_id)
    if is_logged_in(): 
        pass
    else: 
        flash("Please log in to rate this route")
        return redirect("/login")

    date_text = request.form.get("trip_date")
    time_text = request.form.get("trip_time")
    date_time = request.form.get("trip_date") + ' ' + request.form.get("trip_time") +':00.000000' 
    print(date_time)
    new_rating = Rating(
        crowd_rating = int(request.form.get("crowd_rating")) ,
        time_rating = int(request.form.get("time_rating")) ,
        cleanliness_rating = int(request.form.get("cleanliness_rating")) ,
        safety_rating = int(request.form.get("safety_rating")) ,
        outer_view_rating = int(request.form.get("outer_view_rating")) ,
        rating_datetime = date_time, 
        rating_text = request.form.get("rating_text"))
    db.session.add(new_rating)
    db.session.commit()
    db.session.refresh(new_rating)
    print(new_rating)

    new_bus_rating = User_Rating(
        user_id = session['user_id'], 
        rating_id = new_rating.rating_id, 
        bus_id = int(bus_id)
        )
    db.session.add(new_bus_rating)
    db.session.commit()
    return redirect("/")


def is_logged_in(): 
    """ Return True is a user is logged in. 
        Else return False
    """
    return 'user_id' in session


@app.route("/static/<path:resource>")
def get_resource(resource):
    return send_from_directory("static", resource)


if __name__ == "__main__": 
    app.debug = True
    connect_to_db(app)

    app.run(port=5000, host='0.0.0.0')
5000
