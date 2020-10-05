# Foreign
from multiprocessing import Process
import logging
from tqdm import tqdm

# Local dependencies
from testsuite.config import DTYPE, FAIL_MAX, io_block
from testsuite.solution import solution
from testsuite.metrics import Results, Timer, get_solution_length, get_illegal


logging.basicConfig(
	filename="warnings.log",
	filemode='w',
	level=logging.WARNING
)


def test(cases: list, dtype: type):

	for i, case in tqdm(enumerate(cases), total=len(cases)):
		# Unpack case values
		args, answer = case
		# Increment
		Results.answered.value += 1
		# Predefine input
		response = None
		try:
			# Employ input and output blocker
			with io_block():
				# Run solution from solution.py
				response = solution(*args)
		except Exception as e:
			logging.warning(e, case, response)
		try:
			# Validate response using expected type
			if (dtype(answer) == dtype(response)) & (response is not None):
				continue

			# If answers don't match, insert case index and response
			Results.case_index[Results.fail_count.value] = i
			Results.response[Results.fail_count.value] = response
			Results.fail_count.value += 1
		except TypeError:
			logging.warning(TypeError, case, response, type(response))
			# If error returning proper type, include in missed cases
			Results.case_index[Results.fail_count.value] = i
			Results.response[Results.fail_count.value] = response
			Results.fail_count.value += 1

		# Break at fail violation
		if Results.fail_count.value >= FAIL_MAX:
			print(f"You've exceeded the failed case limit: {FAIL_MAX}")
			break

	# Stop timer
	with Timer.running.get_lock():
		Timer.running.value = False


def run(cases: list, ctype: type):
	# Initialize shared variables
	Results.initialize(ctype)
	dtype = DTYPE[ctype]

	test_process = Process(target=test, args=(cases, dtype))
	# Start test
	test_process.start()
	# Start timer
	Timer.start(test_process)

	return score(n=len(cases))


def score(n: int) -> dict:
	answered = Results.answered.value
	correct = answered - Results.fail_count.value
	# Prevent zero division error
	if answered == 0:
		answered = 1
		correct = 0
	fail_index = [i for i in Results.case_index if i >= 0]
	fail_responses = [x for x, i in zip(Results.response, fail_index) if i >= 0]

	score_dict = {
		"answered": answered,
		"failed": Results.fail_count.value,
		"total": n,
		"fail_index": fail_index,
		"fail_responses": fail_responses,
		"correct": correct,
		"percent": round(correct/answered*100, 2),
		"length": get_solution_length(),
		"violations": get_illegal(),
		"runtime": round(Timer.runtime, 6),
		"iter_per_s": round(answered/Timer.runtime, 4)
	}
	return score_dict

