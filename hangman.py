import random
import requests
import json 

url = 'http://linkedin-reach.hagbpyjegb.us-west-2.elasticbeanstalk.com/words'
payload = {'difficulty':1}
response = requests.get(url, params = payload) 
print response.text
print type(response.text)
print repr(response.text)

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
  guessed_ltr = raw_input("Letter?: ")
  guessed_ltr = guessed_ltr.strip().lower()

  #second check for double letters
  if guessed_ltr in incorrect_letters or \
  (guessed_ltr in correct_letters and correct_letters[guessed_ltr]['found']):
    print "You've already guessed this letter--try a different one. But you still have %s guesses left." % guess
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




