from flask import (Flask, render_template, redirect, request, flash, session, jsonify)
from model import connect_to_db, db, Route, Bus, User, User_Rating, Rating

from werkzeug.security import generate_password_hash

app = Flask(__name__)
app.secret_key = 'abc'

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
        ).all()
    print(bus)

    # Assemble all the labels for the chart
    chart_labels = ['crowd_rating', 'time_rating', 'cleanliness_rating', 
                    'safety_rating', 'outer_view_rating']
    
    #Get the average of the bus ratings in a list
    avg_ratings = get_rating_avg(bus[0].bus_ratings_details)

    return render_template(
        "bus_details.html", 
        bus = bus, 
        labels = chart_labels, 
        values = avg_ratings
        )


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
    print(session)

    if is_logged_in(): 
        session.pop('user_id')
        flash("Logged out")
        print(session)
    else: 
        flash("No user logged in currently")
        print(session)

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
        print("User exists")
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
        print("Sign in success")
        return redirect("/")


@app.route('/rate_bus/<bus_id>', methods=['POST'])
def rate_bus(bus_id):
    """ Rate the bus id selected by user
        If the user is logged in add rating to the ratings table and generate the
        rating id and use that rating id load the user_rating table
    """
    print(bus_id)
    if is_logged_in(): 
        pass
    else: 
        flash("Please log in to rate this route")
        return redirect("/login")

    new_rating = Rating(
        crowd_rating = int(request.form.get("crowd_rating")) ,
        time_rating = int(request.form.get("time_rating")) ,
        cleanliness_rating = int(request.form.get("cleanliness_rating")) ,
        safety_rating = int(request.form.get("safety_rating")) ,
        outer_view_rating = int(request.form.get("outer_view_rating")) ,
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






if __name__ == "__main__": 
    app.debug = True
    connect_to_db(app)

    app.run(port=5000, host='0.0.0.0')
5000
