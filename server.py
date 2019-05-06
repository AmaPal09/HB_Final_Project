from flask import (Flask, render_template, redirect, request, flash,
                    session)


app = Flask(__name__)
app.secret_key = 'abc'

@app.route('/')
def index(): 
    """ Homepage """

    return print("Hello")

