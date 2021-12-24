#!/usr/bin/env python3

"""
Mastermind game files that contains the game's logic.

The game can be used from the cli (although quite unfriendly) or
from a UI that instanciate the MastermindCore class.
"""


from collections import Counter
from random import randrange
import logging


class BadGuessLengthError(Exception):
    pass


class BadColoursSet(Exception):
    pass


class UnknownColourError(Exception):
    pass


class MaxTriesReachedError(Exception):
    pass


class MastermindCore:
    def __init__(self):
        logging.getLogger().setLevel(logging.INFO)

        # Initialise default parameters
        self.configure()

        # Set up a new game
        self.reset_game()


    def configure(self,
                  code_length = 4,
                  allow_duplicates = True,
                  max_tries = 10,
                  colours_set = ['Green', 'Yellow', 'Red', 'Orange', 'Blue', 'Black', 'White']):
        """Configure the game's parameters
        """
        self.code_length = code_length
        self.allow_duplicates = allow_duplicates
        self.max_tries = max_tries
        self.colours_set = set(colours_set)

        # Check out that the colours set is big enough when no duplicates are allowed
        size_diff = len(colours_set) < code_length
        if not allow_duplicates and size_diff:
            raise BadColoursSet( (f"The colours set is too small ({len(colours_set)}) "
                                   "for the expected code length ({code_length}) "
                                   "and no duplicates are allowed."))

        logging.info("Configuration updated:")
        logging.info(f" - code_length: {self.code_length}")
        logging.info(f" - allow_duplicates: {self.allow_duplicates}")
        logging.info(f" - max_tries: {self.max_tries}")
        logging.info(f" - colours_set: {', '.join(self.colours_set)}")


    def reset_game(self):
        """ Generate a new code and delete the player's previous guesses
        """
        generator = self.generate_code_peg()
        self.secret_code = [ next(generator) for _ in range(self.code_length) ]
        self.player_guesses = []


    def generate_code_peg(self):
        """ Create a new code peg at each call
        """
        colours = [x for x in self.colours_set]

        while len(colours) > 0:
            id = randrange(len(colours))

            if self.allow_duplicates:
                peg = colours[id]
            else:
                peg = colours.pop(id)

            yield peg


    def add_guess(self, guess):
        """ Add a new guess to the list of the player's guesses
        """
        # Check that the player's guess and the secret code sizes match
        if len(guess) != len(self.secret_code):
            raise BadGuessLengthError(f"Incorrect player's guess size. Expected: {len(self.secret_code)}, got: {len(guess)}")

        # Check if colours from the guest list are within the current set
        wrong_colours = [x for x in guess if x not in self.colours_set]
        if len(wrong_colours) > 0:
            raise UnknownColourError(f"The player's guess contains colours that are not part of the current set: {', '.join(wrong_colours)}.")

        # Find out how many peg of the correct colour are at the correct location
        matching_locations_count = len([x for i, x in enumerate(self.secret_code) if guess[i] == x])

        matching_colours = Counter(guess) & Counter(self.secret_code)
        matching_colours_count = sum(matching_colours.values())

        self.player_guesses.append({'guess': guess,
                                    'matching_places': matching_locations_count,
                                    'matching_colours': matching_colours_count - matching_locations_count})

        player_won = matching_locations_count == len(self.secret_code)
        max_tries_reached = len(self.player_guesses) > self.max_tries

        if not player_won and max_tries_reached:
            raise MaxTriesReachedError(f"Solution not found within {self.max_tries} tries")

        return player_won
