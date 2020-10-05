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


def generate_sample(a: (int, float), b: (int, float), r: float, n: int, r0square: float = 0.5) -> dict:
	"""
	:param a: Lower exponent bound
	:param b: Upper exponent bound
	:param r: Frequency of True cases
	:param n: Test size
	:param r0square: Frequency of squared integers in the false set
	:return:
	"""
	#print(f"Generating {n} cases from range [10^{a}, 10^{b}]...")
	n = int(n)
	A = int(10**a) - 1
	B = int(10**b)
	print(n, A, B)
	prime_squares = modPrimeSieveSquared(A, B)

	# Number of primes in sample = sample size * prime frequency
	n_valid = int(n*r)
	if len(prime_squares) < n_valid:
		n_valid = len(prime_squares)
	# Number of squared compounds in compound sub sample = square frequency * (n - n_valid)
	n_c = n-n_valid
	n_csquare = r0square * (n_c)

	compounds = list(set(random.sample(range(A, B), n_c)) - set(prime_squares))

	i = 0
	cr_range = (x**2 for x in range(int(A**0.5), int(B**0.5)))
	# Replace some compounds with squares of smaller compounds
	while i < n_csquare:
		x = cr_range.__next__()
		if (x not in compounds) & (x not in prime_squares):
			compounds[i] = x
			i += 1

	while len(compounds) < n_c:
		x = int(random.choice(cr_range)) ** 2
		if (x not in compounds) & (x not in prime_squares):
			compounds.append(x)

	prime_sample = random.sample(prime_squares, n_valid)

	n = len(prime_sample) + len(compounds)
	return {'true': prime_sample,
			'false': compounds,
			'size': n,
			'rpositive': len(prime_sample),
			'rnegative': len(compounds),
			'r0negative': i}


def balance(a: (int, float), b: (int, float), n: int, r: float, r0square: float, samples: int) -> dict:
	"""
	:param a: Lower exponent bound
	:param b: Upper exponent bound
	:param r: Frequency of True cases
	:param n: Test size
	:param r0square: Frequency of squared integers in the false set
	:param samples: number of samples
	:return:
	"""
	# Uniform assumption update
	# Check balancing proof at 'tPrimes Generator Balancing.pdf' for detail
	mu_r = r
	d = (b-a)/samples
	n_i = int(n/samples)
	cases = {
		'true': [],
		'false': [],
		'size': 0,
		'rpositive': 0,
		'rnegative': 0,
		'r0negative': 0
		}
	frequencies = []

	for i in range(samples):
		a_i = a + d*i
		b_i = a + d*(i+1)
		sample = generate_sample(a=a_i, b=b_i, r=mu_r, n=n_i, r0square=r0square)
		frequencies.append(len(sample['true'])/sample['size'])

		for key in cases:
			if isinstance(cases[key], list):
				cases[key].extend(sample[key])
			else:
				cases[key] += sample[key]

		c_0 = samples*r/(b-a)
		mu_r = (c_0 - sum(frequencies))/(samples-i)

	return cases


if __name__ == '__main__':
	test = balance(0, 13, 1000, 1/3, 1/3, 2)
	for arg, ans in test:
		print(arg, ans)
