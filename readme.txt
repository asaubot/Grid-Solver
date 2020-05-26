Grid solver

This script will automatically generate a 4*4 letter grid, and will do this according to the probability of each letter appearing in the english language.

It will then figure out all the words that can be drawn from this grid and sort them by order of length

The rules are as follow : 
- Each word can be drawn on the grid by starting with one letter and then taking one of its neighbor (up to 8 neighbors per letter)
- The maximum length of a word is 12
- The minimum length of a word is 2
- One word cannot reuse the same letter twice (same letter means the letter at the same index : if a grid has two 'e', a word with two 'e' can be drawn)

The words will be compared with the ones in the english dictionary, and the algorithm will be quickened using a trie data structure to cancel the process once the first selected letters cannot lead to an existing word