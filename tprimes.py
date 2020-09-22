import random
import numpy as np
import math
import json

def primeSieveSquared(n):
	# Returns a list of prime numbers calculated using the Sieve of Eratosthenes algorithm
	sieve = [True] * n
	# Zero and one are not prime numbers, can skip for simplicity
	sieve[0] = False
	sieve[1] = False
	for i in range(2, int(n**0.5) + 1):
		pointer = i * 2
		while pointer < n:
			sieve[pointer] = False
			pointer += i

	# compile the list of primes
	return [i**2 for i, p in enumerate(sieve) if p]


def frequency(sample: list) -> float:
	return sum([x[1] for x in sample])/len(sample)


def generate(a: (int, float),
             b: (int, float),
             n: (int, float),
             r: float,
             rf: float,
             balanced: bool = False,
             j: (str, int) = "auto") -> list:
	"""
	:param a: lower bound for 10**e exponent
	:param b: upper bound for 10** exponent
	:param n: number of cases in sample
	:param r: percent True (1)
	:param r: percent of Falses are squares of odd numbers
	:param balanced: to random sample evenly for any section of 10**k for k in range a, b
	:param j: How many groups to break sub samples into when balancing

	A T-Prime will always be the square of a prime number
	4: [1,2,4]
	9: [1,3,9]
	25: [1,5,25]
	etc.

	Process:
		1. Generate primes up to the square root of the ceiling
		2. Square them
		3. Compute how many True cases to include in test
		4. Take a sample
		5. Generate non T-Prime integers to complete the test of size n
		6. Shuffle them (random assortment)
		7. Save
	"""
	if balanced:
		# See proof for mathematical explanation
		# Generate random subsets at the given frequency for each exponent
		if j == "auto":
			j = int(b-a)
		assert isinstance(j, int)
		# Exponent difference is equal to the range / number of groups
		d = (b-a)/j
		# Initialize average freq. at the expected rate
		mu_h = r
		subsize = n/j
		cases = []
		freq = []
		# Progress in leaps of d
		for k in range(1, j+1):
			# Generate a sample and include into cases
			# The min will only kick in situations where the
			subset = generate(a+(k-1)*d, a+k*d, n=subsize, r=mu_h, rf=rf)
			cases.extend(subset)
			freq.append(frequency(subset))
			# Update future average
			if k < j:
				mu_h = r/(1-k/j)-sum(freq)/(j-k)
		random.shuffle(cases)
		return cases
	else:
		# Recast n as int here for sample balancing. Reduces rounding error so samples sum to n
		n = int(n)
		A = int(10**a)
		B = int(10**b)
		cases = []
		valids = [x for x in primeSieveSquared(int(B**0.5)) if x >= A]

		m = len(valids)
		if n*r <= m:
			valid_count = int(n*r)
		else:
			valid_count = m

		[cases.append((x, 1)) for x in random.sample(valids, valid_count)]
		# Conventional numbers
		invalids_sample = set([x for x in random.sample(range(A, B), int((1-rf)*(n-valid_count)))])
		# Odd squares
		invalids_sample.union(set([x**2 for x in random.sample(range(int(A**0.5), int(B**0.5)), int((rf)*(n-valid_count))) if x%2 != 0]))
		invalids_sample -= set(valids)

		# Replenish missing from subtracting set intersection
		while len(invalids_sample) < n-valid_count:
			x = random.randint(A, B)
			while (x in valids) | (x in invalids_sample):
				x = random.randint(A, B)
			invalids_sample.add(x)

		for y in invalids_sample: cases.append((y, 0))

		random.shuffle(cases)

		return cases


def gen_range(a: int, b: int, n: int):
	for N in range(a, b+1):
		r = random.uniform(0.33, 0.67)
		rf = random.uniform(0.33, 0.67)
		sample = generate(0, N, n=n, r=r, rf=rf)
		with open(f"/Users/dominictarro/Desktop/Code/Python/Discord Help/tests-10^{N}.json", 'w') as f:
			json.dump(sample, f)


def make_monsters():
	r = random.uniform(0.33, 0.67)
	rf = random.uniform(0.33, 0.67)
	sample = generate(14, 15, n=10000, r=r, rf=rf)

	with open("/Users/dominictarro/Desktop/Code/Python/Discord Help/test-here-be-monsters.json", 'w') as f:
		json.dump(sample, f)


if __name__ == "__main__":
	gen_range(6, 10, n=2000)

