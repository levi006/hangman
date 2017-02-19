import random, requests

def set_difficulty_settings():
    while True:    
        difficulty_level = raw_input('Please select the difficulty level, from 1-10, where 1 is easy and 10 is the most difficult.')
        print difficulty_level.decode('utf-8')
        print type(difficulty_level.decode('utf-8'))
        if not difficulty_level.decode('utf-8').isnumeric() and 1 <= int(difficulty_level) <= 10:
            print "oh noes only numbers from 1-10"
        else:
            break
            return difficulty_level

    max_length = raw_input('Please select the max length of the generated word.')
    min_length = raw_input('Please select the min length of the generated word.')

    payload = {'difficulty': difficulty_level,
                        'maxLength': max_length,
                        'minLength': min_length, 
                        }
    print payload                   
    return payload

def generate_word():
    # words = ['apple']
    payload = set_difficulty_settings()
    response = requests.get(url, params = payload)
    words = response.text.splitlines()
    word_index = random.randrange(0, len(words))
    chosen_word = words[word_index]
    return chosen_word

#evaluate if guessed letter is a alphabetic
def eval_alpha(guess):
    
    while True:    
        guess = raw_input("Guess a letter: ")
        raw_ltr = guess.strip().lower()

        if not raw_ltr.isalpha():
            print "oh noes only letters <-- (OMG MY BF WROTE THIS BC HE IS SO TWEE)"
        else:
            return raw_ltr

def display_hangman():
    guessed_letters.add(legal_ltr)
    mistakes = ' '.join(guessed_letters)
    print "You have guessed these letters: %s " % mistakes
    print ' '.join(answer)  
    return

def initiate_board(secret_word):
    for i in range(len(secret_word)):
        print "_ " * max(range(len(secret_word)))
        return

#Gameplay

url = 'http://linkedin-reach.hagbpyjegb.us-west-2.elasticbeanstalk.com/words'
secret_word = generate_word()
initiate_board(secret_word)
#correct letters = { letter : {count, found status}}
guessed_letters = set()
correct_letters = {}
answer = []
guess_count = 6
guess = ''
won = False

for idx, ltr in enumerate(secret_word):
    correct_letters.setdefault(ltr, {'index':[], 'found': False})
    correct_letters[ltr]['index'].append(idx)
    answer.append("_")

while won == False and guess_count > 0:

    legal_ltr = eval_alpha(guess)

    if legal_ltr == secret_word:
        print "Didn't need all the guesses, did you?"
        won = True
        break
        #play_again()
    elif len(legal_ltr) != 1 and legal_ltr != secret_word:
        print "That wasn't the secret word. Try entering one letter at a time if you're not sure what the word is."

    elif guess_count > 1 and legal_ltr in guessed_letters or \
    (legal_ltr in correct_letters and correct_letters[legal_ltr]['found']):
        print "You've already guessed this letter--try a different one. You still have %s guesses left." % guess_count
        display_hangman() 

    elif guess_count == 1 and (legal_ltr in guessed_letters or (legal_ltr in correct_letters and correct_letters[legal_ltr]['found'])):
        print "You've already guessed this letter--try a different one. You still have one guess left."
        display_hangman() 

    elif legal_ltr in correct_letters:
        for word_idx in correct_letters[legal_ltr]['index']:
            answer[word_idx] = legal_ltr
        
        #changing status to found
        correct_letters[legal_ltr]['found'] = True

        if ''.join(answer) == secret_word:
            won = True 
            break    
        print "Correct!" 
        display_hangman()   

    else: 
        #if letter is incorrect
        guesses_left = 6 - guess_count
        guess_count -= 1
        
        if guess_count == 1 :
            print "Only one guess left! Make it count!"
            display_hangman()

        else: 
            print "Yikes! You now have %s guesses left." % guess_count
            display_hangman()

if won:
    print("Hooray!You've won!")
    print "The secret word was " + secret_word + "!!!"

else:
    print('The gallows for you! The answer was "%s". ') % secret_word





