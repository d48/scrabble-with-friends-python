from ps4a import *
import time
from timeit import default_timer as timer

ALPHABET = 'abcdefghijklmnopqrstuvwxyz'

#
# Computer chooses a word
#
def compChooseWord(hand, wordList, n, wordDict, wordListByLength, handLen):
    """
    Given a hand and a wordList, find the word that gives
    the maximum value score, and return it.

    This word should be calculated by considering all the words
    in the wordList.

    If no words in the wordList can be made from the hand, return None.

    hand: dictionary (string -> int)
    wordList: list (string)
    n: integer (HAND_SIZE; i.e., hand size required for additional points)
    wordDict: dictionary (string -> int), word -> wordScore
    wordListByLength: list, list of words that are a subset of wordDict

    returns: string or None
    """
    # Create a new variable to store the maximum score seen so far (initially 0)
    bestScore = 0
    # Create a new variable to store the best word seen so far (initially None)
    bestWord = None

    # For each word in the wordList
    for word in wordListByLength:
        # If you can construct the word from your hand
        if isValidWord(word, hand, wordListByLength):
            # find out how much making that word is worth
            score = wordDict[word]
            # If the score for that word is higher than your best score
            if (score > bestScore):
                # update your best score, and best word accordingly
                bestScore = score
                bestWord = word
    # return the best word you found.
    return bestWord


#
# Computer plays a hand
#
def compPlayHand(hand, wordList, n, wordDict, wordDictByLength):
    """
    Allows the computer to play the given hand, following the same procedure
    as playHand, except instead of the user choosing a word, the computer
    chooses it.

    1) The hand is displayed.
    2) The computer chooses a word.
    3) After every valid word: the word and the score for that word is
    displayed, the remaining letters in the hand are displayed, and the
    computer chooses another word.
    4)  The sum of the word scores is displayed when the hand finishes.
    5)  The hand finishes when the computer has exhausted its possible
    choices (i.e. compChooseWord returns None).

    hand: dictionary (string -> int)
    wordList: list (string)
    wordDict: dictionary (string -> int), words -> wordScore
    n: integer (HAND_SIZE; i.e., hand size required for additional points)
    """
    # Keep track of the total score
    totalScore = 0

    # store hand length
    handLen = calculateHandlen(hand)

    # As long as there are still letters left in the hand:
    while (handLen > 0):
        # Display the hand
        print("Current Hand: ", end=' ')
        displayHand(hand)

        # there are no valid 1 letter words for this game
        if handLen == 1:
            break

        # only look at a subset of the wordList that has length of words less than or equal to the length of the hand
        wordListByLength = []

        # store list to loop through
        tempList = []

        alphaLeft = ALPHABET

        for item in hand:
            if hand[item] > 0:
                alphaLeft = alphaLeft.replace(item, '')

        # print("characters left: ", alphaLeft)


        # main optimization part 1: this reorganizes word list to filter through
        wordLengthDictByChar = build_wordlist_by_char(wordLengthDict)

        # main optimization part 2: this filters through all word lists from collection, and removes words that start with characters
        # that are not possible that start with characters that are not in player's hand

        # loop through wordDictByLength
        for key in wordLengthDictByChar:

            # if key of word length fits within hand size
            if key <= handLen:
                # view sublist based on hand length possibilities
                tempList = wordLengthDictByChar[key]

                # loop through sublist of all keys in alphabet
                for char in tempList:

                    # check if character is not in the remaining alphabet that represents letters not in hand
                    if char not in alphaLeft:

                        # concatenate words that start with character to words to search through
                        wordListByLength += tempList[char]


        # computer's word
        start = timer()
        word = compChooseWord(hand, wordList, n, wordDict, wordListByLength, handLen)
        end = timer()
        print("Time to choose word: ", end - start)
        # If the input is a single period:
        if word == None:
            # End the game (break out of the loop)
            break

        # Otherwise (the input is not a single period):
        else :
            # If the word is not valid:
            if (not isValidWord(word, hand, wordListByLength)) :
                print('This is a terrible error! I need to check my own code!')
                break
            # Otherwise (the word is valid):
            else :
                # Tell the user how many points the word earned, and the updated total score
                score = wordDict[word]
                totalScore += score
                print('"' + word + '" earned ' + str(score) + ' points. Total: ' + str(totalScore) + ' points')
                # Update hand and show the updated hand to the user
                hand = updateHand(hand, word)

                # update hand length and dict of words to look through
                handLen = calculateHandlen(hand)
                print()
    # Game is over (user entered a '.' or ran out of letters), so tell user the total score
    print('Total score: ' + str(totalScore) + ' points.')


