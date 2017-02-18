import random
import requests
import json 

# url = 'http://linkedin-reach.hagbpyjegb.us-west-2.elasticbeanstalk.com/words'
# payload = {'difficulty':10}
# response = requests.get(url, params = payload) 
# print response.text
# print type(response.text)
# print repr(response.text)

words = ["apple", "foo", "michael"]
# word_list = response.text.splitlines()

word_list_index = random.randrange(0, len(word_list) -1)
chosen_word = word_list[word_list_index]

#correct_letters {letter:{index (integer), found (Boolean)}}
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
  guessed_ltr = input("Letter?: ")
  guessed_ltr = guessed_ltr.strip().lower()

  if guessed_ltr in correct_letters:
    for word_idx in correct_letters[guessed_ltr]['index']:
      answer[word_idx] = guessed_ltr

      
    print ' '.join(answer)
    print "Correct! You still have %s guesses left." % guess  


  elif guessed_ltr in incorrect_letters:
    print "You've already guessed this letter--try a different one."


  else:
    guesses_left = 6 - guess
    guess -= 1
    print "Wrong! You now have %s guesses left." % guess
    incorrect_letters.add(guessed_ltr)
    mistakes = ' '.join(incorrect_letters)
    print "You have guessed these letters: %s " % mistakes  


  if ''.join(answer) == chosen_word:
    won = True



if won:
  print("You won!")

else:
  print("YOU'VE LOST. Hangman!")




