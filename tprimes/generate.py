import random
import json
from tprimes import select


def solution(x: int) -> bool:
	if x <= 0:
		return False
	r = x**0.5
	# Eliminate x does not have a root
	if r.is_integer():
		# Eliminate if root <= 3 is not 2 or 3
		if r <= 3:
			return r > 1
		# Eliminate if divisible by 2 or 3
		elif (r % 2 == 0) | (r % 3 == 0):
			return 0

		# Eliminate odd numbers with divisors
		for i in range(5, int(r**0.5)+1, 2):
			if r % i == 0:
				return 0
		return 1
	return 0


if __name__ == "__main__":
	cases = select.generate(0, 10, 1000)

	for arg, answer in cases:
		sol = solution(arg)
		if sol != answer:
			print(arg, sol, answer)

