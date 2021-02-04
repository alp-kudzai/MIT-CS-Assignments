# 6.0001 Problem Set 3
#
# The 6.0001 Word Game
# Created by: Kevin Luu <luuk> and Jenna Wiens <jwiens>
#
# Name          : <your name>
# Collaborators : <your collaborators>
# Time spent    : <total time>

import math
import random
import string
import time

VOWELS = 'aeiou'
CONSONANTS = 'bcdfghjklmnpqrstvwxyz'
HAND_SIZE = 7

SCRABBLE_LETTER_VALUES = {
    'a': 1, 'b': 3, 'c': 3, 'd': 2, 'e': 1, 'f': 4, 'g': 2, 'h': 4, 'i': 1, 'j': 8, 'k': 5, 'l': 1, 'm': 3, 'n': 1, 'o': 1, 'p': 3, 'q': 10, 'r': 1, 's': 1, 't': 1, 'u': 1, 'v': 4, 'w': 4, 'x': 8, 'y': 4, 'z': 10, '*': 0
}

# -----------------------------------
# Helper code
# (you don't need to understand this helper code)

WORDLIST_FILENAME = "words.txt"

def load_words():
    """
    Returns a list of valid words. Words are strings of lowercase letters.
    
    Depending on the size of the word list, this function may
    take a while to finish.
    """
    
    print("Loading word list from file...")
    # inFile: file
    inFile = open(WORDLIST_FILENAME, 'r')
    # wordlist: list of strings
    wordlist = []
    for line in inFile:
        wordlist.append(line.strip().lower())
    print("  ", len(wordlist), "words loaded.")
    return wordlist

def get_frequency_dict(sequence):
    """
    Returns a dictionary where the keys are elements of the sequence
    and the values are integer counts, for the number of times that
    an element is repeated in the sequence.

    sequence: string or list
    return: dictionary
    """
    
    # freqs: dictionary (element_type -> int)
    freq = {}
    for x in sequence:
        freq[x] = freq.get(x,0) + 1
    return freq
	

# (end of helper code)
# -----------------------------------

#
# Problem #1: Scoring a word
#
def get_word_score(word, n):
    """
    Returns the score for a word. Assumes the word is a
    valid word.

    You may assume that the input word is always either a string of letters, 
    or the empty string "". You may not assume that the string will only contain 
    lowercase letters, so you will have to handle uppercase and mixed case strings 
    appropriately. 

	The score for a word is the product of two components:

	The first component is the sum of the points for letters in the word.
	The second component is the larger of:
            1, or
            7*wordlen - 3*(n-wordlen), where wordlen is the length of the word
            and n is the hand length when the word was played

	Letters are scored as in Scrabble; A is worth 1, B is
	worth 3, C is worth 3, D is worth 2, E is worth 1, and so on.

    word: string
    n: int >= 0
    returns: int >= 0
    """
    
    wordlen = len(word)
    sumPoints = 0
    for c in word:
        letter = c.lower()
        val = SCRABBLE_LETTER_VALUES.get(letter, 0)
        sumPoints += (val)
        
    comp2 = (7*wordlen - 3*(n - wordlen))   
    if comp2 >= 1:
        total_score = sumPoints * comp2
    else:
        total_score = sumPoints * 1
        
    return total_score

#
# Make sure you understand how this function works and what it does!
#
def display_hand(hand):
    """
    Displays the letters currently in the hand.

    For example:
       display_hand({'a':1, 'x':2, 'l':3, 'e':1})
    Should print out something like:
       a x x l l l e
    The order of the letters is unimportant.

    hand: dictionary (string -> int)
    """
    st = ''
    for letter in hand.keys():
        for j in range(hand[letter]):
             # print(letter, end=' ')
             st += (str(letter) + ' ')   # print all on the same line
    # print()
    return st                              # print an empty line

#
# Make sure you understand how this function works and what it does!
# You will need to modify this for Problem #4.
#
def deal_hand(n):
    """
    Returns a random hand containing n lowercase letters.
    ceil(n/3) letters in the hand should be VOWELS (note,
    ceil(n/3) means the smallest integer not less than n/3).

    Hands are represented as dictionaries. The keys are
    letters and the values are the number of times the
    particular letter is repeated in that hand.

    n: int >= 0
    returns: dictionary (string -> int)
    """
    hand = {}
    hand['*']= 1
    num_vowels = int(math.ceil(n / 4))

    for i in range(num_vowels):
        x = random.choice(VOWELS)
        hand[x] = hand.get(x, 0) + 1
    
    for i in range(num_vowels, n - 1):    
        x = random.choice(CONSONANTS)
        hand[x] = hand.get(x, 0) + 1
    
    return hand