#
# Problem #6: Playing a game
#
def playGame(wordList, wordDict, wordDictByLength):
    """
    Allow the user to play an arbitrary number of hands.

    1) Asks the user to input 'n' or 'r' or 'e'.
        * If the user inputs 'e', immediately exit the game.
        * If the user inputs anything that's not 'n', 'r', or 'e', keep asking them again.

    2) Asks the user to input a 'u' or a 'c'.
        * If the user inputs anything that's not 'c' or 'u', keep asking them again.

    3) Switch functionality based on the above choices:
        * If the user inputted 'n', play a new (random) hand.
        * Else, if the user inputted 'r', play the last hand again.

        * If the user inputted 'u', let the user play the game
          with the selected hand, using playHand.
        * If the user inputted 'c', let the computer play the
          game with the selected hand, using compPlayHand.

    4) After the computer or user has played the hand, repeat from step 1

    wordList: list (string)
    wordDict: dict (strings -> word score)
    wordDictByLength: dict (int -> list), keys are length of words for values in it's list
    """
    # keep record of hand and user inputs
    lastHand = {}
    userInput = ''
    userInput2 = ''

    # loop through user input
    while True:
        userInput = input("Enter n to deal a new hand, r to replay the last hand, or e to end game: ").lower()

        if userInput == "e":
            break;

        elif userInput == "r" and len(lastHand) == 0:
            print("You have not played a hand yet. Please play a new hand first!")

        elif userInput == "n" or userInput == "r":

            if userInput == "n":
                # deal new hand
                lastHand = dealHand(HAND_SIZE).copy()

                # lastHand = {'o': 1, 'e': 1, 'w': 1, 'r': 1, 'v': 1, 'd': 1, 'm': 1}

                # print(lastHand)

            # main loop for second user input to play yourself or have the computer play
            while True:
                userInput2 = input("Enter u to have yourself play, c to have the computer play: ").lower()

                if userInput2 == "u":
                    playHand(lastHand, wordList, HAND_SIZE)
                    break;

                elif userInput2 == "c":
                    compPlayHand(lastHand, wordList, HAND_SIZE, wordDict, wordDictByLength)
                    break;

                else:
                    print("Invalid command.")

        else:
            print("Invalid command.")


def buildWordDict(wordList, n):
    """
    wordList: set of words
    n: hand size

    Returns: a dictionary of strings -> word score
    """
    # store the results
    results = {}

    # loop through each word
    for word in wordList:

        # add to dict the wordscore for each based on hand size
        results[word] = getWordScore(word, n)

    return results

def build_wordlist_by_char(wordLengthDict):
    """
    wordLengthDict: dict(int -> list), dictionary of integer keys that correspond to length of words that are in it's list value

    Returns: dict(int -> dict (string -> list)), a dictionary with keys that are integers that correspond to the length of each each word in the corresponding dictionary, where this dictionary's keys are characters for the list of words that start with that charcter. This is used to search on a sublist of words.
    Example: { 2: { 'a': ['aa, 'ab, 'ad'], 'b': ['ba', 'bo', 'be'] }, 3: { 'a': ['ads', 'ace'], 'b': ['bae', 'bod'] } } ...
    """
    results = {}
    tempList = []
    firstChar = ''

    # go through each key that correspond to word size
    for item in wordLengthDict:
        # get all words of that length
        tempList = wordLengthDict[item]

        # go through each word in the list
        for word in tempList:
            # get first character, and add to results[item][<char>].append(word)
            results[item] = results.get(item, {})

            # save first char
            firstChar = word[0]

            # check if first char exists to append to
            results[item][firstChar] = results[item].get(firstChar, [])

            # save word
            results[item][firstChar].append(word)

    return results

def buildWordLengthDict(wordList, handSize):
    """
    wordList: list of strings, words from 2 characters to 8 characters long
    handSize: int, max hand size to save keys in dictionary

    Returns: dict (int -> list), a dictionary with keys that are integers that correpond to the length of each word in it's list of values
    """
    results = {}
    wordLen = 0
    tempList = []

    # loop through each word in the wordList
    for word in wordList:

        # get length of the word
        wordLen = len(word)

        # only save words that fit within handSize
        if wordLen <= handSize:

            # get list if it exists or assign empty list if it doesn't
            results[wordLen] = results.get(wordLen, [])

            # append word to key list
            results[wordLen].append(word)

    # return list
    return results

#
# Build data structures used for entire session and play game
#
if __name__ == '__main__':
    wordList = loadWords()
    wordDict = buildWordDict(wordList, HAND_SIZE)
    wordLengthDict = buildWordLengthDict(wordList, HAND_SIZE)

    playGame(wordList, wordDict, wordLengthDict)

