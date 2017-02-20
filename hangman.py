import random, requests
from collections import defaultdict



def play():
    """Lays out the general game sequence and resets a new game."""

    while True:
        words = get_word_list()
        secret_word = random.choice(words)
        result = play_round(words, secret_word)

        if result:
            print "'Hooray!You've won! The secret word was '%s.'" % secret_word
        else:
            print "The gallows for you! The answer was '%s'." % secret_word

        again = raw_input("Play again? [y/n]")
        if again.lower().startswith("n" or "q"):
            print "Thanks for playing!"
            break
        else:
            print "One hot new challenge coming up!" 

    return

def play_round(words, secret_word):
    """Contains the game play logic and messaging as game progresses."""
    guesses_remaining = 6
    guessed_letters = set()
    initiate_board(secret_word)

    while True:

        guessed_ltr = prompt_guess()
        evil_hangman(guessed_ltr, words, secret_word)
        print "SECRET WORD AFTER EVIL HANGMAN " + secret_word

        if guessed_ltr == secret_word:
            print "Didn't need all the guesses, did you?"
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
                return True

        else:
            guesses_remaining -= 1

            if guesses_remaining == 0:
                return False 

            if guesses_remaining == 1:
                msg = "Only one guess left! Make it count!"
            else:
                msg = "Yikes! You now have %s guesses left." % guesses_remaining
            print msg

        display_hangman(secret_word, guessed_letters)
    return

def evil_hangman(guessed_ltr, words, secret_word):
    print "IN EVIL HANGMAN"
    print "This is SECRET WORD " + secret_word

    def make_word_bank(words, secret_word):
        """Construct word bank of all words the same length as secret word"""
        word_bank = []
        for word in words:
            if len(word) == len(secret_word):
                word_bank.append(word)
        print "This is length of word bank: " + str(len(word_bank))
        print "This is length of words in word bank: " + str(len(word_bank[0]))
        print "This is length of words in word bank: " + str(len(word_bank[345]))
        return word_bank
    
    def switch_secret_word(guessed_ltr, word_bank):
        print "IN SWITCHING SECRET WORD"
        word_families = defaultdict(list)
        for word in word_bank:
            indices = []
            for ltr in range(0, len(word)):
                if word[ltr] == guessed_ltr:
                    indices.append(ltr)
            word_families[tuple(indices)].append(word)
        word_bank = max(word_families.values(), key=lambda fam: len(fam))
        word = random.choice(word_bank)
        secret_word = word
        print "This is NEW SECRET WORD " + secret_word
        return 
    
    make_word_bank(words, secret_word)
    switch_secret_word(guessed_ltr, word_bank)
    return secret_word

def get_word_list():
    """Pings the API to get a word list filtered by difficulty level. Also asks user to select the difficulty level based on a 1-10 scale."""

    while True:    
        level = raw_input('Please select the difficulty level, from 1-10, where 1 is easy and 10 is the most difficult.')

        if level.isdigit() and 1 <= int(level) <= 10:
            break

        else:
            print "Only integers from 1-10 please!"

    payload = {"difficulty": level}
    url = 'http://linkedin-reach.hagbpyjegb.us-west-2.elasticbeanstalk.com/words'

    response = requests.get(url, params = payload)
    words = response.text.splitlines()

    return words

def prompt_guess():
    """Asks user for guess and validates guess. """
    
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
    """Updates board with filled and empty dashes for the secret word and displays a running list of incorrectly guessed letters."""
    board = ""
    for ltr in secret_word:
        if ltr in guessed_letters:
            board += ltr
        else:
            board += "_"
    print " ".join(board)
    print "You've guessed: " + " ".join(sorted(guessed_letters))
    return

if __name__ == "__main__":
    play()







