import io
import base64

from flask import Flask
from flask import render_template
from flask import Response
from flask import jsonify
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas
from matplotlib.figure import Figure

from src.getdata import get_numbers
from src.crunch_numbers import text_data

app = Flask(__name__)


@app.route('/images/plot.png')
def plot_png():
    # Create figure
    fig = Figure()
    axis = fig.add_subplot(1, 1, 1)
    xs = range(100)
    ys = np.random.randint(1, 50, size=len(xs))
    axis.plot(xs, ys)

    # Convert figure to bytes
    output = io.BytesIO()
    FigureCanvas(fig).print_png(output)

    # Returns image
    return Response(output.getvalue(), mimetype='image/png')

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

    return render_template('index.html', **feed_text)