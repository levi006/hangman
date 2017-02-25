"""Evil Hangman."""

import random, requests, sys, time, select
from collections import defaultdict
from gallows import GALLOWS


def set_timer():
    """Choose whether to play with timed guesses."""

    while True:
        answer = str(raw_input('Would you like use timed guesses? [y/n] ')).lower().strip()


        if answer == 'y':
            print "You have 10 seconds per guess."
            return True
        elif answer == 'n':
            print "Who needs the extra stress?"
            return False
        else:
            print "Please enter 'y' or 'n'."

def set_is_evil():
    """Choose difficulty level and get list of words from API for that level.

        >>> from testutils import test_input

        >>> test_input("maybe", "y")

        >>> set_is_evil()
        Would you like to play on evil mode? [y/n] Please enter 'y' or 'n'.
        Would you like to play on evil mode? [y/n] Evil mode on! MUAHAHA!
        True

        >>> test_input("n")

        >>> set_is_evil()
        Would you like to play on evil mode? [y/n] Vanilla Hangman it is!
        False
    """

    while True:
        answer = str(raw_input('Would you like to play on evil mode? [y/n] ')).lower().strip()


        if answer == 'y':
            print "Evil mode on! MUAHAHA!"
            return True
        elif answer == 'n':
            print "Vanilla Hangman it is!"
            return False
        else:
            print "Please enter 'y' or 'n'."


def set_difficulty_level():
    """Choose difficulty level and get list of words from API for that level.
        
        >>> from testutils import test_input
        
        >>> test_input("frog", "11", "3")
        
        >>> set_difficulty_level()
        Select the difficulty level (1=easiest to 10=hardest): Only integers from 1-10 please!
        Select the difficulty level (1=easiest to 10=hardest): Only integers from 1-10 please!
        Select the difficulty level (1=easiest to 10=hardest): 3
    """

    while True:    
        level = raw_input('Select the difficulty level (1=easiest to 10=hardest): ')

        if level.isdigit() and 1 <= int(level) <= 10:
            return int(level)
        else:    
            print "Only integers from 1-10 please!"


def display_hangman(secret_word, guessed_letters):
    """Updates board with filled and empty dashes for the secret word and displays a running list of incorrectly guessed letters.
    
    >>> secret_word = "cat"
    >>> guessed_letters = "c"
    >>> display_hangman(secret_word, guessed_letters)
    c _ _
    You've guessed: c

    >>> secret_word = "dog"
    >>> guessed_letters = "e","s"
    >>> display_hangman(secret_word, guessed_letters)
    _ _ _
    You've guessed: e s

    >>> secret_word = "mat"
    >>> guessed_letters = "m","t", "a"
    >>> display_hangman(secret_word, guessed_letters)
    m a t
    You've guessed: a m t

    """

    board = ""
    for ltr in secret_word:
        if ltr in guessed_letters:
            board += ltr
        else:
            board += "_"

    print " ".join(board)
    print "You've guessed: " + " ".join(sorted(guessed_letters))


def draw_gallows(guesses_remaining):
    """Prints corresponding ASCII art with each turn.
    
    >>> guesses_remaining = 0
    >>> draw_gallows(guesses_remaining)
    <BLANKLINE>
     _______
    |   |  \|
        O   |
       \|/  |
        |   |
       / \  |
            |
            |
           ---

    >>> guesses_remaining = 6
    >>> draw_gallows(guesses_remaining)
    <BLANKLINE>
     _______
    |      \|
            |
            |
            |
            |
            |
            |
           ---
    """

    print GALLOWS[guesses_remaining] 

def get_word_list(level):
    """Choose difficulty level and get list of words from API for that level."""

    params = {"difficulty": level}
    URL = 'http://linkedin-reach.hagbpyjegb.us-west-2.elasticbeanstalk.com/words'

    response = requests.get(URL, params=params)
    
    words = response.text.splitlines()

    return words


def prompt_guess(timer, guesses_remaining):
    """Asks user for guess and validates guess."""

    if timer == False:    
        guess = raw_input("Guess a letter: ")
        raw_ltr = guess.strip().lower()

        if not raw_ltr.isalpha():
            print "Only enter letters, please."
        else:
            return raw_ltr

    if timer == True:
        left = 10

        while left:
            print "\rYou have ten seconds to guess: %ss " % left,
            sys.stdout.flush()
     
            stdin_ready, _, _ = select.select([sys.stdin], [], [], 1)

            if stdin_ready:

                raw_ltr = raw_input().strip().lower()

                if not raw_ltr.isalpha():
                    print "Only enter letters, please."
                
                else:
                    return raw_ltr 
            
            left -= 1  
        
        return None               
                
