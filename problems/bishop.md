# Bishop

## Problem
Your chess teacher wants to know if a bishop can reach a certain spot on the board in the given amount of moves.

Given a starting square (str), ending square (str) and the maximum number of moves allowed (int). Return True if the
ending square can be reached from the starting square within the given amount of moves. Keep in mind the chessboard goes
from a1 to h8 (8x8).

Example:

    solution("a1", "b4", 3)
    >>> True

## Solution

When looking at a chess board, we observe two possible colors. All squares of one color can be accessed by no more that
two diagonal moves. We can also convert the alphabetical characters to a number, giving us a matrix.

    a -> 1
    b -> 2
    c -> 3
    ...

![](https://www.chessbaron.ca/blog/wp-content/uploads/2015/11/chessboardmove1.jpg)

After redefining the board in numerals, we can observe a pattrn among the squares by summing the individual square.

    a1 -> 2
    a2 -> 3
    a3 -> 4
    ...
    h6 -> 14
    h7 -> 15
    h8 -> 16

The position 'a1' can reach 'a2', but not 'a3'. It can also reach 'h6' and 'h8' but not 'h7'. As we can see from our
sums, the even-sum points can reach any other even sum point in a minimum of two moves. Therefore, our primary test
becomes "are you an even or odd sum?".

For situations where we can only use one move, we simply check if the slope between the positions is 1 or -1.

For situations of zero moves, check if the two positions are equal.
