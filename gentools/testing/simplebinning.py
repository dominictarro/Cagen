from gentools.wrap import binning
import random


# Generate 5 sub-samples in the range 10^0 to
# 10^10 and merge them so they sum to 1000 cases
@binning(m=0, M=10, n=100000, bins=10)
def generator(a, b, n):
	"""
	Generates n random values in the range [a, b)

	:param a: Lower bound for generating values
	:param b: Upper bound for generating values
	:param n: Number of values to generate
	:return: List of random values in range [a, b)
	"""
	return random.choices(range(int(a), int(b)), k=n)


cases = generator()
