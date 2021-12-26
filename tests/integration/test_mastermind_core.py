from mastermind.mastermind_core import MastermindCore


def test_add_valid_guesses():
    """ Validating adding a valid guess. The properties shall be modified
        accordingly.
    """
    guess1 = ['Red', 'Green', 'Blue', 'Yellow']
    guess2 = ['Red', 'Green', 'Blue', 'Blue']

    mastermind = MastermindCore()
    mastermind.configure(
        code_length = 4,
        colours_set = ['Red', 'Green', 'Blue', 'Yellow']
    )
    mastermind._secret_code = ['Green', 'Red', 'Blue', 'Blue']

    ret = mastermind.add_guess(guess1)
    assert ret == False
    assert mastermind.nb_player_guesses == 1
    assert mastermind._player_guesses[0]['guess'] == guess1
    assert mastermind._player_guesses[0]['matching_places'] == 1
    assert mastermind._player_guesses[0]['matching_colours'] == 2

    ret = mastermind.add_guess(guess2)
    assert ret == False
    assert mastermind.nb_player_guesses == 2
    assert mastermind._player_guesses[1]['guess'] == guess2
    assert mastermind._player_guesses[1]['matching_places'] == 2
    assert mastermind._player_guesses[1]['matching_colours'] == 2


def test_add_winning_guess():
    """ Validating adding a winning guess. The properties shall be modified
        accordingly.
    """
    guess = ['Green', 'Red', 'Blue', 'Blue']

    mastermind = MastermindCore()
    mastermind.configure(
        code_length = 4,
        colours_set = ['Red', 'Green', 'Blue', 'Yellow']
    )
    mastermind._secret_code = ['Green', 'Red', 'Blue', 'Blue']
    ret = mastermind.add_guess(guess)

    assert ret == True
    assert mastermind.nb_player_guesses == 1
    assert mastermind._player_guesses[0]['guess'] == guess
    assert mastermind._player_guesses[0]['matching_places'] == 4
    assert mastermind._player_guesses[0]['matching_colours'] == 0
