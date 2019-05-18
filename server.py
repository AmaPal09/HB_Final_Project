from flask import (Flask, render_template, redirect, request, flash, session)
from model import connect_to_db, db, Route, Bus, User, User_Rating, Rating

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
    print(buses[0].bus_ratings_details)
    
    #bus_routes is a list of objs of class Bus_Route

    return render_template(
        "route_details.html", 
        route=route, 
        buses = buses
        )


@app.route('/login', methods=['GET'])
def login_form(): 
    """User login form"""

    return render_template("login_form.html")


@app.route('/login', methods=['POST'])
def user_login(): 
    """ Validate password and log user in"""

    print("Entered /login POST route")
    email = request.form.get("email")
    print(email)
    password = request.form.get("password")
    print(password)

    user = User.query.filter(User.user_email == email).first()

    # print(user)
    # print(user.check_user_pwd(password))
    # print(session.keys())
    if user is not None and user.check_user_pwd(password) and 'user_id' not in session.keys(): 
        session['user_id'] = user.user_id
        flash("Logged in")
        session.modified = True
        return redirect("/")
    else: 
        flash("Log in unsuccessful")
        return redirect("/")


if __name__ == "__main__": 
    app.debug = True
    connect_to_db(app)

    app.run(port=5000, host='0.0.0.0')
5000
