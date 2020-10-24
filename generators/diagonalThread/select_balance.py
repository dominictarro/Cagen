from .solution import solution
from gentools.wrap import binning
import random
import json


@binning(m=0, M=18.9648976075, n=100000, bins=4)
def generator(a, b, n) -> list:
	rng = range(int(a), int(b)+1)

	x_samp = random.sample(rng, k=n)
	y_samp = random.sample(rng, k=n)

	cases = []
	for x, y in zip(x_samp, y_samp):
		sol = solution(x, y)
		cases.append(((x, y), sol))

	for _ in range(int(n**0.5)):
		new = tuple([random.choice(rng)]*2)
		sol = solution(*new)
		cases.pop(random.randint(0, n))
		cases.insert(random.randint(0, n), [new, sol])

	return cases


metasample = generator()

print(x:=max(max([x[0] for x in metasample])))
print(len(str(x)))
