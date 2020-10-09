from itertools import product
import random
import json
import string


from generators.bishop.solution import solution


numalpha = {i: char for i, char in enumerate(string.ascii_lowercase)}

numeric = range(1, len(numalpha))
n = range(100)
positions = [numalpha[x[0]] + str(x[1]) for x in product(numeric, numeric, repeat=1)]
combos = list(product(positions, positions, n, repeat=1))
sample = random.sample(combos, 100000)

n_extra = [0, 23, 24, 50, 51, 77]
for x in n_extra:
	for _ in range(3):
		z = random.choice(sample)
		i = sample.index(z)
		z = list(z)
		z[2] = x
		sample[i] = tuple(z)

cases = [0]*len(sample)
i = 0
for a, b, n in sample:
	answer = solution(a, b, n)
	cases[i] = [(a, b, n), int(answer)]
	i += 1

with open("../testsuite/tests/cardinal.json", 'w') as outfile:
	json.dump(cases, outfile)
