# Foreign dependencies
import sys
import os

# Local dependencies
from challenge import config, test, utils


def main():
	# Display
	print(config.INTRO)
	print(config.instructions)

	# Acquire test id
	selection = None
	while selection is None:
		# Choose test
		test_selection = input("-> ")
		if test_selection == config.EXIT:
			sys.exit()
		selection = config.get_test(test_selection)

	# Clear terminal
	os.system('cls' if os.name == 'nt' else 'clear')
	cases, type_id = selection

	# Run test
	results, timer = test.run(cases, type_id)

	# Score results
	score = results.score(cases, timer)

	# Display results
	utils.display_score(score=score)

	# If failed cases, offer to save for further review
	if len(score["fails"]) > 0:
		to_save = input("Would you like to save your missed cases?(Y/N)\n-> ").lower()
		if to_save == 'y':
			utils.save_missed(score)


if __name__ == "__main__":
	main()
