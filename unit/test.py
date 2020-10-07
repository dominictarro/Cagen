# Foreign dependencies
from multiprocessing import Process
from tqdm import tqdm
import logging
import os

# Local dependencies
from unit.config import FAIL_MAX, RUNTIME_MAX, RESPONSE_CTYPE, RESPONSE_DTYPE
from unit.metrics import Timer, Results
from unit.solution import solution
from unit.utils import io_block


logging.basicConfig(filename="./results/failed-eval.log", filemode='w', level=logging.WARNING)


def test(cases: list, results: Results, timer: Timer, dtype: type):
	# Block io
	with io_block():
		for i, case in tqdm(enumerate(cases), total=len(cases)):
			args, answer = case
			results.answered.value += 1
			try:
				# Clock solution runtime
				with timer.clock():
					response = solution(*args)
				if dtype(response) != dtype(answer):
					try:
						results.add_fail(i=i, response=None)
					except Exception as e:
						logging.warning(e)
			except Exception as e:
				# If any error during solution or response check, include it into results for user's review
				results.add_error(i=i, error=e)
				results.add_fail(i=i, response=None)

			# Break upon overcoming the fail limit
			if results.fail_count.value >= FAIL_MAX:
				break


def run(cases: list, type_id: str) -> (Results, Timer):
	dtype, ctype = RESPONSE_DTYPE[type_id], RESPONSE_CTYPE[type_id]

	results = Results(ctype=ctype, dtype=dtype, fail_max=FAIL_MAX)
	timer = Timer()

	test_proc = Process(target=test, args=(cases, results, timer, dtype))
	test_proc.start()
	test_proc.join(timeout=RUNTIME_MAX)

	if test_proc.is_alive():
		test_proc.terminate()

	return results, timer

