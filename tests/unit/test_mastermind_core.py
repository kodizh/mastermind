from mastermind.mastermind_core import MastermindCore


def test_configure_default():
    mastermind = MastermindCore()
    mastermind.configure()

    assert mastermind.code_length == 4
    assert mastermind.allow_duplicates == True
    assert mastermind.max_tries == 10
    assert mastermind.colours_set == set(['Green', 'Yellow', 'Red', 'Orange', 'Blue', 'Black', 'White'])


def test_configure():
    mastermind = MastermindCore()
    mastermind.configure(
        code_length = 3,
        allow_duplicates = False,
        max_tries = 12,
        colours_set = ['Red', 'Green', 'Blue']
    )

    assert mastermind.code_length == 3
    assert mastermind.allow_duplicates == False
    assert mastermind.max_tries == 12
    assert mastermind.colours_set == set(['Red', 'Green', 'Blue'])


def test_init_default():
    mastermind = MastermindCore()

    assert mastermind.code_length == 4
    assert mastermind.allow_duplicates == True
    assert mastermind.max_tries == 10
    assert mastermind.colours_set == set(['Green', 'Yellow', 'Red', 'Orange', 'Blue', 'Black', 'White'])
    assert len(mastermind.secret_code) == 4
    assert len([x for x in mastermind.secret_code if x not in mastermind.colours_set]) == 0
    assert len(mastermind.player_guesses) == 0


def test_reset_game():
    mastermind = MastermindCore()
    mastermind.configure(
        code_length = 3,
        allow_duplicates = False,
        colours_set = ['Red', 'Green', 'Blue']
    )
    mastermind.reset_game()

    assert len(mastermind.secret_code) == 3
    assert len([x for x in mastermind.secret_code if x not in mastermind.colours_set]) == 0
    assert len(mastermind.player_guesses) == 0


def test_generate_code_peg_with_duplicates():
    mastermind = MastermindCore()
    generator = mastermind.generate_code_peg()
    for i in range(30):
        assert next(generator) in mastermind.colours_set
