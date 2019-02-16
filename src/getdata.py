import json

def get_numbers():
	with open("src/data.json", "r") as jfile:
		data = json.load(jfile)
	return data