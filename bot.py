import json
import re

def gather_input():

	path = take_input("Please provide the path of input file")

	with open(path, 'r') as file_data:
		input_data = json.loads(file_data.read())

	# call the conversation function
	sample_text_function(input_data["questions"])

def sample_text_function(question_matrix):
	
	localVar = {}

	for ques in question_matrix:
		if ques.get('instruction'):
			unpack_instruction(ques, localVar)
		elif ques.get("text"):
			list_instance = re.findall('.*(\[.*?\]).*', ques["var"])
			if list_instance:
				temp_var = get_var_input(ques, localVar)
				list_eval = "{0}.append('{1}')".format(ques["var"].split("[")[0], temp_var)
				eval(list_eval, localVar)
			else:
				localVar[ques["var"]] = get_var_input(ques, localVar)
		elif ques.get("calculated_variable"):
			localVar[ques["var"]] = eval(ques["formula"], localVar)


def get_var_input(data, localVar):
	
	var = data["var"]

	if data.get("conditions"):
		conditions = data.get("conditions")
		and_cond = ["(" + " and ".join(row) + ")" for row in conditions]
		cond = " or ".join(and_cond)

		while eval(cond, localVar):
			localVar[var] = take_input(data["text"], data.get("options"))
	else:
		# take input
		temp_var = take_input(data["text"], data.get("options"))

	return localVar.get(var) or temp_var

def unpack_instruction(data, localVar):

	output = data["instruction"]

	if data.get("list_var") and data.get("list_length"):
		for i in range(0, int(data["list_length"])):
			localVar["i"] = i
			args = [eval(x, localVar) for x in data["instruction_var"]]
			output = data["instruction"] % tuple(args)
			print(output)

		return
	elif data.get("instruction_var"):
		args = [localVar[d] for d in data["instruction_var"]]
		output = output % tuple(args)

	print(output)


def take_input(text, options=[]):

	inp, opt = "", ""
	if options:
		opt = "(" + " / ".join(options) + ")"

	# python 2 & 3 based input
	try:
		inp =  raw_input("{0} {1}: ".format(text, opt))
	except NameError:
		inp = input("{0} {1}: ".format(text, opt))

	if options and inp not in options:
		print("Invalid option. Please select one of these {0}".format(opt))
		inp = take_input(text, options)

	return inp

if __name__ == "__main__":
	gather_input()