"""Models and DB functions for Hackbright Transportation Project"""

from flask import Flask
from flask_sqlalchemy import SQLAlchemy

#Create flask application
app = Flask(__name__)
#create SQLAlcemy object for the flask set-up by passing. 
db = SQLAlchemy(app)

#Configure the flask application to point to postgres DB created for this project
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgres:///hb_project_db'
#Echo set to True in Dev for debugging
app.config['SQLALCHEMY_ECHO'] = True
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db.app = app
db.init_app(app)

print("Connected to DB")


##############################################################################
# Composing ORM

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
        nullable = False)
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


class Route(db.Model): 
    """ Route Model """

    route_id = db.Column(
        db.Integer, 
        primary_key = True, 
        autoincrement = True)
    agency_id = db.Column(
        db.Integer, 
        db.ForeignKey('agencies.agency_id'), 
        nullable = False)
    route_tag = db.Column(
        db.String(10),
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