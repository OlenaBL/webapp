import flask
import pickle
import pandas as pd
import numpy as np
from flask import Flask, render_template, request, redirect, url_for
from numpy.core.arrayprint import dtype_is_implied


# Use pickle to load in the pre-trained model
with open(f'model/bike_model_xgboost.pkl', 'rb') as f:
    model = pickle.load(f)

# Initialise the Flask app
app = flask.Flask(__name__, template_folder='templates')

# Set up the main route
@app.route('/', methods=['GET', 'POST'])
def main():
    if flask.request.method == 'GET':
        # Just render the initial form, to get input
        return(flask.render_template('main.html'))
    
    if flask.request.method == 'POST':
        # Extract the input
        text = flask.request.form['text']
        #text = [text]
        #humidity = flask.request.form['humidity']
        #windspeed = flask.request.form['windspeed']

        # Make DataFrame for model
        input_variables = pd.DataFrame([[text]], #humidity, windspeed]], 
                                       columns=['text'], #'temperature', 'humidity', 'windspeed'],
                                       dtype=np.array,
                                       index=['input'])
        
        #input_variables = pd.DataFrame(text, index=['input'], columns=['text'])
        #input_variables['text'] = input_variables['text'].astype(float)

        # Get the model's prediction
        prediction = model.predict(input_variables)[0]
    
        # Render the form again, but add in the prediction and remind user
        # of the values they input before
        return flask.render_template('main.html',
                                     original_input={'text':text},
                                                     #'Humidity':humidity,
                                                     #'Windspeed':windspeed},
                                     result=clf,
                                     )

if __name__ == '__main__':
    app.run()
