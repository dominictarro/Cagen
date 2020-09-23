
def isinteger(x):
	r = x**0.5
	if r.is_integer():
		return r > 1
	return 0


def iseven(x):
	return x % 2


def rootprime(x):
	r = x**0.5
	if r.is_integer():
		for i in range(2, int(r**0.5)+1):
			if r % i: return 0
		return x > 1

solution = {'isinteger': isinteger, 'iseven': iseven, 'rootprime': rootprime}
