import os

import pandas as pd
import numpy as np

import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine
import Hee_final
import test
from flask import Flask, jsonify, render_template, request
app = Flask(__name__)


# #################################################
# # Database Setup
# #################################################
# dbfile = os.path.join('db', 'belly_button_biodiversity.sqlite')
# engine = create_engine(f"sqlite:///{dbfile}")

# # reflect an existing database into a new model
# Base = automap_base()
# # reflect the tables
# Base.prepare(engine, reflect=True)

# # Save references to each table
# Samples_Metadata = Base.classes.samples_metadata
# OTU = Base.classes.otu
# Samples = Base.classes.samples

# # Create our session (link) from Python to the DB
# session = Session(engine)


@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        print(request.form)
        searchTerms = request.form['searchTerms']
        from Hee_final import word_to_predict
        # sentence = "The food is awful, i would no recommend this place. Decor is grim and service is terrible. Do not come back"
        predicted = word_to_predict(searchTerms)
        s = int(predicted)
        print(s)
        return render_template('index.html', predict = s)
    # return render_template('index.html')

@app.route('/test')
def testoutput():
    from Hee_final import word_to_predict
    sentence = "The food is awful, i would no recommend this place. Decor is grim and service is terrible. Do not come back"
    predicted = word_to_predict(sentence)
    s = int(predicted)
    return jsonify(s)

@app.route('/one')
def one():
    from test import addone
    number = 6
    q = addone(number)
    return jsonify(q)


if __name__ == "__main__":
    app.run(debug=True)
