import json


def solution(n,m):
	t=n+m-2
	while m:n,m=m,n%m
	return t+n


gcd = lambda n,m:gcd(m,n%m) if m else n


for fn in ["diagonal-0.json", "diagonal-1.json", "diagonal-2.json", "diagonal-3.json"]:
	with open(fn, 'r') as f:
		cases = json.load(f)

	squares = 0
	gcds = 0

	for args, ans in cases:
		if args[0] == args[1]:
			squares += 1
		elif gcd(*args) != 1:
			gcds += 1

	print(fn)
	print(f"Total: {len(cases)}")
	print(f"Square: {squares}")
	print(f"GCD: {gcds}")
	print("")
