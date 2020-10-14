import random
import json

from .solution import solution

A = 1
B = 10**15
n = 10**5

cases = []

args = random.sample(range(A, B+1), n)

for x in args:
	cases.append(([x], solution(x)))

with open("../challenge/cases/easy.json", 'w') as f:
	json.dump(cases, f)
