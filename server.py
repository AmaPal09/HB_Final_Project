from flask import (Flask, render_template, redirect, request, flash,
                    session)
from model import connect_to_db 

app = Flask(__name__)
app.secret_key = 'abc'

@app.route('/')
def index(): 
    """ Homepage """

    return render_template("homepage.html")



if __name__ == "__main__": 
    app.debug = True
    connect_to_db(app)

    app.run(port=5000, host='0.0.0.0')
5000
