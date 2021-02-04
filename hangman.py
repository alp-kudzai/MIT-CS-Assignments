# Problem Set 2, hangman.py
# Name: 
# Collaborators:
# Time spent:

# Hangman Game
# -----------------------------------
# Helper code
# You don't need to understand this helper code,
# but you will have to know how to use the functions
# (so be sure to read the docstrings!)
import random
import string

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
    # line: string
    line = inFile.readline()
    # wordlist: list of strings
    wordlist = line.split()
    print("  ", len(wordlist), "words loaded.")
    return wordlist



def choose_word(wordlist):
    """
    wordlist (list): list of words (strings)
    
    Returns a word from wordlist at random
    """
    return random.choice(wordlist)

# end of helper code

# -----------------------------------

# Load the list of words into the variable wordlist
# so that it can be accessed from anywhere in the program
wordlist = load_words()


def is_word_guessed(secret_word, letters_guessed):
    '''
    secret_word: string, the word the user is guessing; assumes all letters are
      lowercase
    letters_guessed: list (of letters), which letters have been guessed so far;
      assumes that all letters are lowercase
    returns: boolean, True if all the letters of secret_word are in letters_guessed;
      False otherwise
    '''
    secret_word_list = list(secret_word)
    true_counter = 0
    for c in letters_guessed:
        if c in secret_word_list:
            true_counter += 1
    word_len = len(letters_guessed)
    if true_counter == word_len:
        return True
    else:
        return False 


def get_guessed_word(secret_word, letters_guessed):
    '''
    secret_word: string, the word the user is guessing
    letters_guessed: list (of letters), which letters have been guessed so far
    returns: string, comprised of letters, underscores (_), and spaces that represents
      which letters in secret_word have been guessed so far.
    '''
    word_len = len(secret_word)
    list_container = ['_ ']*word_len
    secret_word_list = list(secret_word)
    index = 0
    for c in secret_word_list:
        for l in letters_guessed:
            if c == l:
                list_container[index] = str(l)
        index += 1
    container = ''.join(list_container)
    return container


def get_available_letters(letters_guessed):
    '''
    letters_guessed: list (of letters), which letters have been guessed so far
    returns: string (of letters), comprised of letters that represents which letters have not
      yet been guessed.
    '''
    alpha = string.ascii_lowercase
    alpha_list = list(alpha)
    clone_list = alpha_list[:]
    for c in alpha_list:
        if c in letters_guessed:
            clone_list.remove(c)
    alpha_str = ''.join(clone_list)
    return alpha_str
    
    
    

