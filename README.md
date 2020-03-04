# Overview

Command-line word game in Python from an online comp sci class: words with friends

Letters are dealt to players, who then construct one or more words out of their letters. Each valid word receives a score, based on the length of the word and the letters in that word.

Original word list consists of up to 8 letter words for a total of 83,667 words.

Updated word list of up to 8 letter words for a total of 370,103 words.

**Note on word lists**
* `words.txt` - 83,667 words
* `TWL06.txt` Tournament Word List (TWL06): TWL - the American dictionary, based on the Official Scrabble Players' Dictionary , used in North American and Canadian tournaments - 178,691 words
* `words_alpha.txt` - 370,103 words


# Usage

```bash
$ python3 wordgameb.py

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

The default game given in the class did not have any optimizations for computer choosing the best scoring word. There was an optional exercise to make that algorithm faster. This repo covers explorations into those algorithm optimizations.

The main functions that were updated are found in `compPlayHand` and `compChooseWord`. The functions were modified to reduce the time for the computer turn in choosing the best word score based on remaining letters in it's hand by reducing the search space.

## Goal
A goal of mine is to get the time it takes for the computer player to choose the best scoring 7 and 8 letter word to be **less than one second**. 

## Version 1

### Before

 * **117 seconds** for all hands from _1_ to _n_ where _n_ number of letters in each hand.

### After

* **27 seconds** for 7 letter hands (75% reduction in time to compute).
* **280 ms** for 4 letter hands.
* **5 ms** for 2 letter hands.

1. Pre-calculate all word Scrabble score values from the word list for constant time look-up.
2. Computer player: Check for best valid word score from a subset of the word list that match the length of the player's hand, instead of searching the entire list of ~83k words on each hand.


## Version 2

* **9.3 seconds** for 7 letter hands (66% reduction from last version).

Reduces search space by removing word search on words that start with letters that the player does not have in their hand.

## Version 3

* **1.5 seconds** for 7 letter hands (84% reduction from last version).

Improves on Version 2 by limiting word search with a pre-step of grouping words by character. This makes the word list that is filtered quicker to put together before the best score is calculated for all words.

## Version 4

* **0.5 seconds** or **574 ms** for 7 letters hands (66% reduction from last version).

Similar to Version 3 with pre-step by going through reduced word list but checking through each word to see if last character is not in player's hand. On average this reduced the search space for checking the best word the computer can make from 33-66%.


## Version 5 

* **100 ms** for 7 letters hands (80% reduction from last version) and **150ms** average for 8 letter hands.

Continue with Version 4 step of further reducing search space for best scoring word. Implement an algorithm to check if any characters exist in a word that is a character not in the player's hand since we know the player would not be able to make that word. This gave an average reduction of the search space by 95-99% of the total words and gave great actual search time of around 100 ms average for computer choosing the best scoring word.

**Note**
* On a word list of 370k words, average look up time in 8-letter hands are 300ms.
