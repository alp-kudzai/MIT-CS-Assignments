# Problem Set 4B
# Name: <your name here>
# Collaborators:
# Time Spent: x:xx

import string
import time
### HELPER CODE ###
def load_words(file_name):
    '''
    file_name (string): the name of the file containing 
    the list of words to load    
    
    Returns: a list of valid words. Words are strings of lowercase letters.
    
    Depending on the size of the word list, this function may
    take a while to finish.
    '''
    print("Loading word list from file...")
    # inFile: file
    inFile = open(file_name, 'r')
    # wordlist: list of strings
    wordlist = []
    for line in inFile:
        wordlist.extend([word.lower() for word in line.split(' ')])
    print("  ", len(wordlist), "words loaded.")
    return wordlist

def is_word(word_list, word):
    '''
    Determines if word is a valid word, ignoring
    capitalization and punctuation

    word_list (list): list of words in the dictionary.
    word (string): a possible word.
    
    Returns: True if word is in word_list, False otherwise

    Example:
    >>> is_word(word_list, 'bat') returns
    True
    >>> is_word(word_list, 'asdf') returns
    False
    '''
    word = word.lower()
    word = word.strip(" !@#$%^&*()-_+={}[]|\:;'<>?,./\"")
    return word in word_list

def get_story_string():
    """
    Returns: a story in encrypted text.
    """
    f = open("story.txt", "r")
    story = str(f.read())
    f.close()
    return story

### END HELPER CODE ###

WORDLIST_FILENAME = 'words.txt'

class Message(object):
    def __init__(self, text):
        '''
        Initializes a Message object
                
        text (string): the message's text

        a Message object has two attributes:
            self.message_text (string, determined by input text)
            self.valid_words (list, determined using helper function load_words)
        '''
        self.messsage_text = text
        self.valid_words = load_words(WORDLIST_FILENAME)

    def get_message_text(self):
        '''
        Used to safely access self.message_text outside of the class
        
        Returns: self.message_text
        '''
        self.copy_messageText = self.messsage_text[:]
        return self.copy_messageText

    def get_valid_words(self):
        '''
        Used to safely access a copy of self.valid_words outside of the class.
        This helps you avoid accidentally mutating class attributes.
        
        Returns: a COPY of self.valid_words
        '''
        self.copy_validWords = self.valid_words[:]
        return self.copy_validWords

    def build_shift_dict(self, shift):
        '''
        Creates a dictionary that can be used to apply a cipher to a letter.
        The dictionary maps every uppercase and lowercase letter to a
        character shifted down the alphabet by the input shift. The dictionary
        should have 52 keys of all the uppercase letters and all the lowercase
        letters only.        
        
        shift (integer): the amount by which to shift every letter of the 
        alphabet. 0 <= shift < 26

        Returns: a dictionary mapping a letter (string) to 
                 another letter (string). 
        '''
        
        # cases = string.ascii_lowercase + string.ascii_uppercase
        lower = string.ascii_lowercase
        upper = string.ascii_uppercase
        self.shift_dict = {}
        for l in range(len(lower)):
            if (l+shift <= (len(lower) - 1)):
                self.shift_dict[lower[l]] = lower[l + shift]
            else:
                new_lshift = shift - (len(lower) - l) #here i am subtr 26 for the
                #position of the letter that is to be shifted, then
                #subtr that from the shift var to get the new position
                #that wraps back to the beginning of the alphabet.
                self.shift_dict[lower[l]] = lower[new_lshift]
                
        for L in range(len(upper)):
            if (L + shift) <= (len(upper) - 1):
                self.shift_dict[upper[L]] = upper[L + shift]
            else:
                new_Lshift = shift - (len(upper) - L)
                self.shift_dict[upper[L]] = upper[new_Lshift]
        return self.shift_dict
    
    def apply_shift(self, shift):
        '''
        Applies the Caesar Cipher to self.message_text with the input shift.
        Creates a new string that is self.message_text shifted down the
        alphabet by some number of characters determined by the input shift        
        
        shift (integer): the shift with which to encrypt the message.
        0 <= shift < 26

        Returns: the message text (string) in which every character is shifted
             down the alphabet by the input shift
        '''
        cypher_dict = Message.build_shift_dict(self, shift)
        self.newCyph_message = ''
        for l in self.messsage_text:
            if l.isalpha():
               self.newCyph_message += cypher_dict[l]
            else:
                self.newCyph_message += l
        return self.newCyph_message
                
        
    
    def __str__(self):
        return 'Message:'+self.messsage_text+''