def hangman(secret_word):
    '''
    secret_word: string, the secret word to guess.
    
    Starts up an interactive game of Hangman.
    
    * At the start of the game, let the user know how many 
      letters the secret_word contains and how many guesses s/he starts with.
      
    * The user should start with 6 guesses

    * Before each round, you should display to the user how many guesses
      s/he has left and the letters that the user has not yet guessed.
    
    * Ask the user to supply one guess per round. Remember to make
      sure that the user puts in a letter!
    
    * The user should receive feedback immediately after each guess 
      about whether their guess appears in the computer's word.

    * After each guess, you should display to the user the 
      partially guessed word so far.
    
    Follows the other limitations detailed in the problem write-up.
    '''
    secretW_len = len(secret_word)
    l_g = []    #letters guessed
    sw = secret_word    #secret word
    guesses = 6
    warnings = 3
    
    avail_letters = get_available_letters(l_g)
    print('The secret word is', secretW_len,'letters long.\n')
    print('You have', guesses,'guesses. Goodluck.')
    print('Available letters:', avail_letters.upper())
    lg = str(input('Please guess a letter: ')).lower()
    ## Check for valid input
    while True:
        if lg.isalpha():
            break
        else:
            if warnings > 0:
                warnings -= 1
            else:
                guesses -= 1
            print('You have', warnings,'warnings left, and',guesses,'guesses left!')
            lg = str(input('Please enter a letter!: ')).lower()
    
    while guesses > 0:
        l_g.append(lg)
        underscore_LG = get_guessed_word(sw, l_g)
        avail_letters = get_available_letters(l_g)
        if is_word_guessed(sw, l_g):
            print('GOOD GUESS:', underscore_LG)
            print('_____________________________________________________')     #end of line
        else:
            ########################################################
            #### Testing to see if input was a vowel or otherwise ##
            ########################################################
            if lg in ['a', 'e', 'o', 'i']:
                guesses -= 2
            else:
                guesses -= 1
            print('TOUGH LUCK BUDDY! Try again:', underscore_LG)
            print('________________________________________________________') #end of line
            l_g.pop() #remove the last input coz it was the wrong guess
            
        ###############################################
        ##### Loop exiting statements #################
        ###############################################
        if str(sw) == str(get_guessed_word(sw, l_g)):
            secret_w = set(sw)
            unique_len = len(secret_w)
            score = guesses * unique_len
            print()
            print('CONGRATULATIONS, YOU WIN!')
            print('Your Score:', score)
            break
        if guesses == 0:
            break
        ###############################################
        #####user input
        
        print('You have:', warnings,'warnings left; and:',guesses,'guesses left.')
        #avail_letters = get_available_letters(l_g)
        print('Available letters:', avail_letters.upper())
        lg = str(input('Please guess a letter: ')).lower()
        ######################
        # if 'quit' is typed #
        ######################
        if lg == 'quit':
            print('Quiting...')
            break
        #####################
        
        ###Loop tests to see if user input is valid##
        while True:
            if lg in avail_letters:
                break
            elif lg not in avail_letters and lg.isalpha() :
                if warnings > 0: 
                    warnings -= 1
                else:
                    guesses -= 1
                print('You have', warnings,'warnings left, and',guesses,'guesses left!')
                lg = str(input('You have used this letter, guess again!: ')).lower()
                
            else:
                if warnings > 0:
                    warnings -= 1
                else:
                   guesses -= 1 
                print('You have', warnings,'warnings left, and',guesses,'guesses left!')
                lg = str(input('Please enter a letter!: ')).lower()
                
        #############################################
        
    if guesses == 0:
        print('You Lost. The Word Was,', sw,'Try Again Next Time.')
    else:
        print('Done!')
        
            
        # letters_g = get_guessed_word(let_guess) #now we have letters guessed underscores
        # if is_word_guessed(sw, letters_g):
        
        
    



# When you've completed your hangman function, scroll down to the bottom
# of the file and uncomment the first two lines to test
#(hint: you might want to pick your own
# secret_word while you're doing your own testing)


# -----------------------------------



def match_with_gaps(my_word, other_word):
    '''
    my_word: string with _ characters, current guess of secret word
    other_word: string, regular English word
    returns: boolean, True if all the actual letters of my_word match the 
        corresponding letters of other_word, or the letter is the special symbol
        _ , and my_word and other_word are of the same length;
        False otherwise: 
    '''
    
    stripd_word = ''
    for c in my_word:
        stripd_word += c.strip()
        
    index1 = 0
    true_counter = 0
    letter_counter = 0
    index2 = 0
        
    if len(stripd_word) == len(other_word):
        for c in stripd_word:
            if c.isalpha():
                letter_counter += 1
            index1 += 1
            index2 = 0
            for l in other_word:
                index2 += 1
                if (c == l) and (index1 == index2):
                    true_counter += 1
                    
    if (true_counter == letter_counter) and true_counter>0 and letter_counter >0:
        return True
    else:
        return False



def show_possible_matches(my_word):
    '''
    my_word: string with _ characters, current guess of secret word
    returns: nothing, but should print out every word in wordlist that matches my_word
             Keep in mind that in hangman when a letter is guessed, all the positions
             at which that letter occurs in the secret word are revealed.
             Therefore, the hidden letter(_ ) cannot be one of the letters in the word
             that has already been revealed.

    '''
    #strip my word
    stripd_w = ''
    for c in my_word:
        stripd_w += c.strip()
    
    possible_words = []
    for strng in wordlist:
        if match_with_gaps(stripd_w, strng):
            possible_words.append(strng)
    print('#################################################################')
    print(possible_words)
    print('#################################################################')



