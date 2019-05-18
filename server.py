from flask import (Flask, render_template, redirect, request, flash,
                    session)
from model import connect_to_db, db, Route, Bus, User_Rating, Rating

app = Flask(__name__)
app.secret_key = 'abc'

@app.route('/')
def index(): 
    """ Homepage """

    return render_template("homepage.html")


@app.route('/routes')
def route_list(): 
    """ Display list of all Muni Routes present in SF"""

    routes = Route.query.filter(Route.agency_id == 49).all()
    print(type(routes[0]))

    return render_template("route_list.html", routes=routes)


@app.route('/routes/<route_id>')
def route_details(route_id): 
    """ Display the bus routes for the selected route """ 
    print("Step1")
    route = Route.query.filter(Route.route_id == int(route_id)).one()
    print("Step2")
    buses = Bus.query.filter(
        Bus.route_id==route.route_id
        ).options(db.joinedload("bus_ratings_details")
        ).all()
    print("Step3")
    
    #bus_routes is a list of objs of class Bus_Route
    print(type(buses))

    ratings_details_list = []
    for bus in buses: 
        #for each instance, bus_route.bus_ratings is a list of objs of class User_Rating
        for bus_user_rating in bus.bus_ratings_details: 
            ratings_details_list += Rating.query.filter(
                Rating.rating_id == bus_user_rating.rating_id
                ).all()

            
    print(type(ratings_details_list))
    print(type(ratings_details_list[0]))
    print(ratings_details_list)

    return render_template(
        "route_details.html", 
        route=route, 
        buses = buses, 
        ratings_details_list = ratings_details_list
        )






if __name__ == "__main__": 
    app.debug = True
    connect_to_db(app)

    app.run(port=5000, host='0.0.0.0')
5000
