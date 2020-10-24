from gentools.wrap import binning
import random


# Text to print for each bin
def printable():
	i = 0
	while True:
		yield f"Generating sample {i}"
		i += 1


# Random seeds for each bin's generation
seeds = [101, 392, 81]
# Shift random values
biases = [2, 3, 5, 7]


@binning(m=0, M=10, n=10000, bins=5, seed=seeds, stdout=printable(), bias=biases)
# Generate 5 sub-samples in the range 10^0 to
# 10^10 and merge them so they sum to 1000
def generator(a, b, n, seed=1, bias=0, stdout="..."):
	"""
	Generates n random values in the range [a, b) and whether the number it is even.

	:param a: Lower bound for generating values
	:param b: Upper bound for generating values
	:param n: Number of values to generate
	:param seed: Random generator seed
	:param stdout: Announcement to print to terminal when generating a bin
	:param bias: Shifts the generated value
	:return: List of random values in range [a, b)
	"""
	random.seed(seed)
	print(stdout)
	print(f"\tSeed: {seed}")
	print(f"\tBias: {bias}")
	return [([x+bias], (x + bias) % 2 == 0) for x in random.choices(range(int(a), int(b)), k=n)]


cases = generator()
