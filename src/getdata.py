import json

def get_numbers():
	with open("src/example1.json", "r") as jfile:
		data = json.load(jfile)
	return data