"""
READ BEFORE USE

Paste your solution in the file 'solution.py' and follow the described instructions

- Solutions that exceed the default time limit or fail maximum during runtime will be terminated
	- You will still receive performance results and response validity metrics for your completed cases

"""
# Foreign
import sys
import os

# Local dependencies
from testsuite import config, test


def execute():
	# TODO: config.INTRO        -complete
	# TODO: test selection      -complete
	print(config.INTRO)
	print(config.instructions)

	selected = None
	test_select = ""
	while selected is None:
		test_select = input("-> ")
		if test_select == '0':
			sys.exit()
		selected = config.get_test(test_select)
	os.system('cls' if os.name == 'nt' else 'clear')
	cases, answer_ctype = selected
	# TODO: test execution      -complete
	test.run(cases, answer_ctype)

	# TODO: code analytics      -complete
	# TODO: results analytics   -complete
	# TODO: results reporting   -complete
	results = test.score(n=len(cases))
	config.display_score(results)
	# TODO: missed case storage -complete
	if results["failed"] > 0:
		to_save = input("Would you like to save your missed cases?(Y/N)\n-> ").lower()
		if to_save == 'y':
			config.save_missed(
				fail_index=results["fail_index"],
				responses=results["fail_responses"],
				cases=cases,
				t_id=test_select
			)


if __name__ == "__main__":
	execute()
