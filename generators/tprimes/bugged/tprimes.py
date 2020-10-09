import random
import numpy as np
import math
import json

def primeSieveSquared(n, low=0):
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
	return [i**2 for i, p in enumerate(sieve) if (i**2 > low) & p]


def frequency(sample: list) -> float:
	return sum([x[1] for x in sample])/len(sample)


def generate(a: (int, float), b: (int, float), n: (int, float), r: float,
			 rf: float, balanced: bool = False, j: (str, int) = "auto") -> list:
	"""
	:param a: lower bound for 10**e exponent
	:param b: upper bound for 10** exponent
	:param n: number of cases in sample
	:param r: percent True (1)
	:param rf: percent of Falses that are squares of odd numbers (edge)
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
		6. Shuffle them (random assortment) and return
	"""
	if balanced:
		"""
		Process:
			1. Determine groups (j number of them)
			2. Determine the exponent span of each group (d)
			3. Determine the sample size of each group (subsize)
			4. For group k, generate a subset with a True frequency of mu_h and a false-positive rate of rf
			5. Add subset to cases
			6. Get the True frequency for subset and add to freq
			7. Update mu_h for the next sample subset
		
		"""
		# See proof for mathematical explanation of mu_h
		# Generate random subsets at the given frequency for each exponent group

		if j == "auto":
			j = int(b-a)
		assert isinstance(j, int)
		# Exponent difference is equal to the range / number of groups
		d = (b-a)/j
		# Initialize average freq. at the expected overall frequency
		mu_h = r
		# Initialize average sample size at the approximated uniform
		n_h = n/j
		cases = []
		freq = []

		for k in range(1, j+1):

			# Generate a sample and include into cases
			subset = generate(a+(k-1)*d, a+k*d, n=n_h, r=mu_h, rf=rf)
			cases.extend(subset)

			freq.append(frequency(subset))
			# Update future average
			if k < j:
				# Min to prevent going over 1
				mu_h = min(r/(1-k/j)-sum(freq)/(j-k), 1)
				n_h = (n - len(cases))/(j-k)

		# If the sub samples were not enough
		if len(cases) < n:
			A, B = 10**a, 10**b
			valids = [x for x in primeSieveSquared(int(B ** 0.5), low=A)]

			while len(cases) < n:
				x = random.randint(A, B)
				new = (x, int(x in valids))
				while new in cases:
					x = random.randint(A, B)
					new = (x, int(x in valids))
				cases.append(new)

		random.shuffle(cases)
		return cases
	else:
		# Recast n as int here for sample balancing. Reduces rounding error so samples sum to n
		n = int(n)
		A = int(10**a)
		B = int(10**b)
		cases = []
		valids = [x for x in primeSieveSquared(int(B**0.5), low=A)]

		m = len(valids)
		if m >= n*r:
			valid_count = int(n*r)
		else:
			valid_count = m

		[cases.append((x, 1)) for x in random.sample(valids, valid_count-1)]

		# Conventional numbers
		invalids_sample = set([x for x in random.sample(range(A, B), int((1-rf)*(n-valid_count)))])
		# Odd squares (edge cases)
		invalids_sample.union(set([x**2 for x in random.sample(range(int(A**0.5), int(B**0.5)), int((rf)*(n-valid_count))) if x%2 != 0]))
		invalids_sample -= set(valids)

		# Replenish lost values from subtracting set intersection
		while len(invalids_sample) < n-valid_count:
			# Generate an x value
			x = random.randint(int(A**0.5), int(B**0.5))**2

			# In order to maintain frequency, give a chance that x will be an edge case
			if random.uniform(0, 1) <= rf:
				while (x % 2 == 0) | (x in valids) | (x in invalids_sample):
					x = random.randint(int(A ** 0.5), int(B ** 0.5)) ** 2
			else:
				while (x in valids) | (x in invalids_sample):
					x = random.randint(A, B)
			invalids_sample.add(x)

		for y in invalids_sample: cases.append((y, 0))

		random.shuffle(cases)

		return cases


def gen_range(a: int, b: int, n: int):
	# Generate a b-a cases for exponents a to b
	for N in range(a, b+1):
		r = random.uniform(0.33, 0.67)
		rf = random.uniform(0.33, 0.67)
		sample = generate(0, N, n=n, r=r, rf=rf)
		with open(f"/Users/dominictarro/Desktop/Code/Python/Discord Help/tests-10^{N}.json", 'w') as f:
			json.dump(sample, f)


if __name__ == "__main__":
	X = generate(4, 8, n=2000, r=0.5, rf=0.25, balanced=True)
	bound = 10**(5+(8-5)/3)
	count = 0
	for x, ans in X:
		if x < bound:
			count += 1
	print(len(X))


