from itertools import product
import random
import json
from bishop.solution import solution


numalpha = {
	1: "a",
	2: "b",
	3: "c",
	4: "d",
	5: "e",
	6: "f",
	7: "g",
	8: "h"
}

numeric = range(1, 9)
n = range(10)
positions = [numalpha[x[0]] + str(x[1]) for x in product(numeric, numeric, repeat=1)]
combos = list(product(positions, positions, n, repeat=1))
sample = random.sample(combos, 25000)

n_extra = [23, 24, 50, 51, 77]
for x in n_extra:
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

with open("../testsuite/tests/bishop.json", 'w') as outfile:
	json.dump(cases, outfile)
