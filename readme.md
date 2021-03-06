# Hangman

## Table of Contents
- [Introduction](#introduction)
- [Installation](#installation)
- [Extensions](#extensions)
- [Next Steps](#next-steps)
 

## Introduction

This is a command line application of Hangman, written in Python.  Users have the option to select difficulty settings, and to play in traditional or "evil" mode. 

In traditional hangman, the secret word is fixed for the entirety of the game, and never changes. The "evil hangman" variant is where the computer cheats by switching the secret word every time the user guesses a letter. Since the secret word(s) still match the revealed letters and blank spaces on the board, the user experience is identical to a traditional game of hangman, but winning is much more difficult. By maintaining a list of possible secret words and continually paring down the list of candidates as the user guesses each letter, the computer delays committing to a fixed secret word until there are no other possibilities. 

Further details on Evil Hangman can be found [here](http://www.keithschwarz.com/cs106l/spring2010/handouts/020_Assignment_1_Evil_Hangman.pdf), via Keith Schwarz. 

## Installation

1. Make sure you have Python installed (if you're on a Mac, Python should already be installed).

	1. Also, the words are generated from an API, so you'll need to be connected to the internet to play. 

1. Clone or download the git repo at: "https://github.com/levi006/hangman".

     `git clone https://github.com/levi006/hangman.git`

1. Make sure you have pip (a package management system for Python) installed. If you need to install it, type:  

     `sudo easy_install pip`

1. Install the virtual environment tool:

     `sudo pip install virtualenv`

1. Create a virtual environment inside the working directory:

     `virtualenv env`

1. Source the environment:

     `source env/bin/activate`

1. Download the requirements:

     `pip install -r requirements.txt`

1. Run the file from your terminal:

     `python hangman.py`

And you should have the game up and running!


## Extensions 

### Initial Implementation

The first pass was a basic control flow for traditional hangman, and then I refactored the code into functions to avoid repetition. I ran into architectural issues when deciding what to designate as top level and helper functions, and what to designate as a helper function vs. folding it as a few lines of code in a higher level function. As I progressed, I began thinking an object oriented approach would be more elegant, especially as I was working on implementing the Evil Hangman variant--this would probably be a main focus for next steps.


### Features

The current version of the game has the following features:

1. The length of the secret word is displayed to the guesser (e.g. as a set of underscores)

1. As the guesser makes correct guesses, occurrences of the guessed letter in the word
are shown while unknown letters are still hidden

1. The number of guesses remaining is displayed

1. A list of incorrect guesses are displayed  

The game also allows the user to select from 10 difficulty settings, and to guess an entire word at a time.   

### Evil Hangman

This was the most interesting component of the game to code, and I needed to use a defaultdict data structure to keep track of which letters had been guessed (and not guessed) and at which index, in order to generate a new list of plausible word candidates that were 1) the same length as the previous secret word and 2) contained the same letters at the same indices (or blanks at the same indices) as the preceding secret word. 

The logic for evil mode quickly outgrew the initial control flow I had originally scripted out, and figuring out how to break up and modularize the code into functions, and when to insert the evil hangman logic was a challenge for me. (Structuring the functions and overall code structure were the biggest challenges). I ended up breaking the game logic into a top level "play()" function and each guess was evaluated in a secondary "play_round()" function. If a player elects to play in evil mode, each guessed letter is passed to a function that generates a word bank and a secret word for the next turn. Letters are only revealed on the board when the word bank runs out of candidates for which it can switch the secret word.

## Next Steps

Something to explore would be writing a function to play around with letter frequencies. Currently, each new secret word for an Evil Hangman turn is picked because it's the first in the generated word list (for larger word lists, random selection can take a few seconds). Instead of picking the first word in the work bank, we could preferentially weight the word candidates containing less commonly used letters like "j" or "q", making Evil Hangman slightly more difficult. Conversely, we could also give helpful hints to the player by suggesting the mostly likely, or most frequently occuring letters, to yield a correct guess.  

Notes on adding a timer:

Ended up with two while loops, one for displaying a timer and one to prompt a guess from the user. Impossible to run these while loops in parallel--searching brings up threading/multiprocessing, concepts for later exploration. 

Went back to stdin/stdout (selectIO for testing => select.select method has timing!!). 

Came across the curses library for advanced character displays in the terminal. Can designate specific areas of window for printing/stdout, i.e. gallows, scoreboard, timer, input.   






