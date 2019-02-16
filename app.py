from flask import Flask
from flask import render_template
from flask import Response
from flask import jsonify
import numpy as np

from src.getdata import get_numbers
from src.crunch_numbers import text_data, pie_data

app = Flask(__name__)

@app.route('/data/json')
def get_json():
    # Get data
    data = get_numbers()

    return jsonify(data)

@app.route('/')
def hello_world():
    # Get data
    data = get_numbers()

    # Crunch numbers
    feed_text = text_data(data)
    feed_pie = pie_data(data)

    return render_template('index.html', **feed_text, **feed_pie)