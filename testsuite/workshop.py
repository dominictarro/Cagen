
import sys
from contextlib import contextmanager


@contextmanager
def input_block(placeholder=None):
	# Blocks input
	stdin, sys.stdin = sys.stdin, placeholder
	try:
		yield placeholder
	except RuntimeError:
		sys.stdin = stdin
	finally:
		sys.stdin = stdin


@contextmanager
def io_block(placeholder=None, dump="dump.txt"):
	stdin, sys.stdin = sys.stdin, placeholder
	stdout, sys.stdout = sys.stdout, open(dump, 'a')
	try:
		yield placeholder
	except RuntimeError:
		sys.stdin = stdin
		sys.stdout = stdout
		#logging.warning(RuntimeError, stdin, stdout, sys.stdin, sys.stdout)
	finally:
		sys.stdin = stdin
		sys.stdout = stdout

def call(x):
	print("hello: ", x)
	print(input("respond: "))


for i in range(10):
	with io_block():
		call(i)

print("Done")