from flask import Flask
from flask import render_template
from flask import Response
from flask import jsonify
import numpy as np

from src.csv2json import filter_data
from src.gsheet2csv import main
from src.crunch_numbers import text_data, pie_data, map_data

app = Flask(__name__)

# @app.route('/data/json')
# def get_json():
#     # Get data
#     data = filter_data()

#     return jsonify(data)

@app.route('/')
def hello_world():
    # Get data
    # main()
    data = filter_data()

    # Crunch numbers
    feed_text = text_data(data)
    feed_pie = pie_data(data)
    feed_map = map_data(data)

    return render_template('index.html', **feed_text, **feed_pie, **feed_map)