#
# Problem #2: Update a hand by removing letters
#
def update_hand(hand, word):
    """
    Does NOT assume that hand contains every letter in word at least as
    many times as the letter appears in word. Letters in word that don't
    appear in hand should be ignored. Letters that appear in word more times
    than in hand should never result in a negative count; instead, set the
    count in the returned hand to 0 (or remove the letter from the
    dictionary, depending on how your code is structured). 

    Updates the hand: uses up the letters in the given word
    and returns the new hand, without those letters in it.

    Has no side effects: does not modify hand.

    word: string
    hand: dictionary (string -> int)    
    returns: dictionary (string -> int)
    """
    chand = hand.copy()
    for c in word:
        c = c.lower()
        if c not in chand:
            pass
        elif chand[c] > 1:
            chand[c] = chand[c] - 1
        else:
            chand.pop(c,0)
            
    return chand
        
    # pass  # TO DO... Remove this line when you implement this function

#
# Problem #3: Test word validity
#
def is_valid_word(word, hand, word_list):
    """
    Returns True if word is in the word_list and is entirely
    composed of letters in the hand. Otherwise, returns False.
    Does not mutate hand or word_list.
   
    word: string
    hand: dictionary (string -> int)
    word_list: list of lowercase strings
    returns: boolean
    """
    lower_word = ''
    chand = hand.copy()
    for c in word:
        lower_word += c.lower()
    tc = 0
    wrd_len = len(lower_word)
    
    if lower_word in word_list:
        pass
    elif '*' in lower_word:
        passed = False
        vowel = 'aeiou'
        for c in vowel:
            test_word = lower_word.replace('*', c)
            if test_word in word_list:
                passed = True
                break
        if passed:
            pass
        else:
            return False
    else:
        return False
    
    for c in lower_word:
        if c in chand:
            tc += 1
            chand = update_hand(chand, c)
        else:
            pass
        
    if tc == wrd_len:
        return True
    # pass  # TO DO... Remove this line when you implement this function

#
# Problem #5: Playing a hand
#
def calculate_handlen(hand):
    """ 
    Returns the length (number of letters) in the current hand.
    
    hand: dictionary (string-> int)
    returns: integer
    """
    hand_len = 0
    for v in hand:
        hand_len += hand.get(v, 0)
        
    return hand_len
    # pass  # TO DO... Remove this line when you implement this function

def play_hand(hand, word_list):

    """
    Allows the user to play the given hand, as follows:

    * The hand is displayed.
    
    * The user may input a word.

    * When any word is entered (valid or invalid), it uses up letters
      from the hand.

    * An invalid word is rejected, and a message is displayed asking
      the user to choose another word.

    * After every valid word: the score for that word is displayed,
      the remaining letters in the hand are displayed, and the user
      is asked to input another word.

    * The sum of the word scores is displayed when the hand finishes.

    * The hand finishes when there are no more unused letters.
      The user can also finish playing the hand by inputing two 
      exclamation points (the string '!!') instead of a word.

      hand: dictionary (string -> int)
      word_list: list of lowercase strings
      returns: the total score for the hand
      
    """
    
    # BEGIN PSEUDOCODE <-- Remove this comment when you implement this function
    total_score = 0     
    while calculate_handlen(hand) > 0:    # As long as there are still letters left in the hand:
        print('--------------------------------')
        ds = display_hand(hand)
        print('Current hand:',ds)    # Display the hand
        
        user_in = input('Enter a word, or "!!" if you are finished: ')  # Ask user for input
        
        if user_in == '!!':    # If the input is two exclamation points:
        
            break   # End the game (break out of the loop)

            
        else:    # Otherwise (the input is not two exclamation points):

            if is_valid_word(user_in, hand, word_list):   # If the word is valid:

                score = get_word_score(user_in, HAND_SIZE)
                print(f'{user_in} earned {score} points.')
                                       # Tell the user how many points the word earned,
                total_score += score# and the updated total score

            else:   # Otherwise (the word is not valid):
                print('That is not a valid word, please pick another one!')# Reject invalid word (print a message)
                
            hand = update_hand(hand, user_in)# update the user's hand by removing the letters of their inputted word
            time.sleep(-time.time()%1)  

    if calculate_handlen(hand) == 0:
        print(f'You ran out of letters. Total score: {total_score}points.')      # Game is over (user entered '!!' or ran out of letters),
    else:# so tell user the total score
        print(f'Total Score: {total_score} points.')
    return total_score # Return the total score as result of function



