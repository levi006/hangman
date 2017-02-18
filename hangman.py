import random, requests

url = 'http://linkedin-reach.hagbpyjegb.us-west-2.elasticbeanstalk.com/words'


# words = ['apple', 'berry']

def set_difficulty_settings():
  difficulty_level = raw_input('Please select the difficulty level, from 1-10, where 1 is easy and 10 is the most difficult.')
  max_length = raw_input('Please select the max length of the generated word.')
  min_length = raw_input('Please select the min length of the generated word.')

  payload = {'difficulty': difficulty_level,
            'max length': max_length,
            'minimum length': min_length, 
            }
  return payload

payload = set_difficulty_settings()
response = requests.get(url, params = payload) 
words = response.text.splitlines()

word_index = random.randrange(0, len(words) -1)

chosen_word = words[word_index]
correct_letters = {}
answer = []
incorrect_letters = set()

for idx, ltr in enumerate(chosen_word):
  correct_letters.setdefault(ltr, {'index':[], 'found': False})
  correct_letters[ltr]['index'].append(idx)
  answer.append("_")

won = False
guess = 6

while not won and guess > 0:

  guessed_ltr = raw_input("Guess a letter: ")
  guessed_ltr = guessed_ltr.strip().lower()

  #second check for double letters
  if guessed_ltr in incorrect_letters or \
  (guessed_ltr in correct_letters and correct_letters[guessed_ltr]['found']):
    print "You've already guessed this letter--try a different one. You still have %s guesses left." % guess
    print ' '.join(answer)

  #if letter is correct
  elif guessed_ltr in correct_letters:
    for word_idx in correct_letters[guessed_ltr]['index']:
      answer[word_idx] = guessed_ltr
    #changing status for found
    correct_letters[guessed_ltr]['found'] = True
    
    if ''.join(answer) == chosen_word:
      won = True 
      break  
    print ' '.join(answer)
    print "Correct! You now have %s guesses left." % guess  

  else:
    guesses_left = 6 - guess
    guess -= 1
    print "Wrong! You now have %s guesses left." % guess
    incorrect_letters.add(guessed_ltr)
    mistakes = ' '.join(incorrect_letters)
    print "You have guessed these letters: %s " % mistakes  

if won:
  print("Correct! You've won!")

else:
  print('The gallows for you! The answer was "%s". ') % chosen_word




