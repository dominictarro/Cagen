import random
import json


def modPrimeSieveSquared(b: int, a: (int, float)) -> list:
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


def generate(a: (int, float), b: (int, float), r: float, n: int,
             balance: bool = False, samples: (int, list, tuple) = 1) -> float:
			'''
			:param a: Lower exponent bound
			:param b: Upper exponent bound
			:param r: Frequency of True cases
			:param n: Test size
			:param balance:
			:param samples:
			:return:
			'''


if __name__ == "__main__":
	print(modPrimeSieveSquared(120, 3))