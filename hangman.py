import random, requests
from collections import defaultdict
from gallows import GALLOWS


def play(is_evil=True):
    """Lays out the general game sequence and resets a new game."""
    

    while True:
        set_is_evil()
        level = set_difficulty_level()
        words = get_word_list(level)
        

        if is_evil:
            # For the evil variant, the list of words all has to
            # be the same length.
            word_lens = [len(w) for w in words]
            word_len = random.randint(min(word_lens), max(word_lens))
            words = [w for w in words if len(w) == word_len]

        result = play_round(words, is_evil)

        if result:
            print "Congratulations!"

        else:
            print "Better luck next time!"
 
        again = raw_input("Play again? [y/n]").lower()
 
        if again.startswith("n") or again.startswith("q"):
            print "Thanks for playing!"
            return
        
        print "One hot new challenge coming up!" 



def play_round(words, is_evil):

    """Contains the game play logic and messaging as game progresses."""

    secret_word = random.choice(words)
    
    guesses_remaining = 6
    guessed_letters = set()

    draw_gallows(guesses_remaining)    
    display_hangman(secret_word, guessed_letters)


    while True:

        guessed_ltr = prompt_guess()

        if guessed_ltr == secret_word:
            print "Didn't need all the guesses, did you?"
            print "'Hooray!You've won! The secret word was '%s.'" % secret_word
            return True

        # Validate input

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

        # if evil, reduce our word list

        if is_evil:
            words = generate_word_bank(guessed_ltr, words)
            secret_word = random.choice(words)

        # print "WORD BANK: %s %s" % (len(word_bank), word_bank)
        print "SECRET WORD " + secret_word

        guessed_letters.add(guessed_ltr)

        if guessed_ltr in secret_word:
            print "Correct!"
            if not(set(secret_word) - guessed_letters):
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
                msg = "Yikes! You now have %s guesses left." % guesses_remaining

            print msg
            draw_gallows(guesses_remaining)

        display_hangman(secret_word, guessed_letters)

    
def generate_word_bank(guessed_ltr, words):
    """Builds a new word bank based on a guessed letter each turn. 

    Given a word bank of possible words, find the list of words that include the guessed letter
    and which have the longest-set of matching locations of the letter. Choose one randomly
    and return it along with the newly-reduced word bank.

        >>> wb = ["can", "con", "non", "coy", "alf", "aaa"]
        >>> switch_secret_word("n", wb)
        ['coy', 'alf', 'aaa']
    """

    word_families = defaultdict(list)

    for word in words:

        # find locations of guessed letter in word
        indices = [i for i, ltr in enumerate(word) if ltr == guessed_ltr]
        
        # {(0, 2): ["non"], (2,): ["can", "con"]}
        indices_words = word_families[tuple(indices)].append(word)
        print type(indices_words)
    # find family with most words (eg ["can", "con"])
 
    words = max(word_families.values(), key=lambda fam: len(fam))
    print("word_bank:", words)
 
    return words 

def set_difficulty_level():
    """Choose difficulty level and get list of words from API for that level."""

    while True:    
        level = raw_input('Select the difficulty level (1=easiest to 10=hardest)')

        if level.isdigit() and 1 <= int(level) <= 10:
            return int(level)

        print "Only integers from 1-10 please!"

def set_is_evil():
    """Choose difficulty level and get list of words from API for that level."""
   
    answer = raw_input('Hi! Welcome to Hangman! Would you like to play on evil mode?[y/n]')

    if answer == 'y':
        is_evil = True
        print "Evil mode on! MUAHAHA!"
    else: 
        is_evil = False
        print "Vanilla it is!"

    return is_evil   

def get_word_list(level):
    """Choose difficulty level and get list of words from API for that level."""

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


def draw_gallows(guesses_remaining):
    print GALLOWS[guesses_remaining]


if __name__ == "__main__":
    play()







