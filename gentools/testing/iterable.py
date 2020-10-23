from gentools.wrap import binning
import random

k = 4
# Random seeds for each bin's generation
seeds = [101, 392, 81]
# Text to print for each bin
printable = (f"Generating sample {i}" for i in range(k))


@binning(m=0, M=10, n=10000, k=k, seed=seeds, stdout=printable)
# Generate 5 sub-samples in the range 10^0 to
# 10^10 and merge them so they sum to 1000
def generator(a, b, n, seed=1, stdout="..."):
	random.seed(seed)
	print(f"Seed: {seed}")
	print("\t", stdout)
	return [([x], x % 2 == 0) for x in random.choices(range(int(a), int(b)), k=n)]


cases = generator()

