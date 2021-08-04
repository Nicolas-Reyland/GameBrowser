# GameBrowser - file handler
import os
import json

def load_file(path):
	return json.load(open(path, 'r'))

def save_file(path, data):
	if not path.endswith('.json'): path += '.json'
	json.dump(data, open(path, 'w'))

