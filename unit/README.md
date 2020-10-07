# Coding Challenge Unit Tester

Developed for the [Tech with Tim Discord](https://discord.gg/PaKYTH) challenges, this program tests a solution function against pre-defined test cases.


## Functionality

<div id="functionality"></div>

- Time limit
- Fail limit
- Input/output blocking
- Rule violation identifiers
    - Imports
    - IO
    - Solution calls
    - eval, exec, compile methods
- Missed case history
- Error tracking
- Performance metrics
    - True code length
    - Runtime and iteration rate precision up to one-thousandth of a second per iteration
    – Correct / Completed, fraction and percentage



## User Instructions

<div id="user_inst"></div>

1. Open the file `solution.py` and replace the placeholder solution with your solution.
    - Make sure your function is called `solution`
2. Go to `main.py` and run the program.
3. Enter the test id you would like to test your algorithm against
4. Await results
5. If any, save missed cases (optional)

## Admin Instructions

<div id="admin_inst"></div>

The cases ought to be stored in a json file, formatted as follows:

    [
        [[arguments], answer],
        [[arguments], answer],
        ...
    ]

Note that the arguments must be a nested list, even if there is only one.

`test_attr.json` contains information about the tests

    {
        "test id": {
            "filename": "./tests/test.json",
            "difficulty": "medium",
            "size": 1000,
            "args": "[1,10000]",
            "response-type": "int",
            "open": true
        }
    }

__test id__
_id the user will input to select test (string)_
__filename__
_relative path to file (string)_<br>
__difficulty__ 
_(string)_<br>
__size__ 
_number of cases (integer)_<br>
__args__ 
_boundaries for arguments (string)_<br>
__response-type__ 
_expected output data type (string)_<br>
__open__
_whether or not this test is available for use (boolean)_<br>


You can also modify the default settings for the test in the file `default.json`.

    {
        "FAIL_MAX": 30,
        "RUNTIME_MAX": 10,
        "ENDL": "\n",
        "SPACE": 20,
        "INTRO": "{color}Welcome to the {header}Tech with Tim{color}, Discord challenge tester!{clear}\n",
        "EXIT": "0"
    }

The settings relevant to the test include

*__FAIL_MAX__
_Maximum tolerance for failed cases (integer)_<br>
*__RUNTIME_MAX__
_Maximum tolerance for algorithm runtime (numeric)_<br>
__INTRO__
_Pre-formatted introductory text upon running the program_<br>

*_Will still return results after shutting down test_


## Results

<div id="results"></div>

__Why do some of my responses show -1, -1.0, or "-1"?__<br>
- This occurs when there was an error in your solution, or the data type of your response does not match the data type of the answer. Check `/results/errors.json` for the exception raised.

