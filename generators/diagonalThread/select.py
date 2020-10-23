import random
import json


def solution(n,m):
	t=n+m-2
	while m:n,m=m,n%m
	return t+n


def generator(a, b, n) -> list:
	rng = range(a, b)

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


if __name__ == "__main__":
	sample_params = [
		(1, 10**6, 10**4),
		(1, 10**8, 10**5),
		(1, 10**12, 10**6),
		(1, 10**16, 10**4)
	]

	for i, params in enumerate(sample_params):
		cases = generator(*params)

		with open(f"diagonal-{i}.json", 'w') as f:
			json.dump(cases, f)
