# Cagen
Case generators and a solution-testing program for __Tech with Tim__'s weekly challenge on [Discord](https://discord.gg/PaKYTH).

## Challenge
The abstract testing unit for any challenge.<br>
[Read More](./challenge/README.md)

## Generators

    - Bishop
    - Easy Numbers
    - T-Primes
    - In 2120

## Problem Explanations
- [Bishop](./problems/bishop.md)
- [Easy Numbers](./problems/easynumbers.md)
- [T-Primes](./problems/tprimes.md)
- [In 2120](./problems/in2120.md)

## Generator Tools

### `wrap.binning`
 - Balances the distribution of values in a random sample from range [`10^m`, `10^M`).
 - Attenuates to the 90% skew towards the upper exponent by dividing the sampling into `k`

#### Parameters:
 - m: int/float
    - Lower bound for 10^x
 - M: int/float
    - Upper bound for 10^x
 - n: int
    - Sample size
 - k: int
    - Number of bins to use
 - **kwargs
    - Any keyword argument that is an iterable. Built into a generator that sends one value to each keyword on each
    iteration

The wrapper passes 3 arguments during each call that the generator function must be able to handle:
 1. The lower bound (absolute, not exponent) e.g. (100)
 2. The upper bound (absolute, not exponent) e.g. (10000.55)
 3. The sample size e.g. 1000

Basic implementation.
```python
from gentools.wrap import binning
import random

# Generate 5 sub-samples in the range 10^0 to
# 10^10 and merge them so they sum to 1000 cases
@binning(m=0, M=10, n=100000, k=10)
def generator(a, b, n):
    return random.choices(range(int(a), int(b)), k=n)


cases = generator()
```

Using iterables to map as arguments for each bin.
```python
from gentools.wrap import binning
import random

k = 4
# Random seeds for each bin's generation
seeds = [101, 392, 81]
# Text to print for each bin
printable = (f"Generating sample {i}" for i in range(k))


@binning(m=0, M=10, n=1000, k=k, seed=seeds, stdout=printable)
# Generate 5 sub-samples in the range 10^0 to
# 10^10 and merge them so they sum to 1000
def generator(a, b, n, seed=1, stdout="..."):
	random.seed(seed)
	print(f"Seed: {seed}")
	print("\t", stdout)
	return [([x], x % 2 == 0) for x in random.choices(range(int(a), int(b)), k=n)]


cases = generator()
```
Runtime output
```
>>> Seed: 101
>>>	 Generating sample 0
>>> Seed: 392
>>>	 Generating sample 1
>>> Seed: 81
>>>	 Generating sample 2
>>> Seed: 1
>>>	 ...
```