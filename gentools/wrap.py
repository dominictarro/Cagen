from typing import Callable, Union, List
import random


def __has_next(generator: iter):
	try:
		return generator.__next__()
	except StopIteration:
		return False


def __kwarg_generator(**kwargs):
	"""
	Keyword argument generator that can handle lists/generators of varying lengths.

	:param kwargiters: Keyword arguments for iterables that should be zipped together for passing into a function,
						index by index
	:return:
	"""
	kwargs = {key: iter(kwargs[key]) for key in kwargs}
	while True:
		yield {
			key: x for key in kwargs if (x := __has_next(kwargs[key]))
		}


def __bin_generator(low: Union[int, float], high: Union[int, float], leap: Union[int, float], subn: int):
	"""

	:param low:     Lower bound of the generator
	:param high:    Upper bound of the generator
	:param leap:    Range for each bin
	:param subn:    Bin size
	:return: generator for bin inputs
	"""
	for i in range(low, high):
		yield 10**(leap*abs(i)), 10**(leap*abs(i+1)), subn


def binning(m: Union[int, float], M: Union[int, float], n: int, bins: int = 1, **kwargiters):
	"""
	Runs case generator using a binning strategy to more evenly distribute randomly sampled values within the range
	[10^m, 10^M).

	The first 3 arguments of the wrapped function are
	1. The lower bound (absolute, not exponent)
	2. The upper bound (absolute, not exponent)
	3. The sample size

	:param m: The lower exponent bound for 10^x
	:param M: The upper exponent bound for 10^x
	:param n: The number of cases to be generated
	:param bins: The number of bins (sub samples) to use when generating
	:param negatives: Whether generated values can be negative

	:param kwargiters: If your generator allows custom parameters for each sample, pass a list, generator, or tuple
					keyword arguments
	:return: wrapper function
	"""
	if not isinstance(bins, int):
		raise TypeError(f"Argument k must be an integer argument: {bins} given")
	elif not isinstance(m, (int, float)) or not isinstance(M, (int, float)):
		raise TypeError(f"Exponent bounds must be real numbers: m={m} and M={M} given")


	# Create a generator from the negative max to the positive max
	leap = (M-m) / bins
	bins_gen = __bin_generator(0, bins, leap=leap, subn=n // bins)

	# Turn custom bin lists into iterable
	kwarg_iterator = __kwarg_generator(**kwargiters)

	def wrap(f: Callable):
		def wrapper(*args, **kwargs):
			cases = []
			# Iterate through bins
			for a, b, subn in bins_gen:
				try:
					# Get next kwargs
					kwarg_iter = kwarg_iterator.__next__()
				except StopIteration:
					kwarg_iter = {}
				# Generate sub sample cases
				subcases = f(a, b, subn, *args, **kwargs, **kwarg_iter)
				# Update meta cases
				cases.extend(subcases)

			# Prune excess
			for _ in range(len(cases)-n):
				x = random.choice(cases)
				cases.remove(x)

			random.shuffle(cases)
			return cases

		return wrapper
	return wrap
