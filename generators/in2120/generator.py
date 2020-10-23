import random
import json
from string import digits

digits = digits.strip('0')


def solution(x: int) -> bool:
	return '0' in str(x).strip('0')


def gen_sub_sample(L: int, H: int, n: int, freq: float = 0.5) -> list:
	cases = []
	args = random.sample(range(L, H), n)

	true_count = 0
	false_count = 0

	for arg in args:
		ans = solution(arg)
		cases.append([(arg,), ans])

		if ans:
			true_count += 1
		else:
			false_count += 1

	true_ratio = true_count/n

	print(true_ratio)

	return cases


def gen_sample(L: int, H: int, n: int, bins: int = 1, freq: float = 0.5) -> list:
	leap = (H-L)//bins
	sizes = [(L+leap*i, L+leap*(i+1)) for i in range(bins)]
	subn = n//bins

	cases = []
	for low, high in sizes:
		subsample = gen_sub_sample(L=low, H=high, n=subn, freq=freq)
		cases.extend(subsample)

	return cases

