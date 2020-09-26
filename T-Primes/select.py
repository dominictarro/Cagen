import random
import json


def tPrimeSieveRoot(A: (int, float), B: int) -> list:
	"""
	Returns a list of squared primes in the range [a, b]

	:param A: Lower bound
	:param B: Upper bound
	:return: List of prime squares in the range [A, B]
	"""
	a_root = int(A ** 0.5)
	root = int(B ** 0.5)
	sieve = [True] * root
	sieve[:1] = [False] * 2

	# Eliminate evens
	print("Eliminating evens...")
	sieve[4::2] = [False] * int(root / 2 - 1)

	print("Eliminating odds...")
	# Search for odds
	for i in range(3, int(root**0.5) + 1, 2):
		if sieve[i]:
			sieve[2*i::i] = [False] * int(root / i - 1)
	print("Yielding primes...")
	if a_root % 2 == 0:
		# Return primes that are along even indices
		# e.g. a_root = 10
		# x = 2*i + a_root
		# List comp [2*i + a_root for i, x in enumerate(sieve[a_root::2])]
		# i   0  1  2  3 ...
		# x  10 12 14 16 ...
		# [i*2 + a_root for i, x in enumerate(sieve[a_root+1::2])]
		# i   0  1  2  3 ...
		# x  11 13 15 17 ...
		return [2*i + a_root for i, x in enumerate(sieve[a_root+1::2]) if x]
	# Return odd indexed primes
	return [i*2 + a_root for i, x in enumerate(sieve[a_root::2]) if x]


def generate(a, b, n):

	A = 10**a
	if a == 0:
		A = 0
	B = 10**b

	aroot = int(A**0.5)
	broot = int(B**0.5)
	print(aroot, broot)
	print("Generating sieve...")
	sieve = tPrimeSieveRoot(A, B)
	tprime_n = int(n/3)
	try:
		sieve_samp = random.sample(sieve, tprime_n)
	except ValueError:
		tprime_n = len(sieve)
		sieve_samp = sieve

	odd_n = int((n - tprime_n)/2)

	if a % 2 == 0:
		print("Generating sample of evens...")
		odd_samp = [(x**2, 0) for x in set(random.sample(range(aroot+1, broot, 2), odd_n)) - set(sieve)]
		print("Generating sample of odds...")
		even_n = max(n - tprime_n - len(odd_samp), 0)
		even_samp = [(x**2, 0) for x in random.sample(range(aroot, broot, 2), even_n)]
	else:
		print("Generating sample of odds...")
		odd_samp = [(x**2, 0) for x in set(random.sample(range(aroot+1, broot, 2), odd_n)) - set(sieve)]
		print("Generating sample of evens...")
		even_samp = [(x**2, 0) for x in random.sample(range(aroot, broot, 2), n - tprime_n - len(odd_samp))]

	cases = []
	print("Building cases...")
	cases.extend(odd_samp)
	cases.extend(even_samp)
	cases.extend([(x**2, 1) for x in sieve_samp])
	random.shuffle(cases)

	try:
		# See if (4, 0) was generated by the even sample
		# If so, convert to true case
		i = cases.index((4, 0))
		cases[i] = (4, 1)
	except ValueError:
		pass

	return cases