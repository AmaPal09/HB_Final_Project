"""Models and DB functions for Hackbright Transportation Project"""

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
# from db import PrimaryKeyConstraint
# from flask_sqlalchemy import SQLALCHEMY_ECHO


db = SQLAlchemy()


##############################################################################
# Composing ORM

#Details of various areas and bus agencies in those areas

class Region(db.Model):
    """Region Model."""

    __tablename__ = "regions"

    region_id = db.Column( 
        db.Integer, 
        primary_key = True, 
        autoincrement = True)
    region = db.Column(
        db.String(50), 
        nullable = False)

    region_agency = db.relationship('Agency')
    
    def __repr__(self):
        """Show info about Region"""

        return "Region_ID={}, Region={}".format(
            self.region_id, self.region)


class Agency(db.Model):
    """Agency Model."""

    __tablename__ = "agencies"

    agency_id = db.Column( 
        db.Integer, 
        primary_key = True, 
        autoincrement = True)
    agency_tag = db.Column(
        db.String(20), 
        nullable = False)
    agency_short_title = db.Column(
        db.String(30), 
        nullable = True)
    agency_title = db.Column(
        db.String(50), 
        nullable = False)
    region_id = db.Column(
        db.Integer, 
        db.ForeignKey('regions.region_id'),
        nullable = False)

    agency_region = db.relationship('Region')
    agency_route = db.relationship('Route')

    def __repr__(self):
        """Show info about Agency"""

        return "Agency_ID={}, Agency_Tag={}, Agency_short_title={}, Agency_Title={}, Region_ID={}" .format(
            self.agency_id, self.agency_tag, self.agency_short_title, self.agency_title, self.region_id)


#Details of various bus routes for an agency

class Route(db.Model): 
    """ Route Model """

    __tablename__ = "routes"

    route_id = db.Column(
        db.Integer, 
        primary_key = True, 
        autoincrement = True)
    agency_id = db.Column(
        db.Integer, 
        db.ForeignKey('agencies.agency_id'), 
        nullable = False)
    route_tag = db.Column(
        db.String(30),
        nullable = False)
    route_title = db.Column(
        db.String(50),
        nullable = False)

    route_agency = db.relationship('Agency')

    def __repr__(self): 
        """ Show info about Route """

        return "Route_ID={}, Agency_ID={}, Route_Tag={}, Route_Title={}".format(
            self.route_id, self.agency_id, self.route_tag, self.route_title)



class Direction(db.Model): 
    """ Direction Model """

    __tablename__ = "directions"

    direction_id = db.Column(
        db.Integer, 
        primary_key = True, 
        autoincrement = True)
    direction = db.Column(
        db.String(15), 
        nullable = False)

    def __repr__(self):
        """ Show info about Direction"""

        return "Direction_ID={}, Direction={}".format(
            self.direction_id, self.direction)


class Bus_Route(db.Model): 
    """ Route Model """

    __tablename__ = "bus_routes"

    bus_route_id = db.Column(
        db.Integer, 
        primary_key = True, 
        autoincrement = True)
    title = db.Column(
        db.String(60),
        nullable = False)
    tag = db.Column(
        db.String(20),
        nullable = False)
    route_id = db.Column(
        db.Integer, 
        db.ForeignKey('routes.route_id'), 
        nullable = False)
    direction_id = db.Column(
        db.Integer, 
        db.ForeignKey('directions.direction_id'), 
        nullable = False)
    # stop_id = db.Column(
    #     db.Integer,
    #     db.ForeignKey('stops.stop_id'),
    #     nullable = False)
    # stop_seq = db.Column(
    #     db.Integer,
    #     nullable = False)

    bus = db.relationship('Route')
    bus_direction = db.relationship('Direction')
    bus_rating_by_users = db.relationship('User_Rating')
    
    # bus_route_stop = db.relationship('Stop')

    def __repr__(self): 
        """ Show info about Route """

        return "Bus_Route_ID={}, Title={}, Tag={}, Route_Id={}, Direction_ID={}".format(
            self.bus_route_id, self.title, self.tag, self.route_id, self.direction_id)


#Details of various stops of various bus routes

class Stop(db.Model): 
    """ Bus Stop Model """

    __tablename__ = "stops" 

    stop_id = db.Column(
        db.Integer,
        primary_key = True,
        autoincrement = True)
    stop_tag  = db.Column(
        db.Integer,
        nullable = False)
    stop_id_tag = db.Column(
        db.Integer,
        nullable = False)
    stop_title = db.Column(
        db.String(50),
        nullable = False)
    stop_lon = db.Column(
        db.Float(),
        nullable = False)
    stop_lat = db.Column(
        db.Float(), 
        nullable = False)

    stops_on_bus_route = db.relationship('Bus_Route_Stop')

    def __repr__(self): 
        """ Show info about Stop""" 

        return "Stop_ID={}, Stop_Tag={}, Stop_ID_Tag={}, Stop_Title={}, Stop_Longitude={}, Stop_Latitude={}".format(
            self.stop_id, self.stop_tag, self.stop_id_tag, self.stop_title, self.stop_lon, self.stop_lat)


