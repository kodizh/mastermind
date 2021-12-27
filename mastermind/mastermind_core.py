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


class BadColoursSetError(Exception):
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


    def configure(self,
                  code_length = 4,
                  allow_duplicates = True,
                  max_tries = 10,
                  colours_set = ['Green', 'Yellow', 'Red', 'Orange', 'Blue', 'Black', 'White']):
        """Configure the game's parameters
        """
        self._code_length = code_length
        self._allow_duplicates = allow_duplicates
        self._max_tries = max_tries
        self._colours_set = set(colours_set)

        # Check out that the colours set is big enough when no duplicates are allowed
        size_diff = len(colours_set) < code_length
        if not allow_duplicates and size_diff:
            raise BadColoursSetError((f"The colours set is too small ({len(colours_set)}) "
                                       "for the expected code length ({code_length}) "
                                       "and no duplicates are allowed."))

        logging.info("Configuration updated:")
        logging.info(f" - code_length: {self._code_length}")
        logging.info(f" - allow_duplicates: {self._allow_duplicates}")
        logging.info(f" - max_tries: {self._max_tries}")
        logging.info(f" - colours_set: {', '.join(self._colours_set)}")


    @property
    def code_length(self):
        return self._code_length


    @property
    def secret_code(self):
        return self._secret_code


    @property
    def max_tries(self):
        return self._max_tries


    @property
    def colours_set(self):
        return self._colours_set


    @property
    def nb_player_guesses(self):
        return len(self._player_guesses)


    @property
    def last_row_correct_positions(self):
        row = self.nb_player_guesses - 1
        return self._player_guesses[row]['matching_places']


    @property
    def last_row_correct_colours(self):
        row = self.nb_player_guesses - 1
        return self._player_guesses[row]['matching_colours']


    def reset_game(self):
        """ Generate a new code and delete the player's previous guesses
        """
        generator = self.generate_code_peg()
        self._secret_code = [ next(generator) for _ in range(self._code_length) ]
        self._player_guesses = []
        logging.info(f"New secret code generated: {self._secret_code}")


    def generate_code_peg(self):
        """ Create a new code peg at each call
        """
        colours = [x for x in self._colours_set]

        while len(colours) > 0:
            id = randrange(len(colours))

            if self._allow_duplicates:
                peg = colours[id]
            else:
                peg = colours.pop(id)

            yield peg


    def add_guess(self, guess):
        """ Add a new guess to the list of the player's guesses
        """
        # Check that the player's guess and the secret code sizes match
        if len(guess) != len(self._secret_code):
            raise BadGuessLengthError(f"Incorrect player's guess size. Expected: {len(self._secret_code)}, got: {len(guess)}")

        # Check if colours from the guest list are within the current set
        wrong_colours = [x for x in guess if x not in self._colours_set]
        if len(wrong_colours) > 0:
            raise UnknownColourError(f"The player's guess contains colours that are not part of the current set: {', '.join(wrong_colours)}.")

        logging.info(f"Adding new guess #{len(self._player_guesses)}")

        # Find out how many peg of the correct colour are at the correct location
        matching_locations_count = len([x for i, x in enumerate(self._secret_code) if guess[i] == x])
        logging.info(f"Matching locations: {matching_locations_count}")

        matching_colours = Counter(guess) & Counter(self._secret_code)
        matching_colours_count = sum(matching_colours.values())
        logging.info(f"Matching colours: {matching_colours_count}")

        self._player_guesses.append({'guess': guess,
                                    'matching_places': matching_locations_count,
                                    'matching_colours': matching_colours_count - matching_locations_count})

        player_won = matching_locations_count == len(self._secret_code)
        max_tries_reached = len(self._player_guesses) >= self._max_tries

        logging.info((f"Guess added. Player won: {player_won}, current tries: "
                      f"{len(self._player_guesses)}, max tries reached: {max_tries_reached}"))

        if not player_won and max_tries_reached:
            raise MaxTriesReachedError(f"Solution not found within {self._max_tries} tries")

        return player_won
