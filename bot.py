import json
import re

def get_input_file():
	# pass the absolute path of file or just the name if in same directory
	path = take_input("Please provide the path of the input file")

	with open(path, 'r') as file_data:
		input_data = json.loads(file_data.read())

	# call the conversation interpreter function
	eval("{0}({1})".format(scrub(input_data["function"]), input_data["questions"]))