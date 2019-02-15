from flask import Flask
from flask import render_template
import numpy as np

from src.getdata import get_numbers

app = Flask(__name__)

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