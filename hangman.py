import random, requests
from collections import defaultdict



def play():
    """Lays out the general game sequence and resets a new game."""

    while True:
        words = get_word_list()
        secret_word = random.choice(words)
        result = play_round(words, secret_word)

        if result:

            again = raw_input("Play again? [y/n]")
            if again.lower().startswith("n" or "q"):
                print "Thanks for playing!"
                break
        else:
            print "One hot new challenge coming up!" 

    return

def play_round(words, secret_word, is_evil=True):
    """Contains the game play logic and messaging as game progresses."""
    
    guesses_remaining = 6
    guessed_letters = set()
    initiate_board(secret_word)
    draw_gallows(guesses_remaining)    

    if is_evil:
        word_bank = make_word_bank(words, secret_word)
        print "WORD BANK: %s %s" % (len(word_bank), word_bank)
        print "SECRET WORD " + secret_word

    while True:

        guessed_ltr = prompt_guess()

        if is_evil and guessed_ltr in secret_word:
            secret_word, word_bank = switch_secret_word(guessed_ltr, word_bank)        
            print "Correct!"
            print "WORD BANK: %s %s" % (len(word_bank), word_bank)
            print "SECRET WORD AFTER EVIL HANGMAN " + secret_word

        if guessed_ltr == secret_word:
            print "Didn't need all the guesses, did you?"
            print "'Hooray!You've won! The secret word was '%s.'" % secret_word
            return True

        elif len(guessed_ltr) != 1:
            print "That wasn't the secret word. Try entering one letter at a time if you're not sure what the word is."
            continue

        if guessed_ltr in guessed_letters:
            if guesses_remaining == 1:
                msg = "You still have one guess left."
            else:
                msg = "You have %d guesses left." % guesses_remaining
            print "You've already guessed this letter. " + msg
            continue

        guessed_letters.add(guessed_ltr)

        if guessed_ltr in secret_word:
            print "Correct!"
            if not(set(secret_word) - guessed_letters):
                # They have guessed every correct letter
                print "Hooray! You've won! The secret word was '%s'." % secret_word
                return True

        else:
            guesses_remaining -= 1

            if guesses_remaining == 0:
                draw_gallows(guesses_remaining)
                print "The gallows for you! The answer was '%s'." % secret_word
                return False 

            if guesses_remaining == 1:
                msg = "Only one guess left! Make it count!"
            else:
                msg = "Yikes! You now have %s guesses left." % guesses_remaining
            print msg
            draw_gallows(guesses_remaining)
        display_hangman(secret_word, guessed_letters)
    return


def make_word_bank(words, secret_word):
    """Construct word bank of all words the same length as secret word.

        >>> make_word_bank(["ab", "aa", "ba", "foozle"], "ha")
        ['ab', 'aa', 'ba']
    """
    
    return [w for w in words if len(w) == len(secret_word)]    
    
def switch_secret_word(guessed_ltr, word_bank):
    """Find new secret word from word bank of possibilities. 

    Given a word bank of possible words, find the list of words that include the guessed letter
    and which have the longest-set of matching locations of the letter. Choose one randomly
    and return it along with the newly-reduced word bank.

        >>> wb = ["can", "con", "non", "coy", "alf", "aaa"]
        >>> switch_secret_word("n", wb)
        ('coy', ['coy', 'alf', 'aaa'])
    """

    word_families = defaultdict(list)

    for word in word_bank:

        # find locations of guessed letter in word
        indices = [i for i, ltr in enumerate(word) if ltr == guessed_ltr]
        
        # throw out words that include letter
        if not indices: 
            continue

        # {(0, 2): ["non"], (2,): ["can", "con"]}
        word_families[tuple(indices)].append(word)

    # find family with most words (eg ["can", "con"])
    word_bank = max(word_families.values(), key=lambda fam: len(fam))

    # word = random.choice(word_bank)
    word = word_bank[0]

    return (word, word_bank) 

def get_word_list():
    """Choose difficulty level and get list of words from API for that level."""

    while True:    
        level = raw_input('Select the difficulty level (1=easiest to 10=hardest)')

        if level.isdigit() and 1 <= int(level) <= 10:
            break

        print "Only integers from 1-10 please!"

    params = {"difficulty": level}
    URL = 'http://linkedin-reach.hagbpyjegb.us-west-2.elasticbeanstalk.com/words'

    response = requests.get(URL, params=params)
    words = response.text.splitlines()

    return words

def prompt_guess():
    """Asks user for guess and validates guess. 
        
        guess = "a"
        >>> prompt_guess("a")
        >>> "oh noes only letters"


    """
    
    while True:    
        guess = raw_input("Guess a letter: ")
        raw_ltr = guess.strip().lower()

        if not raw_ltr.isalpha():
            print "oh noes only letters"
        else:
            return raw_ltr

def initiate_board(secret_word):

    for i in range(len(secret_word)):
        print "_ " * max(range(len(secret_word)))
        return

def display_hangman(secret_word, guessed_letters):
    """Updates board with filled and empty dashes for the secret word and displays a running list of incorrectly guessed letters.



    """

    board = ""
    for ltr in secret_word:
        if ltr in guessed_letters:
            board += ltr
        else:
            board += "_"

    print " ".join(board)
    print "You've guessed: " + " ".join(sorted(guessed_letters))
    return

def draw_gallows(guesses_remaining):

    imgs = [
'''
 _______
|   |  \|
    O   |
   \|/  |
    |   |
   / \  |
        |
        |
       ---''',

'''
 _______
|   |  \|
    O   |
   \|/  |
    |   |
   /    |
        |
        |
       ---''',

'''
 _______
|   |  \|
    O   |
   \|/  |
    |   |
        |
        |
        |
       ---''',
'''
 _______
|   |  \|
    O   |
    |   |
    |   |
        |
        |
        |
       ---''',

'''
 _______
|   |  \|
    O   |
    |   |
    |   |
        |
        |
        |
       ---''',

 '''
 _______
|   |  \|
        |
        |
        |
        |
        |
        |
       ---''',
'''
 _______
|      \|
        |
        |
        |
        |
        |
        |
       ---''']

    print imgs[guesses_remaining]
    return

if __name__ == "__main__":
    play()







