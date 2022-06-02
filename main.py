#!/usr/bin/env python3
import time
import sys
import os

current_condition_operation = 'AND'
# Each item in list is a wait parameter formatted as follows": {"operation":"AND", "type":"directory-available", "arguments":[]}
wait_conditions = []

check_time = 5


def add_wait_parameter(args, index):  # returns parser continuation index
	global current_condition_operation
	global check_time
	wait_arguments = []
	wait_type = args[index][2:]
	return_index = index

	if wait_type == "and":
		current_condition_operation = "AND"
		return_index = index + 1

	elif wait_type == "nand":
		current_condition_operation = "NAND"
		return_index = index + 1

	elif wait_type == "directory-available":
		wait_arguments.append(args[index + 1])
		return_index = index + 2
		wait_conditions.append(
			{"operation": current_condition_operation, "type": wait_type, "arguments": wait_arguments})

	elif wait_type == "check-time":
		try:
			check_time = int(args[index + 1])
			return_index = index+2
		except ValueError:
			print("Please specify a valid number for --check-time")
			sys.exit(1)

	else:
		print("Unknown argument: " + str(args[index]))
		sys.exit(1)

	return return_index


def parse_arguments(args):
	current_index = 0
	while True:
		if len(args[current_index]) > 2 and args[current_index][:2] == "--":
			current_index = add_wait_parameter(args, current_index)
		else:
			current_index += 1
		if current_index >= len(args):
			break


def wait():
	global wait_conditions
	global check_time
	all_conditions_met = False
	while True:
		for condition in wait_conditions:
			if condition["type"] == "directory-available":
				if os.path.isdir(condition["arguments"][0]):
					if condition["operation"] == "NAND":
						all_conditions_met = False
					else:

						all_conditions_met = True
				else:
					if condition["operation"] == "NAND":
						all_conditions_met = True
					else:
						all_conditions_met = False
		if all_conditions_met:
			quit()
		time.sleep(check_time)


def main():
	parse_arguments(sys.argv)
	print(sys.argv)
	print(wait_conditions)
	print(check_time)
	wait()


if __name__ == "__main__":
	main()
