import random
import json
import logging



def modPrimeSieveSquared(a: (int, float), b: int) -> list:
	"""
	Returns a list of squared primes in the range [a, b]

	:param b: Upper bound for power of 10
	:param a: Lower bound for power of 10
	:return: List of prime squares in the range [a, b]
	"""
	root = int(b**0.5)
	sieve = [True]*root
	sieve[:1] = [False]*2

	for i in range(2, int(root**0.5)+1):
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
			# Check balancing proof at 'tPrimes Generator Balancing.pdf' for detail
			mu_r = r
			d = (b-a)/samples
			n_i = int(n/samples)
			cases = []
			frequencies = []

			for i in range(samples):
				a_i = a + d*i
				b_i = a + d*(i+1)
				sample = generate(a=a_i, b=b_i, r=mu_r, n=n_i, r0square=r0square)
				frequencies.append(frequency(sample, axis=1))

				c_0 = samples*r/(b-a)
				mu_r = (c_0 - sum(frequencies))/(samples-i)

		else:
			# Non-uniform updating algorithm
			pass
	else:
		print(f"Generating {n} cases from range [10^{a}, 10^{b}]...")
		n = int(n)
		A = 10**a
		B = 10**b
		print("Generating prime squares...")
		prime_squares = modPrimeSieveSquared(A, B)

		# Number of primes in sample = sample size * prime frequency
		n_valid = int(n*r)
		if len(prime_squares) < n_valid:
			n_valid = len(prime_squares)
		# Number of squared compounds in compound sub sample = square frequency * (n - n_valid)
		n_c = n-n_valid
		n_csquare = r0square * (n_c)

		print("Building compounds...")
		compounds = list(set([x for x in random.sample(range(A-1, B), n_c)]) - set(prime_squares))

		i = 0
		k = 0
		cr_range = (x**2 for x in range(int(A**0.5)-1, int(B**0.5)))
		# Replace some compounds with squares of smaller compounds
		print("Inserting squares...")
		lenrange = int(B**0.5) - int(A**0.5) - 1
		while (i < n_csquare) & (k < lenrange):
			k += 1
			x = cr_range.__next__()
			if (x not in compounds) & (x not in prime_squares):
				compounds[i] = x
				i += 1

		print("Inserting compounds...")
		while len(compounds) < n_c:
			x = int(random.choice(cr_range)) ** 2
			if (x not in compounds) & (x not in prime_squares):
				compounds.append(x)

		prime_sample = random.sample(prime_squares, n_valid)
		cases = []

		cases.extend([(x, 1) for x in prime_sample])
		cases.extend([(x, 0) for x in compounds])
		random.shuffle(cases)
	return cases


if __name__ == "__main__":

	def isinteger(x):
		r = x ** 0.5
		if r.is_integer():
			return r > 1
		return 0


	def iseven(x):
		return x % 2


	def isintoreven(x):
		r = x ** 0.5
		if r.is_integer():
			return r > 1
		return r % 2 == 1


	def ifykyk(x):
		r = x ** 0.5
		if r.is_integer():
			for i in range(2, int(r**0.5)+1):
				if r % i == 0:
					return 0
			return r > 1
		return 0


	solution = {
		'isinteger': isinteger,
		'iseven': iseven,
		'ifykyk': ifykyk,
		'isintoreven': isintoreven,
	}

	ranges = [(0, 8), (0, 12)]#, (0, 16)]
	#ranges = [(0, 16)]
	files = ["lvl0.json", "lvl1.json"]#, "lvl2.json"]
	#files = ["lvl2.json"]
	i = 0
	for a, b in ranges:
		print("")
		cases = generate(a, b, 1/3, 50000)
		with open(files[i], 'w') as f:
			json.dump(cases, f)
		i += 1


