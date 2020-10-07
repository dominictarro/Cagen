"""

Measurement classes and methods to be accessed by the testing daemon and main process

"""

# Foreign dependencies
from ctypes import c_float, c_int, c_bool, c_wchar_p
from multiprocessing import Value, Array
from contextlib import contextmanager
from typing import Any
import time

# Local dependencies
from unit.utils import get_solution_length, get_violations
from unit.config import ERROR_TO_ID, ID_TO_ERROR


class Timer:

	def __init__(self):
		# Runtime in nanoseconds
		self._runtime = Value(c_float, 0.0)

	@property
	def runtime(self):
		"""

		:return: Runtime in seconds
		"""
		with self._runtime.get_lock():
			return self._runtime.value / 10**9

	@contextmanager
	def clock(self):
		"""
		Measures time from call to finish in nanoseconds

		:return:
		"""
		t0 = time.time_ns()
		try:
			yield None
		finally:
			self._runtime.value += time.time_ns() - t0


class Results:
	# Translation dict for if the response's data type is not the data type the test expects
	_type_default_dict = {
		int: -1,
		float: -1.0,
		str: "-1",
		bool: -1
	}

	def __init__(self, ctype: type, dtype: type, fail_max: int):
		"""

		:param ctype:       Data type that results will be from ctypes library
		:param dtype:       Data type that results will be in Python
		:param fail_max:    Maximum tolerance for failed cases
		"""
		self.dtype = dtype
		self.default_type_value = Value(ctype, self._type_default_dict[dtype])

		# Count
		self.answered = Value(c_int, 0)
		self.fail_count = Value(c_int, 0)
		# Case list indexes for cases where output did not equal answer
		self.failed_case_indices = Array(c_int, [-1]*fail_max)
		# Responses for respective failed cases
		self.failed_case_responses = Array(ctype, fail_max)

		# Count
		self.error_count = Value(c_int, 0)
		# Case list indexes for cases where solution or output yielded an error
		self.error_case_indices = Array(c_int, [-1]*fail_max)
		# Respective error types (encoded as integer—see config for encoding dict)
		self.errors = Array(c_int, [-1]*fail_max)

	@contextmanager
	def get_locks(self, *args):
		"""
		Locks shared memory objects for editing

		:param args: Variables that need to acquire a lock
		:return:
		"""
		try:
			for attr in args:
				attr.acquire()
			yield None
		finally:
			for attr in args:
				attr.release()

	def add_error(self, i: int, error: Exception):
		"""
		Insert an erroneous case into the error lists

		:param i:       Case index
		:param error:   Error raised
		:return:
		"""
		with self.get_locks(self.error_case_indices,
		                    self.errors,
		                    self.error_count):
			self.error_case_indices[self.error_count.value] = i
			self.errors[self.error_count.value] = ERROR_TO_ID[error.__class__]
			self.error_count.value += 1

	def add_fail(self, i: int, response: Any):
		"""
		Insert a failed case into the fail lists

		:param i:           Case index
		:param response:    Response that failed
		:return:
		"""
		with self.get_locks(self.failed_case_responses,
		                    self.fail_count,
		                    self.failed_case_indices):
			if isinstance(response, self.dtype):
				# If response is of the proper type, use response
				self.failed_case_responses[self.fail_count.value] = response
			else:
				# If response is not the proper type, use the default value for that type
				self.failed_case_responses[self.fail_count.value] = self.default_type_value.value
			self.failed_case_indices[self.fail_count.value] = i
			self.fail_count.value += 1

	def get_failed(self, cases: list) -> iter:
		"""
		Generator for dicts yielding each failed case's index, arguments, answer. and response

		:param cases:   Test case list
		:return:
		"""
		for i, response in zip(self.failed_case_indices, self.failed_case_responses):
			# Default for index is -1
			if i < 0:
				break
			yield {"index": i, "arguments": cases[i][0], "answer": cases[i][1], "response": response}

	def get_errors(self, cases: list) -> iter:
		"""
		Generator for dicts yielding each erroneous case's index, arguments. and error type

		:param cases:   Test case list
		:return:
		"""
		for i, err in zip(self.error_case_indices, self.errors):
			# Default for list is -1
			if i < 0:
				break
			yield {"index": i, "arguments": cases[i][0], "error": ID_TO_ERROR[err]}

	def score(self, cases: list, timer: Timer) -> dict:
		"""
		Using test cases and the testing timer, produce a dictionary of performance results

		:param cases:   Test case list
		:param timer:   Timer object
		:return:        Dictionary of performance scores and misc. metrics
		"""
		failed = list(self.get_failed(cases=cases))
		errors = list(self.get_errors(cases=cases))
		answered = self.answered.value
		correct = answered - len(failed)

		return {
			"answered": answered,
			"total": len(cases),
			"correct": correct,
			"fails": failed,
			"percent": round(correct/answered*100, 2),
			"errors": errors,
			"length": get_solution_length(),
			"violations": get_violations(),
			"runtime": round(timer.runtime, 6),
			"iter_per_s": round(answered/timer.runtime, 4)
		}
