# Foreign
from multiprocessing import Process, Value, Array
from typing import Any
import time
import sys
import re

# Local dependencies
from testsuite.config import FAIL_MAX, RUNTIME_MAX, c_int, c_bool


class Results:
	# Shared memory objects for recording test outcomes
	answered = Value(c_int, 0)
	fail_count = Value(c_int, 0)
	case_index = list()
	response = list()

	@classmethod
	def initialize(cls, ctype: type):
		"""

		:param ctype:   Response data type to initialize missed values with
		:return:
		"""

		# C arrays must be pre-built to the worst case length
		# Use these to record failed cases
		cls.case_index = Array(c_int, FAIL_MAX)
		cls.response = Array(ctype, FAIL_MAX)


class Timer:
	begin = Value(c_bool, False)
	limit = RUNTIME_MAX
	runtime = 0.0001
	running = Value(c_bool, True)
	_DELAY = 0.0001

	@classmethod
	def start(cls, process: Process):
		t0 = time.time()
		cls.begin = True
		while (cls.runtime < cls.limit) & cls.running.value:
			time.sleep(cls._DELAY)
			# Check if shared value is true

			if (cls.running.value == False) | (Results.fail_count.value >= FAIL_MAX):
				# If true, test has been completed. Break
				break

			# Increment elapsed time
			cls.runtime = time.time() - t0

		# After passing time limit, kill thread
		if cls.running.value:
			print(f"You've exceeded the time limit: {cls.limit} seconds")
			process.terminate()


def get_solution_stripped() -> str:
	# Strip comments and docstrings
	comment = f'#.*?\n'
	docstring = f"'''~.*?'''"
	docstring_double = f'"""~.*?"""'
	pattern = f"{comment}|{docstring}|{docstring_double}"
	regex = re.compile(pattern, flags=re.DOTALL)
	with open("solution.py", 'r') as infile:
		solution = infile.read()
		solution = regex.sub('', solution)
	return solution


def get_solution_length() -> int:
	return len(get_solution_stripped())


def get_illegal():
	# Catch import statements, input, print, and solution call statements
	# Don't touch, optional if function demands *args -> "(solution\((?!\*args).*?\))"
	VIOLATION_REGEX = [
		"import.*",
		"input.*",
		"print.*",
		"(solution\([\"\'0-9].*?\))"
	]
	regex = re.compile(f"{'|'.join(VIOLATION_REGEX)}")
	solution = get_solution_stripped()
	# Find all occurrences of the violations
	violations = [x for x in regex.finditer(solution)]
	# Return strings of the violations
	return [solution[x.start():x.end()] for x in violations]
