import io
import base64

from flask import Flask
from flask import render_template
import numpy as np
import matplotlib.pyplot as plt

from src.getdata import get_numbers

app = Flask(__name__)

@app.route('/plot')
def build_plot():

	img = io.BytesIO()

	y = [1,2,3,4,5]
	x = [0,2,1,3,4]
	plt.plot(x,y)
	plt.savefig(img, format='png')
	img.seek(0)

	plot_url = base64.b64encode(img.getvalue()).decode()

	# return '<img src="data:image/png;base64,{}">'.format(plot_url)
	return render_template('index.html', plot=plot_url)

@app.route('/')
def hello_world():
	# Get data
	data = get_numbers()
	
	# Crunch numbers
	n_prostitues = np.sum([[prostitue for prostitue in data["prostitues"][region].values()] \
		for region in data["prostitues"]])

	n_benevoles = np.sum([region for region in data["benevoles"].values()])

	n_sensibilises = np.sum([region for region in data["sensibilises"].values()])

	# Return template filled with data
	feed = {
		"n_prostitues": n_prostitues,
		"n_benevoles": n_benevoles,
		"n_sensibilises": n_sensibilises
	}

	return render_template('index.html', **feed)