class Bus_Route_Stop(db.Model): 
    """ Bus route and stops model 
    Intermediate table to handle many to many relationship """

    __tablename__ = "bus_route_stops"

    bus_route_id = db.Column( 
        db.Integer,
        db.ForeignKey('bus_routes.bus_route_id'),
        primary_key = True) 
    stop_id = db.Column(
        db.Integer,
        db.ForeignKey('stops.stop_id'), 
        primary_key = True)
    stop_seq = db.Column(
        db.Integer,
        nullable = False) 

    bus_route_with_stop = db.relationship('Bus_Route')

    def __repr__(self): 
        """ Show info about stops on a bus route """

        return "Bus_Route_ID={}, Stop_ID={}, Stop_Seq={}".format(
            self.bus_route_id, self.stop_id, self.stop_seq)


#User details

class User(db.Model): 
    """ User Model""" 

    __tablename__ = "users"

    user_id = db.Column(
        db.Integer, 
        primary_key = True,
        autoincrement = True)
    user_fname = db.Column(
        db.String(50),
        nullable = False)
    user_lname = db.Column(
        db.String(50),
        nullable = False)
    user_email = db.Column(
        db.String(60),
        nullable = False)

    user_rated = db.relationship('User_Rating')

    def __repr__(self): 
        """ Show info about user""" 

        return "User_ID={}, User_First_Name={}, User_Last_Name={}, User_Email={}".format(
            self.user_id, self.user_fname, self.user_lname, self.user_email)


class Rating(db.Model): 
    """ Ratings Model"""

    __tablename__ = "ratings"

    rating_id = db.Column(
        db.Integer,
        primary_key = True,
        autoincrement = True)
    rating_datetime = db.Column(
        db.DateTime,
        nullable = False,
        default = datetime.utcnow)
    crowd_rating = db.Column(
        db.Integer,
        nullable = False)
    time_rating = db.Column(
        db.Integer, 
        nullable = False)
    cleanliness_rating = db.Column(
        db.Integer, 
        nullable = False)
    safety_rating = db.Column(
        db.Integer, 
        nullable = False)
    outer_view_rating = db.Column(
        db.Integer, 
        nullable = False) 
    rating_text = db.Column(
        db.String(100),
        nullable = True )

    def __repr__(self): 
        """ Show info about user_ratings""" 

        return "Rating_ID={}, Rating_Datetime={}, Crowd_Rating={}, Time_Rating={}, Cleanliness_Rating={}, Safety_Rating={}, Outer_View_Rating={}, Rating_Text={}".format(
            self.rating_id, self.rating_datetime, self.crowd_rating, self.time_rating, self.cleanliness_rating, self.safety_rating, self.outer_view_rating, self.rating_text)



class User_Rating(db.Model): 
    """ User Ratings Model"""

    __tablename__ = "user_ratings"

    user_id = db.Column(
        db.Integer, 
        db.ForeignKey('users.user_id'),
        primary_key = True) 
    rating_id = db.Column(
        db.Integer, 
        db.ForeignKey('ratings.rating_id'), 
        primary_key = True)
    bus_route_id = db.Column(
        db.Integer, 
        db.ForeignKey('bus_routes.bus_route_id'), 
        primary_key = True)
    trip_datetime = db.Column(
        db.DateTime,
        nullable = False,
        default = datetime.utcnow)

    user_details = db.relationship('User')
    bus_route_details = db.relationship('Bus_Route')
    rating_details = db.relationship('Rating')
    
    def __repr__(self): 
        """ Show info about user""" 

        return "User_ID={}, Rating_ID={}, Bus_Route_ID={}, Trip_Datetime={}".format(
            self.user_id, self.rating_id, self.bus_route_id, self.trip_datetime)


################################################################################
def connect_to_db(app): 
    """Configure the flask application to point to postgres DB created for this project

        Connect the Flask app to the DB 

    """

    #Create flask application
      
    app.config['SQLALCHEMY_DATABASE_URI'] = 'postgres:///hb_project_db'
    #Echo set to True in Dev for debugging
    # app.config['SQLALCHEMY_ECHO'] = True
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    db.app = app
    db.init_app(app)

if __name__ == "__main__": 
    # Add this to allow working with module interactively. 

    from server import app
    connect_to_db(app)
    print("Connected to DB")
