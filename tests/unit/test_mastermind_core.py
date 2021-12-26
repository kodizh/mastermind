from mastermind.mastermind_core import MastermindCore
from mastermind.mastermind_core import BadColoursSetError

import pytest


def test_configure_default():
    """ Validating that default configuration initialises all preperties properly
    """
    mastermind = MastermindCore()
    mastermind.configure()

    assert mastermind.code_length == 4
    assert mastermind._allow_duplicates == True
    assert mastermind.max_tries == 10
    assert mastermind.colours_set == set(['Green', 'Yellow', 'Red', 'Orange', 'Blue', 'Black', 'White'])


def test_configure():
    """ Validating that configuration initialises properties according to the passed
        arguments.
    """
    mastermind = MastermindCore()
    mastermind.configure(
        code_length = 3,
        allow_duplicates = False,
        max_tries = 12,
        colours_set = ['Red', 'Green', 'Blue']
    )

    assert mastermind.code_length == 3
    assert mastermind._allow_duplicates == False
    assert mastermind.max_tries == 12
    assert mastermind.colours_set == set(['Red', 'Green', 'Blue'])


def test_init_default():
    """ Validating that default constructor initialises all properties properly
    """
    mastermind = MastermindCore()

    assert mastermind.code_length == 4
    assert mastermind._allow_duplicates == True
    assert mastermind.max_tries == 10
    assert mastermind.colours_set == set(['Green', 'Yellow', 'Red', 'Orange', 'Blue', 'Black', 'White'])
    assert len(mastermind._secret_code) == 4
    assert len([x for x in mastermind._secret_code if x not in mastermind.colours_set]) == 0
    assert len(mastermind._player_guesses) == 0


def test_reset_game():
    """ Validating that reset games takes into account a change of properties
    """
    mastermind = MastermindCore()
    mastermind.configure(
        code_length = 3,
        allow_duplicates = False,
        colours_set = ['Red', 'Green', 'Blue']
    )
    mastermind.reset_game()

    assert len(mastermind._secret_code) == 3
    assert len([x for x in mastermind._secret_code if x not in mastermind.colours_set]) == 0
    assert len(mastermind._player_guesses) == 0


def test_generate_code_peg_with_duplicates():
    """ Validating the peg generation. All generated pegs shall be comprised
        within the pegs set.
    """
    mastermind = MastermindCore()
    generator = mastermind.generate_code_peg()
    for i in range(500):
        assert next(generator) in mastermind.colours_set


def test_generate_code_peg_with_no_duplicates():
    """ Validating the peg generation when no duplicates are allowed. All
        generated pegs shall be comprised within the pegs set, and an exception
        shall be raised when no colours are available in the set.
    """
    mastermind = MastermindCore()
    mastermind._allow_duplicates = False
    mastermind._colours_set = ['Red', 'Green', 'Blue']

    # Test not exceeding the set's limit
    generator = mastermind.generate_code_peg()
    for i in range(3):
        print(f"Iteration {i}")
        assert next(generator) in mastermind.colours_set

    # Test exceeding the set's limit
    generator = mastermind.generate_code_peg()
    with pytest.raises(StopIteration):
        for i in range(4):
            print(f"Iteration {i}")
            assert next(generator) in mastermind.colours_set


def test_bad_colours_set():
    """ Validating that the BadColoursSetError exception is raised when required
    """
    mastermind = MastermindCore()
    with pytest.raises(BadColoursSetError):
        mastermind.configure(
            code_length = 4,
            allow_duplicates = False,
            colours_set = ['Red', 'Green', 'Blue'])
