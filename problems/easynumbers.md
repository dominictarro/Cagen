# Easy Numbers

## Problem
You're walking accross the street and you find a paper with what seems to be math problems. A particular one grabs your
interest as you have no idea right of the bat how it could have been possibly done.

```python
    >>> print(solution(1))
    0
    >>> print(solution(5))
    4
    >>> print(solution(10))
    9
    >>> print(solution(12))
    13
    >>> print(solution(34))
    57
    >>> print(solution(70))
    129
    >>> print(solution(100))
    189
```

Write up an algorithm that will be able to solve these examples (do not hard code it because your solution will be
tested against many randomly generated integers like that)

## Solution

First is recognizing the pattern. The 1, 5, and 10 are reduced by 1, 12 incremented by 1, but from there the answers
are ostensibly random. What we can say is that after 10, all answers are greater than the argument. The increments
tell us there must be an additive component.

`f(x) = ax + b`

The next part is deciphering what that is. For 1, 5 and 10 `b=-1`, but that stops with 12. However, `2*12-11 = 13`. Test
this hypothesis:
```
    2*1-11, 2*5-11, 2*10-11, 2*12-11, 2*34-11, 2*70-11, 2*100-11
    -9       -1        9        13      57       129      189
```


This captures part of the problem, but we notice that until we hit 10, `a=2`,`b=11` is inappropriate. We notice that the
arguments that had trouble with this solution are single digit numbers. Make a and b functions of the number of
digits:

`f(x) = a(x)x + b(x)`

Hypothesis: a(x) = number of digits of x
			b(x) = unit repdigit of length b(x)
```
    1*1-1, 1*5-1, 2*10-11, 2*12-11, 2*34-11, 2*70-11, 3*100-111
    0        4       9       13       57       129       189
```
This satisfies all examples and provides a generalized solution to larger numbers!

Defintion of the unit repdigit: `u(d) = (10^d-1)/9`<br>
Definition of digits: `d(x) = round( log_10(x) + 1 )`

### Code

```python
class Solution:

	@staticmethod
	def logdigits(x: int) -> int:
		return int(log10(x)) + 1

	@staticmethod
	def unitrep(d: int) -> int:
		return (10**d-1)//9

	@staticmethod
	def solution1(x: int):
		# Use import and unit definition
		return ( d := Solution.logdigits(x) )*x - Solution.unitrep(d)

	@staticmethod
	def solution2(x: int):
		# Use string conversion and unit definition
		return ( d := len(str(x)))*x - Solution.unitrep(d)

	@staticmethod
	def solution3(x: int):
		# Use string conversion only
		return (d := len(str(x)))*x - int('1'*d)
```