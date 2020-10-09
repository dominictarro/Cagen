"""

General functions, classes, and variables that are consistent and miscellaneous

"""
from contextlib import contextmanager
import json
import sys
import re


# Input/output redirection during test
OUTPUTS_FILE = "./io/io.txt"


class Colors:
	"""
	Text formatting for terminal output
	"""
	HEADER = '\033[95m'
	OKBLUE = '\033[94m'
	OKGREEN = '\033[92m'
	WARNING = '\033[93m'
	FAIL = '\033[91m'
	ENDC = '\033[0m'
	BOLD = '\033[1m'
	UNDERLINE = '\033[4m'


@contextmanager
def io_block():
	"""
	Block print, input, sys.stdin/stdout statements

	:return:
	"""
	# Temporarily set input/output to dump into a file
	# Input method will return None, however runtime error handling should catch it
	stdout = sys.stdout
	sys.stdout = open(OUTPUTS_FILE, 'w')
	stdin = input
	globals()["__builtins__"]["input"] = print
	try:
		yield None
	finally:
		# Return io methods to their respective variables
		sys.stdout.close()
		sys.stdout = stdout
		globals()["__builtins__"]["input"] = stdin


def get_solution_stripped() -> str:
	"""
	Read solution.py into variable and strip it of comments and docstrings

	:return:
	"""
	# Comments up through the end of line
	COMMENT = r"#.*?\n"
	# Docstrings up through the end of its final line
	DOCSTRING = r"('){3}(.*?)('){3}\n"
	DOCSTRING_DOUBLE = r'("){3}(.*?)("){3}'
	PATTERN = f"{COMMENT}|{DOCSTRING}|{DOCSTRING_DOUBLE}"
	regex = re.compile(PATTERN, flags=re.DOTALL)
	with open("solution.py", 'r') as infile:
		solution = infile.read()
		solution = regex.sub('', solution)
		solution = solution.strip()
	return solution


def get_solution_length() -> int:
	"""

	:return: Number of characters used in solution
	"""
	return len(get_solution_stripped())


def get_violations() -> list:
	"""
	Return a list of all violations in solution.py file according the regex patterns in ./resources/violation_regex.json
	:return:
	"""
	with open("./resources/violation_regex.json", 'r') as infile:
		VIOLATION_REGEX = json.load(infile)
	regex = re.compile(f"{'|'.join(VIOLATION_REGEX)}")
	solution = get_solution_stripped()

	return [x.group() for x in regex.finditer(solution)]


def display_score(score: dict):
	"""
	Print test results to terminal

	:param score: scoring dictionary returned from Metrics.Results.score(*args)
	:return:
	"""
	output = f"""\
Code Length:    {score['length']} characters
Answered:       {score['answered']}/{score['total']}
Correct:        {score['correct']}/{score['answered']}, {score['percent']}%
Runtime:        {score['runtime']} seconds
Rate:           {score['iter_per_s']} iterations per second

Violations:     {Colors.FAIL}{score["violations"]}{Colors.ENDC}
Errors:         {len(score['errors'])}
	"""
	print(output)


def save_missed(score: dict):
	"""
	Store missed cases in file for user's review

	:param score:
	:return:
	"""
	with open("./results/failed_cases.json", 'w') as outfile:
		json.dump(score["fails"], outfile)

	with open("./results/errors.json", 'w') as outfile:
		json.dump(score["errors"], outfile)
