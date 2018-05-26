import os

import pandas as pd
import numpy as np
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine
import Hee_final
import test
from flask import Flask, jsonify, render_template, request



# Flask App
app = Flask(__name__)


### Using 11/2/1
from sqlalchemy import Column, Float, Integer, String
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

# Define a Reviews class
class Reviews(Base):
    __tablename__ = 'review_history'

    record_id = Column(Integer, primary_key=True)
    review = Column(String)
    human_rating = Column(Integer)

# Use a Session to test the Review class

from sqlalchemy import create_engine
from sqlalchemy.orm import Session

engine = create_engine("sqlite:///reviews.sqlite")
Base.metadata.create_all(engine)

session = Session(bind=engine)





@app.route("/", methods=["GET", "POST"])
def index():
    # predict = ""
    s = ""
    searchTerms = ""
    if request.method == "POST":
        print(request.form)
        human_rate = request.form['humanRating']
        searchTerms = request.form['searchTerms']
        from Hee_final import word_to_predict
        predicted = word_to_predict(searchTerms)
        s = int(predicted)
        print(s)
        session.add(Reviews(review=searchTerms, human_rating = human_rate))
        session.commit()
    return render_template('index.html', predict = s, review_term = searchTerms)
    


@app.route("/data/")
def data():
    return render_template("data.html")

@app.route("/methodology/")
def methodology():
    return render_template("Method.html")

@app.route("/home/")
def home():
    return render_template("index.html")    


# @app.route('/test')
# def testoutput():
#     from Hee_final import word_to_predict
#     sentence = "The food is awful, i would no recommend this place. Decor is grim and service is terrible. Do not come back"
#     predicted = word_to_predict(sentence)
#     s = int(predicted)
#     return jsonify(s)

@app.route('/collection')
def sqlquery():
    x = session.query(Reviews.record_id, Reviews.review, Reviews.human_rating).all()
    return jsonify(x)


if __name__ == "__main__":
    app.run(debug=True, port=5001)
