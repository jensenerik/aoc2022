# Advent of code 2022

https://adventofcode.com/2022

### Day 17 comments

Day 17 is a tetris simulation without row erasing or random pieces, and with fixed player input.
We drop a sequence of shapes onto each other, with a series of left and right motions (the input)
alternating with drops. We must determine the height of the tower after a certain number of pieces
have been dropped.

The straightforward approach involves creating a mask for each piece, and determining whether each step
causes a collision. My solution stores both the previous pieces and the currently moving piece as
sets of coordinates (tuples of integers). The mask of the moving piece is added to an offset to determine
the current and next positions, with some logic around collision detection. To drop multiple pieces,
we just need to track the state of the board and our place in the sequence of left/right moves.

However, for part 2, we get a terrible surprise, as we are asked to calculate the final position after
one trillion pieces have been dropped. The naive approach is fast enough for a couple thousand pieces,
but takes 20 seconds for 10,000 pieces, so a trillion take some decades.

My solution for part 2 relies on the fact that the pieces come in a sequence of 5, and the left/right
input is finite and repeats, so we could imagine that the moves might repeat as well, eventually.
A repeating sequence would allow us to calculate a much smaller set of moves, then multiply the height
added by the sequence to get to our target, plus a few extra moves if it doesn't work out evenly.
