# Hangman

## Table of Contents
- [Introduction](#introduction)
- [Installation](#installation)
- [Extensions](#extensions)
 

## Introduction

This is a command line application of Hangman, written in Python.  Users have the option to select difficulty settings, and to play in traditional or "evil" mode. 

In traditional hangman, the secret word is fixed for the entirety of the game, and never changes. The "evil hangman" variant is where the computer cheats by switching the secret word every time the user guesses a letter. Since the secret word(s) still match the revealed letters and blank spaces on the board, the user experience is identical to a traditional game of hangman, but winning is much more difficult. By maintaining a list of possible secret words and continually paring down the list of candidates as the user guesses each letter, the computer delays committing to a fixed secret word until there are no other possibilities. 

Further details on Evil Hangman can be found [here](http://www.keithschwarz.com/cs106l/spring2010/handouts/020_Assignment_1_Evil_Hangman.pdf), via Keith Schwarz. 

## Installation

1. Make sure you have Python installed (if you're on a Mac, Python should already be installed).

1. Clone or download the git repo at: "https://github.com/levi006/hangman".

     `git clone https://github.com/levi006/hangman`

1. Run the file from your terminal:

     `python hangman.py`

And you should have the game up and running!


## Extensions 

#### Initial Implementation

The first pass was a basic control flow for traditional hangman, and then I refactored the code into functions to avoid repetition. I ran into architectural issues when deciding what to designate as top level and helper functions, and what to designate as a helper function vs. folding it as a few lines of code in a higher level function. As I progressed, I began thinking an object oriented approach would be more elegant, especially as I was working on implementing the Evil Hangman variant--this would probably be a main focus for next steps.

The current version of the game has the following features:
	* The length of the secret word is displayed to the guesser (e.g. as a set of underscores)
	* As the guesser makes correct guesses, occurrences of the guessed letter in the word
	are shown while unknown letters are still hidden
	* The number of guesses remaining is displayed
	* A list of incorrect guesses are displayed  

The game also allows the user to select from 10 difficulty settings, and to guess an entire word at a time.  
 

#### Evil Hangman







