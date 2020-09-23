import random
import json


def modPrimeSieveSquared(a: (int, float), b: int) -> list:
	"""
	Returns a list of squared primes in the range [a, b]

	:param b: Upper bound for power of 10
	:param a: Lower bound for power of 10
	:return: List of prime squares in the range [a, b]
	"""
	root = int(b**0.5) + 1
	sieve = [True]*root
	sieve[:1] = [False]*2

	for i in range(2, root):
		pointer = i * 2
		while pointer < root:
			sieve[pointer] = False
			pointer += i

	return [i**2 for i, p in enumerate(sieve) if (b >= i**2 >= a) & p]


def frequency(sample: list, axis=None) -> float:
	if axis is not None:
		return sum([x[axis] for x in sample])/len(sample)
	return sum([x for x in sample])/len(sample)


def generate(a: (int, float), b: (int, float), r: float, n: int, r0square: float = 0.5, balance: bool = False,
    samples: (int, list, tuple) = 1):
	"""
	:param a: Lower exponent bound
	:param b: Upper exponent bound
	:param r: Frequency of True cases
	:param n: Test size
	:param r0square: Frequency of squared integers in the false set
	:param balance:
	:param samples:
	:return:
	"""
	if balance:
		if isinstance(samples, int):
			# Uniform assumption update
			mu_r = r

			pass
		else:
			# Non-uniform updating algorithm
			pass
	else:
		n = int(n)
		A = 10**a
		B = 10**b
		prime_squares = modPrimeSieveSquared(A, B)

		# Number of primes in sample = sample size * prime frequency
		n_valid = int(n*r)
		if len(prime_squares) < n_valid:
			n_valid = len(prime_squares)
		# Number of squared compounds in compound sub sample = square frequency * (n - n_valid)
		n_csquare = r0square * (n - n_valid)

		compounds = [x for x in random.sample(range(A, B), n - n_valid) if x not in prime_squares]

		i = 0
		cr_range = range(int(A**0.5), int(B**0.5))
		# Replace some compounds with squares of smaller compounds
		while i < n_csquare:
			x = int(random.choice(cr_range))**2
			if (x not in compounds) & (x not in prime_squares):
				print(x)
				compounds[i] = x
				i += 1

		prime_sample = random.sample(prime_squares, n_valid)
		cases = []

		cases.extend([(x, 1) for x in prime_sample])
		cases.extend([(x, 0) for x in compounds])
		random.shuffle(cases)
		return cases


if __name__ == "__main__":
	from tprimes.common_solutions import solution
	test = generate(8, 10, 0.5, 1000)
	n = len(test)
	for sol in solution:
		correct = 0
		for x, ans in test:
			if solution[sol](x) == ans:
				correct += 1
		print(sol, correct)
