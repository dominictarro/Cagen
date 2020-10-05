"""

Acquire settings, format strings, io, establish constants

"""

from ctypes import c_bool, c_int, c_wchar_p, c_float
from typing import Any, List, Union, Tuple, Dict
from contextlib import contextmanager
from datetime import datetime
import logging
import json
import sys


logging.basicConfig(
	filename="warnings.log",
	filemode='w',
	level=logging.WARNING
)


# Read in default settings
with open("./resources/default.json", 'r') as infile:
	globals().update(json.load(infile))

# Read in available tests
with open("./resources/test_attr.json", 'r') as infile:
	TEST_ATTR = json.load(infile)


RESPONSE_CTYPE = {
	"bool": c_bool,
	"int": c_int,
	"float": c_float,
	"str": c_wchar_p
}
DTYPE = {
	c_bool: bool,
	c_int: int,
	c_float: float,
	c_wchar_p: str
}


class colors:
	HEADER = '\033[95m'
	OKBLUE = '\033[94m'
	OKGREEN = '\033[92m'
	WARNING = '\033[93m'
	FAIL = '\033[91m'
	ENDC = '\033[0m'
	BOLD = '\033[1m'
	UNDERLINE = '\033[4m'


# noinspection PyUnboundLocalVariable
INTRO = INTRO.format(color=colors.OKGREEN, header=colors.HEADER, clear=colors.ENDC)


# Suppress attempts to take input
@contextmanager
def io_block(placeholder=None):
	stdin, sys.stdin = sys.stdin, placeholder
	stdout, sys.stdout = sys.stdout, open(DUMP, 'a')
	try:
		yield placeholder
	except RuntimeError:
		sys.stdin = stdin
		sys.stdout = stdout
		logging.warning(RuntimeError, stdin, stdout, sys.stdin, sys.stdout)
	finally:
		sys.stdin = stdin
		sys.stdout = stdout


def get_test_string(t_id: str) -> str:
	"""
	Format the test's attributes for terminal output

	:param t_id:    dictionary key for test
	:return:        formatted string of test's attributes
	"""
	difficulty = TEST_ATTR[t_id]["difficulty"]
	size = TEST_ATTR[t_id]["size"]
	args = TEST_ATTR[t_id]["args"]

	sep = " " * (SPACE - len(t_id))
	string = f"""{colors.OKBLUE}{t_id}{colors.ENDC}: {sep}Number of Cases: {size}
{" " * (SPACE + 2)}Argument Range: {args}
{" " * (SPACE + 2)}Difficulty: {difficulty}\n{'-' * 2 * SPACE}
"""
	return string


def get_test(t_id: str) -> Union[Tuple[Union[List[Tuple[Any, Any]]], type], None]:
	"""
	Return
	([
		(args, answer),
		(args, answer),
		...
	], ctype)
	or None

	:param t_id:    dictionary key for test
	:return:        test and answer data type, or none type if not a valid test
	"""

	try:
		with open(TEST_ATTR[t_id]["filename"], 'r') as infile:
			# Must send answer type to build response array
			ctype_id = TEST_ATTR[t_id]["response-type"]
			return json.load(infile), RESPONSE_CTYPE[ctype_id]
	except KeyError:
		print("'{}' is not a supported test.".format(t_id))

		return None
	except Exception as e:
		logging.warning(e, t_id)
		print(f"There was an unexpected error. '{t_id}' may be unavailable or corrupted.")


def save_missed(fail_index: list, responses: list,
				cases: Union[List[Tuple[Any, Any]]],
				t_id: str):
	"""

	:param fail_index:  array of indices for all missed cases
	:param responses:   array of responses for all missed cases
	:param cases:       array of all cases
	:param t_id:        test name to record failed cases
	"""
	missed = {f"case_{i}": {
		'argument': cases[i][0],
		'answer': cases[i][1],
		'response': responses[k]
	}
		for k, i in enumerate(fail_index)}

	with open(f"./results/failed-cases-{t_id}-{datetime.utcnow()}.json", 'w') as f:
		json.dump(missed, f)


def display_score(score: Dict[str, Any]):
	output = f"""\
Code Length:    {score['length']} characters
Answered:       {score['answered']}/{score['total']}
Correct:        {score['correct']}/{score['answered']}, {score['percent']}
Runtime:        {score['runtime']} seconds
Rate:           {score['iter_per_s']} iterations per second

Violations:     {colors.FAIL}{score["violations"]}{colors.ENDC}\
"""
	print(output)


instructions = f"""Enter the id of the test you would like to take:
{colors.OKBLUE}0{colors.ENDC}: {" "*(SPACE - 1)}exit\n
{ENDL.join([get_test_string(t_id) for t_id in TEST_ATTR.keys() if TEST_ATTR[t_id]['open']])}"""