class PlaintextMessage(Message):
    def __init__(self, text, shift):
        '''
        Initializes a PlaintextMessage object        
        
        text (string): the message's text
        shift (integer): the shift associated with this message

        A PlaintextMessage object inherits from Message and has five attributes:
            self.message_text (string, determined by input text)
            self.valid_words (list, determined using helper function load_words)
            self.shift (integer, determined by input shift)
            self.shift_dict (dictionary, built using shift)
            self.message_text_encrypted (string, created using shift)

        '''
        Message.__init__(self, text)
        self.shift = shift

    def get_shift(self):
        '''
        Used to safely access self.shift outside of the class
        
        Returns: self.shift
        '''
        return self.shift

    def get_encryption_dict(self):
        '''
        Used to safely access a copy self.encryption_dict outside of the class
        
        Returns: a COPY of self.encryption_dict
        '''
        copy_shiftDict = self.build_shift_dict(self.shift)
        return copy_shiftDict
        # copy_shiftDict = self.shift_dict[:]
        # return copy_shiftDict
        

    def get_message_text_encrypted(self):
        '''
        Used to safely access self.message_text_encrypted outside of the class
        
        Returns: self.message_text_encrypted
        '''
        copy_newCyphMessage = self.apply_shift(self.shift)
        return copy_newCyphMessage
    
    def change_shift(self, shift):
        '''
        Changes self.shift of the PlaintextMessage and updates other 
        attributes determined by shift.        
        
        shift (integer): the new shift that should be associated with this message.
        0 <= shift < 26

        Returns: nothing
        '''
        self.shift = shift
        self.shift_dict = self.build_shift_dict(self.shift)
        self.newCyph_message = self.apply_shift(self.shift)
        


class CiphertextMessage(Message):
    def __init__(self, text):
        '''
        Initializes a CiphertextMessage object
                
        text (string): the message's text

        a CiphertextMessage object has two attributes:
            self.message_text (string, determined by input text)
            self.valid_words (list, determined using helper function load_words)
        '''
        Message.__init__(self, text)

    def decrypt_message(self):
        '''
        Decrypt self.message_text by trying every possible shift value
        and find the "best" one. We will define "best" as the shift that
        creates the maximum number of real words when we use apply_shift(shift)
        on the message text. If s is the original shift value used to encrypt
        the message, then we would expect 26 - s to be the best shift value 
        for decrypting it.

        Note: if multiple shifts are equally good such that they all create 
        the maximum number of valid words, you may choose any of those shifts 
        (and their corresponding decrypted messages) to return

        Returns: a tuple of the best shift value used to decrypt the message
        and the decrypted message text using that shift value
        '''
        text = self.get_message_text()
        # print(len(text))
        
        valid_words = self.get_valid_words()
        
        shift_container = ()
        best_shift = ''
        for i in range(1, 27):
            word_counter = 0
            real_words = ''
            contain = self.apply_shift((26-i))
            # print(i)
            # print(contain)
            if ' ' in contain:
                word_con = contain.split(' ')
                for word in word_con:
                    # if word in valid_words:
                    if is_word(self.valid_words, word):
                        # print(word)
                        real_words += word+' '
                        word_counter += 1
                # print(word_counter)
                # print(len(word_con))
                # if len(real_words) > len(best_shift):
                #     best_shift = real_words
                if len(real_words) > len(best_shift):    
                # if (len(word_con)-3) <= word_counter <= len(text):
                    #good shift value
                    best_shift = real_words
                    shift_container += (26-i, best_shift)
                    # print(shift_container)
            else:
                if is_word(valid_words, contain):
                    shift_container += ((26-i), contain)
                    # print(shift_container)
        if len(shift_container) > 1:
            return (shift_container[-2], shift_container[-1])
        elif len(shift_container) == 1:
            return shift_container
        else:
            return print('Oops')
        
if __name__ == '__main__':

#    #Example test case (PlaintextMessage)
    # plaintext = PlaintextMessage('hello', 2)
    # print('Expected Output: jgnnq')
    # print('Actual Output:', plaintext.get_message_text_encrypted())
#
#    #Example test case (CiphertextMessage)
    # ciphertext = CiphertextMessage('jgnnq')
    # print('Expected Output:', (24, 'hello'))
    # print('Actual Output:', ciphertext.decrypt_message())
    
    # ciphertext = CiphertextMessage('P ht pu whpu, tf ihjr rpuk vm obyaz.')
    # print('Expected Output:', (19, 'I am in pain, my back kid of hurts.'))
    # print('Actual Output:', ciphertext.decrypt_message())

    #TODO: WRITE YOUR TEST CASES HERE

    #TODO: best shift value and unencrypted story
    start = time.time()
    story_cyp = CiphertextMessage(get_story_string())
    print(story_cyp)
    print('Translation: ', story_cyp.decrypt_message())
    end = time.time()
    print(f'Time: {end - start}')
    
    #(12, 'Jack is a mythical character created on the spur of a moment 
    #to help cover an planned hack. He has been registered for classes 
    #at twice before, but has reportedly never passed It has been
    #the tradition of the residents of East Campus to 
    #become Jack for a few nights year to educate incoming 
    #students in the ways, means, and ethics of hacking. ')
    
    
    
