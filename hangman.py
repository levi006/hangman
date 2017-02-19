import random, requests

def set_difficulty_settings():
  difficulty_level = raw_input('Please select the difficulty level, from 1-10, where 1 is easy and 10 is the most difficult.')
  max_length = raw_input('Please select the max length of the generated word.')
  min_length = raw_input('Please select the min length of the generated word.')

  payload = {'difficulty': difficulty_level,
            'maxLength': max_length,
            'minLength': min_length, 
            }
  print payload
  return payload

def generate_word():
  words = ['apple', 'berry']
  # words = response.text.splitlines()
  word_index = random.randrange(0, len(words) -1)
  chosen_word = words[word_index]
  return chosen_word

# def eval_guess(guessed_ltr):
#   guessed_ltr = guessed_ltr.strip().lower()
#   if len(guessed_ltr) != 1:
#     print('Please enter only one letter at a time.')
#   if guessed_ltr in incorrect_letters or \
#   (guessed_ltr in correct_letters and correct_letters[guessed_ltr]['found']):
#     print "You've already guessed this letter--try a different one. You still have %s guesses left." % guess_count
#     print ' '.join(answer)
#   elif guessed_ltr not in 'abcdefghijklmnopqrstuvwxyz':
#     print 'Please enter only a letter.'
#   else:
#     return guessed_ltr

#Gameplay

url = 'http://linkedin-reach.hagbpyjegb.us-west-2.elasticbeanstalk.com/words'
# payload = set_difficulty_settings()
# response = requests.get(url, params = payload)
response = requests.get(url)
secret_word = generate_word()
#correct letters = { letter : {count, found status}}
correct_letters = {}
answer = []
incorrect_letters = set()
won = False
guess_count = 6

for idx, ltr in enumerate(secret_word):
  correct_letters.setdefault(ltr, {'index':[], 'found': False})
  correct_letters[ltr]['index'].append(idx)
  answer.append("_")

while not won and guess_count > 0:

  guessed_ltr = raw_input("Guess a letter: ")
  # guessed_ltr = eval_guess(guessed_ltr)
  # guessed_ltr = guessed_ltr.strip().lower()

  #guessing the whole word at once
  if guessed_ltr == secret_word:
    print "Got it! Didn't need all the guesses, did you?"

  #second check for double letters
  elif guessed_ltr in incorrect_letters or \
  (guessed_ltr in correct_letters and correct_letters[guessed_ltr]['found']):
    print "You've already guessed this letter--try a different one. You still have %s guesses left." % guess_count
    print ' '.join(answer)

  #if letter is correct
  elif guessed_ltr in correct_letters:
    for word_idx in correct_letters[guessed_ltr]['index']:
      answer[word_idx] = guessed_ltr
    
    #changing status for found
    correct_letters[guessed_ltr]['found'] = True
    
    if ''.join(answer) == secret_word:
      won = True 
      break  
    print ' '.join(answer)
    print "Correct!" 

  else:
    guesses_left = 6 - guess_count
    guess_count -= 1
    print "Wrong! You now have %s guesses left." % guess_count
    incorrect_letters.add(guessed_ltr)
    mistakes = ' '.join(incorrect_letters)
    print "You have guessed these letters: %s " % mistakes  

if won:
  print("Correct! You've won!")

else:
  print('The gallows for you! The answer was "%s". ') % secret_word




