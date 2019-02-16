from flask import Flask
from flask import render_template
from flask import Response
from flask import jsonify
import numpy as np
import time

from src.csv2json import filter_data
from src.gsheet2csv import load_gspread
from src.crunch_numbers import text_data, pie_data, map_data, numbers_data

app = Flask(__name__)
time_cached_gspread = time.time()

def load_data():
    global time_cached_gspread
    elapsed = time.time() - time_cached_gspread
    if elapsed > 15*60:
        print('Reloading cache from gspread (last time was {}s ago)'.format(np.round(elapsed, 3)))
        load_gspread()
        time_cached_gspread = time.time()
    return filter_data()

@app.route('/data/json')
def get_json():
    # Get data
    data = load_data()

    return jsonify(data)

@app.route('/')
def hello_world():
    # Get data
    data = load_data()

    # Crunch numbers
    feed_text = text_data(data)
    feed_pie = pie_data(data)
    feed_map = map_data(data)
    feed_numbers = numbers_data(data)

    return render_template('index.html', **feed_text, **feed_pie, **feed_map, **feed_numbers)