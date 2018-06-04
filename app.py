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

from sqlalchemy import func

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
    machine_rating = Column(Integer)
    deviations = Column(Integer)

# Use a Session to test the Review class

from sqlalchemy import create_engine
from sqlalchemy.orm import Session

engine = create_engine("sqlite:///reviews.sqlite")
Base.metadata.create_all(engine)

session = Session(bind=engine)

@app.route("/", methods=["GET", "POST"])
def index():
    s = ""
    top = ""
    bottom = ""
    searchTerms = ""
    percentage_accurate = ""
    if request.method == "POST":
        print(request.form)
        human_rate = int(request.form['humanRating'])
        searchTerms = request.form['searchTerms']
        from Hee_final import word_to_predict
        predicted = word_to_predict(searchTerms)
        s = int(predicted)
        deviation = abs(human_rate - s)
        session.add(Reviews(review=searchTerms, human_rating = human_rate, machine_rating = s, deviations = deviation))
        session.commit()
        top = session.query(Reviews).filter(Reviews.deviations == 0).count()
        print(top)
        bottom = session.query(Reviews.deviations).count()
        print(bottom)
        percentage_accurate = round(top/bottom,2) * 100
    return render_template('index.html', predict = s, review_term = searchTerms, accuracy = percentage_accurate)
    
# @app.route("/methodology/")
# def methodology():
#     return render_template("methodology.html")

### ADDITIONS
@app.route("/methodology/")
def methodology():
    return render_template("methods.html")

@app.route("/data/naive_b")
def naives():
    return render_template("Naive_B.html")

@app.route("/data/neural_n")
def neurals():
    return render_template("Neural_N.html")

@app.route("/data/data_clean")
def cleans():
    return render_template("Data_clean.html")

### END OF ADDITIONS

@app.route("/home/")
def home():
    return render_template("index.html")    

@app.route('/data/')
def sqlquery():
    response = session.query(Reviews.record_id, Reviews.review, Reviews.human_rating, Reviews.machine_rating, Reviews.deviations).all()
    return jsonify(response)

@app.route('/barchart')
def chart():
    
    human_rating = session.query(Reviews.human_rating, func.count(Reviews.human_rating)).group_by(Reviews.human_rating).all()
    machine_rating = session.query(Reviews.machine_rating, func.count(Reviews.machine_rating)).group_by(Reviews.machine_rating).all()
    deviations = session.query(Reviews.deviations, func.count(Reviews.deviations)).group_by(Reviews.deviations).all()
     
    human_rating_x = [row[0] for row in human_rating]
    human_rating_y = [row[1] for row in human_rating]

    machine_rating_x = [row[0] for row in machine_rating]
    machine_rating_y = [row[1] for row in machine_rating]

    deviations_x = [row[0] for row in deviations]
    deviations_y = [row[1] for row in deviations]
    
    return jsonify({'human_rating_x': human_rating_x, 'human_rating_y': human_rating_y, 'machine_rating_x': machine_rating_x, 'machine_rating_y': machine_rating_y, 'deviations_x': deviations_x, 'deviations_y': deviations_y })

@app.route('/NaiveBayes_Yelp_30K_BM.html')
def pic():
    return render_template("NaiveBayes_Yelp_30K_BM.html")

if __name__ == "__main__":
    app.run(debug=True, port=5022)
