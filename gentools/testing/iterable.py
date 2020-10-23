from gentools.wrap import binning
import random


# Random seeds for each bin's generation
seeds = [101, 392, 81]
# Shift random values
bias = [random.randint(-5, 6) for _ in range(4)]


# Text to print for each bin
def printable():
	i = 0
	while True:
		yield f"Generating sample {i}"
		i += 1


@binning(m=0, M=10, n=10000, k=5, seed=seeds, stdout=printable(), bias=bias)
# Generate 5 sub-samples in the range 10^0 to
# 10^10 and merge them so they sum to 1000
def generator(a, b, n, seed=1, bias=0, stdout="..."):
	random.seed(seed)
	print(stdout)
	print(f"\tSeed: {seed}")
	print(f"\tBias: {bias}")
	return [([x+bias], (x + bias) % 2 == 0) for x in random.choices(range(int(a), int(b)), k=n)]


cases = generator()