#
# Problem #6: Playing a game
# 


#
# procedure you will use to substitute a letter in a hand
#

def substitute_hand(hand, letter):
    """ 
    Allow the user to replace all copies of one letter in the hand (chosen by user)
    with a new letter chosen from the VOWELS and CONSONANTS at random. The new letter
    should be different from user's choice, and should not be any of the letters
    already in the hand.

    If user provide a letter not in the hand, the hand should be the same.

    Has no side effects: does not mutate hand.

    For example:
        substitute_hand({'h':1, 'e':1, 'l':2, 'o':1}, 'l')
    might return:
        {'h':1, 'e':1, 'o':1, 'x':2} -> if the new letter is 'x'
    The new letter should not be 'h', 'e', 'l', or 'o' since those letters were
    already in the hand.
    
    hand: dictionary (string -> int)
    letter: string
    returns: dictionary (string -> int)
    """
    vowels = 'aeiou'
    consonants = 'bcdfghjklmnpqrstvwxyz'
    if letter not in hand:
        return hand
    else:
        chand = hand.copy()
        letter_val = chand.get(letter, 0)
        if letter_val > 1:
            
            chand.pop(letter, 0)
        checking = True
        while checking:
            if letter in vowels:
                repl_let = random.choice(vowels)
                if repl_let not in hand:
                    checking = False
            else:
                repl_let = random.choice(consonants)
                if repl_let not in hand:
                    checking = False
        if letter_val > 1:
            
            chand[repl_let] = (1)
            chand[letter] = (letter_val - 1)
            
        else:
            chand[repl_let] = letter_val
        
        return chand
    
    # pass  # TO DO... Remove this line when you implement this function
       
    
def play_game(word_list):
    """
    Allow the user to play a series of hands

    * Asks the user to input a total number of hands

    * Accumulates the score for each hand into a total score for the 
      entire series
 
    * For each hand, before playing, ask the user if they want to substitute
      one letter for another. If the user inputs 'yes', prompt them for their
      desired letter. This can only be done once during the game. Once the
      substitue option is used, the user should not be asked if they want to
      substitute letters in the future.

    * For each hand, ask the user if they would like to replay the hand.
      If the user inputs 'yes', they will replay the hand and keep 
      the better of the two scores for that hand.  This can only be done once 
      during the game. Once the replay option is used, the user should not
      be asked if they want to replay future hands. Replaying the hand does
      not count as one of the total number of hands the user initially
      wanted to play.

            * Note: if you replay a hand, you do not get the option to substitute
                    a letter - you must play whatever hand you just had.
      
    * Returns the total score for the series of hands

    word_list: list of lowercase strings
    """
    total_score = 0
    print('-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-')
    times = int(input('Enter total number of hands: '))
    
    
    playing = True
    loop_counter = 0
    time.sleep(-time.time()%1)
    while playing:
        hand = deal_hand(HAND_SIZE)
        ds = display_hand(hand)
        print('Current hand:', ds)
        check_sub = True
        while check_sub:
            us_input = input('Would you like to substitute a letter "yes or "no": ')
            if us_input == 'yes':
                sub_letter = input('Which letter would you like to replace?: ')
                hand = substitute_hand(hand, sub_letter)
                check_sub = False
            elif us_input == 'no':
                check_sub = False
            else:
                print('Invalid input! Enter yes or no!')
            time.sleep(-time.time()%1)
        total_score += play_hand(hand, word_list)
        us_ans = input('Would you like to replay the hand?: ')
        time.sleep(-time.time()%1)
        replay_hand = True
        while replay_hand:
            if us_ans == 'yes':
                total_score += play_hand(hand, word_list)
                replay_hand = False
            elif us_ans == 'no':
                replay_hand = False
            else:
                print('Invalid input! Enter yes or no!')
        loop_counter += 1
        if loop_counter == times:
            playing = False
        else:
            print('Total score for this hand:', total_score)
            print('-----------------------------------------')
            
    print('Total score for all hands:', total_score)
    


#
# Build data structures used for entire session and play game
# Do not remove the "if __name__ == '__main__':" line - this code is executed
# when the program is run directly, instead of through an import statement
#
if __name__ == '__main__':
    word_list = load_words()
    play_game(word_list)