def generate_word_bank(guessed_ltr, words):
    """Builds a new word bank based on a guessed letter each turn. 

    Given a word bank of possible words, find the list of words that include the guessed letter
    and which have the longest-set of matching locations of the letter. Choose one randomly
    and return it along with the newly-reduced word bank.

    Evil use cases:

        # >>> word_bank = ["can", "con", "non", "coy", "alf", "aaa"]
        # >>> generate_word_bank("n", word_bank)
        # ['coy', 'alf', 'aaa']

        >>> word_bank = ["can", "con", "non"]
        >>> generate_word_bank("c", word_bank)
        ['can', 'con']
    """

    word_families = defaultdict(list)

    for word in words:

        # find locations of guessed letter in word
        indices = [i for i, ltr in enumerate(word) if ltr == guessed_ltr]

        # {(0, 2): ["non"], (2,): ["can", "con"]}
        indices_words = word_families[tuple(indices)].append(word)

    # find family with most words (eg ["can", "con"])
    words = max(word_families.values(), key=lambda fam: len(fam))

    # print("word_bank:", words)
 
    return words 


def play_round(words, is_evil, timer):
    """Contains the game play logic and messaging as game progresses.

    For tests of this function, see tests.txt.
    """

    secret_word = random.choice(words)
    
    guesses_remaining = 6
    guessed_letters = set()

    draw_gallows(guesses_remaining)    
    display_hangman(secret_word, guessed_letters)

    while True:

        guessed_ltr = prompt_guess(timer, guesses_remaining)


        if guessed_ltr == secret_word:
            print "Didn't need all the guesses, did you?"
            print "'Hooray!You've won! The secret word was '%s.'" % secret_word
            return True

        # Validate input

        elif guessed_ltr == None:
            guesses_remaining -= 1
            print "\nTime's up! You now have %d guesses left." % guesses_remaining
            continue

        if len(guessed_ltr) != 1:
            print "That wasn't the secret word. Try entering one letter at a time if you're not sure what the word is."
            guesses_remaining -= 1
            msg = "You have %d guesses left." % guesses_remaining
            print msg
            continue

        if guessed_ltr in guessed_letters:
            if guesses_remaining == 1:
                print "You still have one guess left."  
            else:
                print "You've already guessed this letter." + msg         
            continue

        # if evil, reduce word list

        if is_evil:
            words = generate_word_bank(guessed_ltr, words)
            secret_word = words[0]

        # print "SECRET WORD " + secret_word

        guessed_letters.add(guessed_ltr)

        if guessed_ltr in secret_word:
            print "Correct!"
            if not(set(secret_word) - guessed_letters):
            # if all(c in guessed_letter for c in secret_word):

                # They have guessed every correct letter
                print "Hooray! You've won! The secret word was '%s'." % secret_word
                return True
        else:
            # wrong guess
            guesses_remaining -= 1

            if guesses_remaining == 0:
                draw_gallows(guesses_remaining)
                print "The gallows for you! The answer was '%s'." % secret_word
                return False 

            if guesses_remaining == 1:
                msg = "Only one guess left! Make it count!"
            else:
                msg = "You now have %s guesses left." % guesses_remaining
            print msg

            draw_gallows(guesses_remaining)
        display_hangman(secret_word, guessed_letters)
   

def play():
    """Lays out the general game sequence and resets a new game."""

    print "Welcome to Hangman!"

    while True:
        is_evil = set_is_evil()
        timer = set_timer()
        level = set_difficulty_level()
        words = get_word_list(level)
        

        if is_evil == True:
            # For the evil variant, the list of words all has to
            # be the same length.
            word_lens = [len(w) for w in words]
            word_len = random.randint(min(word_lens), max(word_lens))
            words = [w for w in words if len(w) == word_len]

        result = play_round(words, is_evil, timer)

        if result:
            print "Congratulations!"

        else:
            print "Better luck next time!"
 
        again = raw_input("Play again? [y/n]").lower()
 
        if again.startswith("n") or again.startswith("q"):
            print "Thanks for playing!"
            return
        
        print "One hot new challenge coming up!"


if __name__ == "__main__":
    play()







