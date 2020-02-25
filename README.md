# Overview

Command-line word game in Python from the MITx 6.00.1x Intro to Computer Science class: Scrabble with Friends

This game is a lot like Scrabble or Words With Friends, if you've played those. Letters are dealt to players, who then construct one or more words out of their letters. Each valid word receives a score, based on the length of the word and the letters in that word.

Current word list consists of up to 8 letter words for a total of 83,667 words.


# Usage

```bash
$ python3 ps4b.py

Enter n to deal a new hand, r to replay the last hand, or e to end game: n

Enter u to have yourself play, c to have the computer play: u

Current Hand: a p y h h z o
Enter word, or a "." to indicate that you are finished: zap 
"zap" earned 42 points. Total: 42 points

Current Hand: y h h o
Enter word, or a "." to indicate that you are finished: oy
"oy" earned 10 points. Total: 52 points

Current Hand: h h
Enter word, or a "." to indicate that you are finished: .
Goodbye! Total score: 52 points.

Enter n to deal a new hand, r to replay the last hand, or e to end game: r

Enter u to have yourself play, c to have the computer play: c

Current Hand:  a p y h h z o
"hypha" earned 80 points. Total: 80 points

Current Hand:  z o
Total score: 80 points.

Enter n to deal a new hand, r to replay the last hand, or e to end game: e
```

# Optimizations

This repo consists of optimizations for the algorithms in the `compPlayHand` and `compChooseWord` functions to reduce computer turn in choosing the best word based on remaining letters in it's hand.

## Before

 * **117 seconds** for all hands from _1_ to _n_ where _n_ number of letters in each hand.

## After

* **27 seconds** for 7 letter hands (75% reduction in time to compute)
* **280 ms** for 4 letter hands
* **5 ms** for 2 letter hands.

### Updates that were made

1. Pre-calculate all word scores based on Scrabble values for constant time look-up.
2. Check for valid word score based on hand only on a subset of the word list (only look at words based on how many letters are in the player's hand)

# How to make it faster

One idea to make the algorithm faster for the computer player in choosing the best word would be to have all permutations of hands pre-calculated and saved in a hash table for **O(1)** lookup.