def hangman_with_hints(secret_word):
    '''
    secret_word: string, the secret word to guess.
    
    Starts up an interactive game of Hangman.
    
    * At the start of the game, let the user know how many 
      letters the secret_word contains and how many guesses s/he starts with.
      
    * The user should start with 6 guesses
    
    * Before each round, you should display to the user how many guesses
      s/he has left and the letters that the user has not yet guessed.
    
    * Ask the user to supply one guess per round. Make sure to check that the user guesses a letter
      
    * The user should receive feedback immediately after each guess 
      about whether their guess appears in the computer's word.

    * After each guess, you should display to the user the 
      partially guessed word so far.
      
    * If the guess is the symbol *, print out all words in wordlist that
      matches the current guessed word. 
    
    Follows the other limitations detailed in the problem write-up.
    '''
    secretW_len = len(secret_word)
    l_g = []    #letters guessed
    sw = secret_word    #secret word
    guesses = 6
    warnings = 3
    
    avail_letters = get_available_letters(l_g)
    print('Welcome to Hangman with hints, to Quit type "quit" and to get a hint type "*".')
    print('The secret word is', secretW_len,'letters long.\n')
    print('You have', guesses,'guesses. Goodluck.')
    print('Available letters:', avail_letters.upper())
    lg = str(input('Please guess a letter: ')).lower()
    ## Check for valid input
    while True:
        if lg.isalpha():
            break
        else:
            if warnings > 0:
                warnings -= 1
            else:
                guesses -= 1
            print('You have', warnings,'warnings left, and',guesses,'guesses left!')
            lg = str(input('Please enter a letter, to start the game!: ')).lower()
    
    while guesses > 0:
        if lg == '*':
            pass
        else:
            l_g.append(lg)
        underscore_LG = get_guessed_word(sw, l_g)
        avail_letters = get_available_letters(l_g)
        if is_word_guessed(sw, l_g):
            print('GOOD GUESS:', underscore_LG)
            print('_____________________________________________________')     #end of line
        elif lg == '*':
            pass
        else:
            ########################################################
            #### Testing to see if input was a vowel or otherwise ##
            ########################################################
            if lg in ['a', 'e', 'o', 'i']:
                guesses -= 2
            else:
                guesses -= 1
            print('TOUGH LUCK BUDDY! Try again:', underscore_LG)
            print('________________________________________________________') #end of line
            l_g.pop() #remove the last input coz it was the wrong guess
            
        ###############################################
        ##### Loop exiting statements #################
        ###############################################
        if str(sw) == str(get_guessed_word(sw, l_g)):
            secret_w = set(sw)
            unique_len = len(secret_w)
            score = guesses * unique_len
            print()
            print('CONGRATULATIONS, YOU WIN!')
            print('Your Score:', score)
            break
        if guesses == 0:
            break
        ###############################################
        #####user input
        
        print('You have:', warnings,'warnings left; and:',guesses,'guesses left.')
        #avail_letters = get_available_letters(l_g)
        print('Available letters:', avail_letters.upper())
        lg = str(input('Please guess a letter: ')).lower()
        
        if lg == '*':
            show_possible_matches(underscore_LG)
        ######################
        # if 'quit' is typed #
        ######################
        if lg == 'quit':
            print('Quiting...')
            break
        #####################
        
        ###Loop tests to see if user input is valid##
        while True:
            if lg in avail_letters or lg == '*':
                break
            elif lg not in avail_letters and lg.isalpha() :
                if warnings > 0: 
                    warnings -= 1
                else:
                    guesses -= 1
                print('You have', warnings,'warnings left, and',guesses,'guesses left!')
                lg = str(input('You have used this letter, guess again!: ')).lower()
                
            else:
                if warnings > 0:
                    warnings -= 1
                else:
                   guesses -= 1 
                print('You have', warnings,'warnings left, and',guesses,'guesses left!')
                lg = str(input('Please enter a letter!: ')).lower()
                
        #############################################
        
    if guesses == 0:
        print('You Lost. The Word Was,', sw,'Try Again Next Time.')
    else:
        print('Done!')
    pass
   
    



# When you've completed your hangman_with_hint function, comment the two similar
# lines above that were used to run the hangman function, and then uncomment
# these two lines and run this file to test!
# Hint: You might want to pick your own secret_word while you're testing.


if __name__ == "__main__":
    # pass

    # To test part 2, comment out the pass line above and
    # uncomment the following two lines.
    
    #secret_word = 'apple'
    #secret_word = choose_word(wordlist)
    #hangman(secret_word)

###############
    
    # To test part 3 re-comment out the above lines and 
    # uncomment the following two lines. 
    
    #secret_word = 'apple'
    secret_word = choose_word(wordlist)
    hangman_with_hints(secret_word)
