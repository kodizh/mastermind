import kivy
from kivy.app import App

from kivy.factory import Factory

from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.pagelayout import PageLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.widget import Widget
from kivy.uix.button import Label
from kivy.uix.button import Button
from kivy.uix.image import Image

from kivy.properties import ListProperty

from mastermind_core import MastermindCore
from mastermind_core import MaxTriesReachedError
from mastermind_core import BadGuessLengthError

import logging

# this restrict the kivy version i.e
# below this kivy version you cannot
# use the app or software
kivy.require('1.9.0')


class MastermindBoard(PageLayout):
    """ Base widget class for the application.
    """

    """ Defines possible peg colours using RGBA values
    """
    colours = {
        "Red": [1, 0, 0, 1],
        "Green": [.6, 1, .3, 1],
        "Blue": [.3, .6, 1, 1],
        "Yellow": [1, 1, .3, 1],
        "Orange": [1, .6, 0, 1],
        "White": [1, 1, 1, 1],
        "Black": [0, 0, 0, 1]
    }

    """ Define the board background texture
    """
    background_texture = Image(source = '../resources/light_wood_texture.jpg').texture
    background_texture.wrap = 'repeat'
    background_texture.uvsize = (4, 4)

    def __init__(self, **kwargs):
        super(MastermindBoard, self).__init__(**kwargs)
        self.selected_colour = None              # Store the currently selected colour
        self.current_row = []                    # Store the state of the currently played row
        self.widgets = {}                        # Store the widgets that needs an update during the game


    def init_game(self):
        # Initialise the mastermmind game
        self.logic_manager.reset_game()

        # Initialise variables used for gui logic
        self.selected_colour = None
        self.current_row = [None] * self.logic_manager.code_length
        self.widgets = {}

        # Initialise the GUI
        self.ids.player_board.clear_widgets(self.ids.player_board.children)
        self.ids.pegs_reservoir.clear_widgets(self.ids.pegs_reservoir.children)

        self.draw_main_board()
        self.draw_pegs_reservoir()


    def draw_main_board(self):
        board = self.ids.player_board
        # The number of columns is the size of the board + the indications on
        # successful positions and colours + the validate button
        board.cols = self.logic_manager.code_length + 3
        board.row_force_default = True
        board.row_default_height = 50

        max_rows = self.logic_manager.max_tries -1
        for row in range(max_rows, -1, -1):
            position_checker = GridLayout()
            position_checker.rows = 1
            position_checker.add_widget(Widget())
            board.add_widget(position_checker)
            self.widgets[f"pos_check_{row}"] = position_checker

            max_cols = self.logic_manager.code_length
            for col in range(self.logic_manager.code_length):
                spot = Factory.PegSpot()
                spot.spot_position = [row, col]

                # bind the button to function used for setting the selected colour
                spot.bind(on_press = self.set_peg)

                # Disable all spots that are not selectable yet
                if row > 0:
                    spot.disabled = True

                board.add_widget(spot)
                self.widgets[f"peg_spot_{row}_{col}"] = spot

            colours_checker = GridLayout()
            colours_checker.rows = 1
            colours_checker.add_widget(Widget())
            board.add_widget(colours_checker)
            self.widgets[f"col_check_{row}"] = colours_checker

            button_validate = Button(
                text = f"",
                size_hint = (None, None),
                size = (100, 50),
                disabled = True)

            button_validate.bind(on_press = self.validate_row)
            board.add_widget(button_validate)
            self.widgets[f"butt_validate_{row}"] = button_validate



    def draw_pegs_reservoir(self):
        """ Draw the pegs available to the player below the board
        """
        reserv = self.ids.pegs_reservoir
        for peg_colour in self.logic_manager.colours_set:
            peg = Factory.Peg()
            peg.peg_color = peg_colour
            peg.background_normal = f'../resources/peg_{peg_colour}.png'
            #peg.background_color = MastermindBoard.colours[peg_colour]
            peg.bind(on_press = self.select_colour)
            reserv.add_widget(peg)


    def add_logic_manager(self, logic_manager):
        """ Add the logic manager in order to respond to user interface requests
        """
        self.logic_manager = logic_manager


    def set_peg(self, peg_spot):
        """ Action to position a peg onto the player board
        """
        if self.selected_colour:
            peg_spot.background_normal = f'../resources/peg_{self.selected_colour}.png'
            peg_spot.background_disabled_normal = f'../resources/peg_{self.selected_colour}.png'

            peg_row = peg_spot.spot_position[0]
            peg_col = peg_spot.spot_position[1]
            self.current_row[peg_col] = self.selected_colour

            if not None in self.current_row:
                self.toggle_validate_button(peg_row, set_enable=True)


    def select_colour(self, event):
        """ Action to select a colour among the colours available to the player.
        """
        self.selected_colour = event.peg_color
        logging.info(f"Selected colour: {self.selected_colour}")


    def validate_row(self, event):
        """ Action triggered by validating the current row using the validate
            button.
        """
        try:
            has_win = self.logic_manager.add_guess(self.current_row)

            if has_win:
                self.display_end_of_game_popup(has_won=True)
            else:
                self.update_board_state()

        except MaxTriesReachedError as mtre:
            self.display_end_of_game_popup(has_won=False)

        except BadGuessLengthError as bgle:
            logging.error(f"Mismatch between the guess length and the code length. {blge}")


    def update_board_state(self):
        """ Close the current row, and display the response to the player's guess
            to allow the player to continue playing on next row, and update the
            board state.
        """

        correct_positions = self.logic_manager.last_row_correct_positions
        correct_colours = self.logic_manager.last_row_correct_colours
        logging.info((f"Player has not won yet. Correct positions: {correct_positions}, "
                      f"correct colours: {correct_colours}"))

        current_row = self.logic_manager.nb_player_guesses - 1

        # Add the correct positions widgets
        for i in range(correct_positions):
            lbl = Factory.PositionValidator()
            self.widgets[f'pos_check_{current_row}'].add_widget(lbl)

        # Add the correct colours widgets
        for i in range(correct_colours):
            lbl = Factory.ColourValidator()
            self.widgets[f'col_check_{current_row}'].add_widget(lbl, index = 2)

        # Initialise the row vector for the new row
        self.current_row = [None] * self.logic_manager.code_length

        # Remove the validate button
        self.toggle_validate_button(current_row)

        # Close the current row (set buttons to disabled) and initialise the new row
        for col in range(self.logic_manager.code_length):
            self.widgets[f"peg_spot_{current_row}_{col}"].disabled = True
            self.widgets[f"peg_spot_{current_row+1}_{col}"].disabled = False


    def toggle_validate_button(self, row, set_enable=None):
        """ Toggle the validate button at the end of the row
        """

        button_validate = self.widgets[f"butt_validate_{row}"]
        if button_validate.disabled or set_enable:
            button_validate.text = "Validate"
            button_validate.disabled = False
        else:
            button_validate.text = ""
            button_validate.disabled = True


    def display_end_of_game_popup(self, has_won):
        """ Display the dialog box that show up when the game is over
        """

        if has_won:
            end_game_msg = f"WON in {self.logic_manager.nb_player_guesses} tries"
        else:
            end_game_msg = "LOST"

        popup = Factory.EndGame()
        popup.ids.end_game_state.text = f"You have {end_game_msg}!"
        popup.ids.play_again_button.bind(on_press = self.play_again)
        self.widgets['end_game_popup'] = popup
        popup.open()


    def play_again(self, event):
        self.widgets['end_game_popup'].dismiss()
        del self.widgets['end_game_popup']

        self.init_game()


class MastermindApp(App):
    """ Main App class to instanciate the Mastermind board
        and logic module.
    """

    def build(self):
        logging.getLogger().setLevel(logging.INFO)

        self.mastermind_core = MastermindCore()
        self.title = 'Mastermind'

        board = MastermindBoard()
        board.add_logic_manager(self.mastermind_core)
        board.init_game()
        return board


app = MastermindApp()
app.run()
