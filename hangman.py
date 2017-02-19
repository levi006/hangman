import random, requests

def get_word_list():
    """Pings the API to get a word list filtered by difficulty level"""

    while True:    
        level = raw_input(
            'Please select the difficulty level, from 1-10, where 1 is easy and 10 is the most difficult.')

        if level.isdigit() and 1 <= int(level) <= 10:
            break

        else:
            print "Only integers from 1-10 please!"

    # max_length = raw_input('Please select the max length of the generated word.')
    # min_length = raw_input('Please select the min length of the generated word.')
    payload = {"difficulty": level}
    url = 'http://linkedin-reach.hagbpyjegb.us-west-2.elasticbeanstalk.com/words'

    response = requests.get(url, params = payload)
    words = response.text.splitlines()

    return words

def prompt_guess():
    """Checks user  and restricts user input to alphabetic characters only. """
    
    while True:    
        guess = raw_input("Guess a letter: ")
        raw_ltr = guess.strip().lower()

        if not raw_ltr.isalpha():
            print "oh noes only letters"
        else:
            return raw_ltr

def display_hangman(secret_word, guessed_letters):
    """Prints out empty dashes for each character of the secret word and displays a running list of incorrectly guessed letters."""
    board = ""
    for ltr in secret_word:
        if ltr in guessed_letters:
            board += ltr
        else:
            board += "_"
    print " ".join(board)

    print "You've guessed: " + " ".join(sorted(guessed_letters))

    # guessed_letters.add(legal_ltr)
    # mistakes = ' '.join(guessed_letters)
    # print "You have guessed these letters: %s " % mistakes
    # print ' '.join(answer)  
    # return

def initiate_board(secret_word):
    for i in range(len(secret_word)):
        print "_ " * max(range(len(secret_word)))
        return

def play_round(words):
    """Contains the game play logic and messaging as game progresses."""
    guesses_remaining = 6
    guessed_letters = set()
    secret_word = random.choice(words) # "apple"  # get_random_word(level)
    # print secret_word

    initiate_board(secret_word)

    while True:

        ltr = prompt_guess()

        if ltr == secret_word:
            print "Didn't need all the guesses, did you?"
            return True

        elif len(ltr) != 1:
            print "That wasn't the secret word. Try entering one letter at a time if you're not sure what the word is."
            continue

        if ltr in guessed_letters:
            if guesses_remaining == 1:
                msg = "You still have one guess left"
            else:
                msg = "You have %d guesses left" % guesses_remaining
            print "You've already la la la. " + msg
            continue

        guessed_letters.add(ltr)

        if ltr in secret_word:
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
    return secret_word
          

def play():
    """Lays out the general game sequence and resets a new game."""
    words = get_word_list()

    while True:
        result = play_round(words)
        if result:
            print "Hooray!You've won!"
            print "The secret word was %s." % secret_word
        else:
            print "The gallows for you! The answer was '%s'." % secret_word

        again = raw_input("Play again? ")
        if again.lower().startswith("n" or "q"):
            print "Thanks for playing!"
            break
        else:
            print "One hot new challenge coming up!"  

if __name__ == "__main__":
    play()


# while won == False and guess_count > 0:

#     legal_ltr = prompt_guess(guess)

#     if legal_ltr == secret_word:
#         print "Didn't need all the guesses, did you?"
#         won = True
#         break
 







