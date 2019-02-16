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

def load_data(n_days=0):
    global time_cached_gspread
    elapsed = time.time() - time_cached_gspread
    if elapsed > 60*60:
        print('Reloading cache from gspread (last time was {}s ago)'.format(np.round(elapsed, 3)))
        load_gspread()
        time_cached_gspread = time.time()
    return filter_data(n_days)

@app.route('/data/json/')
@app.route('/data/json/<int:n_days>')
def get_json(n_days=0):
    # Get data
    data = load_data(n_days)

    return jsonify(data)

@app.route('/')
@app.route('/<int:n_days>')
def hello_world(n_days=0):
    print("n_days:",n_days)
    # Get data
    data = load_data(n_days)

    # Crunch numbers
    feed_text = text_data(data)
    feed_pie = pie_data(data)
    feed_map = map_data(data)
    feed_numbers = numbers_data(data)

    return render_template('index.html', **feed_text, **feed_pie, **feed_map, **feed_numbers)