"""

Configuration functions, classes, and variables that are used for setting up the test

"""
# Foreign dependencies
from ctypes import c_bool, c_int, c_wchar_p, c_float
from typing import Any, List, Union, Tuple
import json

# Local dependencies
from challenge.utils import Colors


# Read in default settings
with open("./resources/default.json", 'r') as infile:
	"""
	default.json should include the following variables:
		FAIL_MAX: integer
		RUNTIME_MAX: numeric
		ENDL: special character
		SPACE: integer
		INTRO: string
		EXIT: string
	"""
	defaults = json.load(infile)
	FAIL_MAX = defaults["FAIL_MAX"]
	RUNTIME_MAX = defaults["RUNTIME_MAX"]
	ENDL = defaults["ENDL"]
	SPACE = defaults["SPACE"]
	INTRO = defaults["INTRO"]
	EXIT = defaults["EXIT"]

# Read in available tests
with open("./resources/test_attr.json", 'r') as infile:
	TEST_ATTR = json.load(infile)


# Test response type to ctype
RESPONSE_CTYPE = {
	"bool": c_int,
	"int": c_int,
	"float": c_float,
	"str": c_wchar_p
}
# Test response type to type
RESPONSE_DTYPE = {
	"bool": int,
	"int": int,
	"float": float,
	"str": str
}
# For storage of runtime errors in ctype array
# Encode as integer
ERROR_TO_ID = {

}
ID_TO_ERROR = {

}
for i, error in enumerate(Exception.__subclasses__()):
	ERROR_TO_ID[error] = i
	ID_TO_ERROR[i] = str(error)


INTRO = globals()["INTRO"].format(color=Colors.OKGREEN, header=Colors.HEADER, clear=Colors.ENDC)


def get_test_param_string(t_id: str) -> str:
	"""
	Format the test's attributes for terminal output

	:param t_id:    Dictionary key for test
	:return:        Formatted string
	"""
	difficulty = TEST_ATTR[t_id]["difficulty"]
	size = TEST_ATTR[t_id]["size"]
	args = TEST_ATTR[t_id]["args"]

	sep = " " * (globals()["SPACE"] - len(t_id))
	string = f"""{Colors.OKBLUE}{t_id}{Colors.ENDC}: {sep}Number of Cases: {size}
{" " * (globals()["SPACE"] + 2)}Argument Range: {args}
{" " * (globals()["SPACE"] + 2)}Difficulty: {difficulty}\n{'-' * 2 * globals()["SPACE"]}"""
	return string


def get_test(t_id: str) -> Union[Tuple[Union[List[Tuple[Any, Any]]], type], None]:
	"""
	Returns the test cases of the given test id formatted
	[
		[(args), answer],
		[(args), answer],
		...
	]
	and the ctype to be used

	:param t_id:    Dictionary key for test
	:return:        Test and answer data type, or none type if not a valid test
	"""
	try:
		with open(TEST_ATTR[t_id]["filename"], 'r') as infile:
			# Must send answer type to build response array
			return json.load(infile), TEST_ATTR[t_id]["response-type"]
	except KeyError:
		print("'{}' is not a supported test.".format(t_id))
		return None


instructions = f"""Enter the id of the test you would like to take:
{Colors.OKBLUE}{EXIT}{Colors.ENDC}: {" "*(SPACE - 1)}exit\n
{ENDL.join([get_test_param_string(t_id) for t_id in TEST_ATTR.keys() if TEST_ATTR[t_id]['open']])}"""
