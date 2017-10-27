############################################################
# Imports
############################################################
import game_helper as gh
from copy import deepcopy
############################################################
# Class definition
############################################################

DETONATION = 0
LONGEVITY = 3

class Game:
    """
    A class representing a battleship game.
    A game is composed of ships that are moving on a square board and a user
    which tries to guess the locations of the ships by guessing their
    coordinates.
    """

    def __init__(self, board_size, ships):
        """
        Initialize a new Game object.
        :param board_size: Length of the side of the game-board.
        :param ships: A list of ships (of type Ship) that participate in the
            game.
        :return: A new Game object.
        """
        self.__board_size = board_size
        self.__ships = ships
        self.__bombs = {}
        self.__hit_coordinates = []
        self.__not_hit_coordinates = []
        self.__hit_ships = 0
        self.__terminated_ships = 0
        self.__current_turn_hits = []

        for ship in self.__ships:
            cells = ship.coordinates()
            for i in range(len(cells)):
                self.__not_hit_coordinates.append(cells[i])

    def get_board_size(self):
        return self.__board_size
    def get_bombs(self):
        return self.__bombs
    def get_ships(self):
        return self.__ships
    def get_hit_coordinates(self):
        return self.__hit_coordinates
    def get_not_hit_coordinates(self):
        return self.__not_hit_coordinates
    def get_current_turn_ships(self):
        return self.__current_turn_hits
    def get_terminateted_ships(self):
        return self.__terminated_ships
    def get_hit_ships(self):
        return self.__hit_ships


    def __play_one_round(self):
        """
        Note - this function is here to guide you and it is *not mandatory*
        to implement it. The logic defined by this function must be implemented
        but if you wish to do so in another function (or some other functions)
        it is ok.

        The function runs one round of the game :
            1. Get user coordinate choice for bombing.
            2. Move all game's ships.
            3. Update all ships and bombs.
            4. Report to the user the result of current round (number of hits and
             terminated ships)
        :return:
            (some constant you may want implement which represents) Game status :
            GAME_STATUS_ONGOING if there are still ships on the board or
            GAME_STATUS_ENDED otherwise.
        """
        target_bomb = gh.get_target(Game.get_board_size(self))
        for ship in self.__ships:
            if not ship.damaged_cells():
                ship.move()
                for coordinate in ship.coordinates():
                    if coordinate in self.__bombs.keys():
                        self.__current_turn_hits.append(coordinate)

            elif ship.terminated():
                self.__ships.remove(ship)

            elif not ship.hit(target_bomb):
                self.__bombs[target_bomb] = LONGEVITY
            else:
                self.__current_turn_hits.append(target_bomb)

        for bomb in self.__bombs:
            if self.__bombs[bomb] == DETONATION:
                del self.__bombs[bomb]
            else:
                self.__bombs[bomb] -= 1

        gh.board_to_string(self.__board_size, self.__current_turn_hits, self.__bombs,
                           self.__hit_coordinates, self.__not_hit_coordinates)
        self.__current_turn_hits.clear()
        gh.report_turn(self.get_hit_ships(), self.get_terminateted_ships())

    def __repr__(self):
        """
        Return a string representation of the board's game.
        :return: A tuple converted to string (that is, for a tuple x return
            str(x)). The tuple should contain (maintain
        the following order):
            1. Board's size.
            2. A dictionary of the bombs found on the board, mapping their
                coordinates to the number of remaining turns:
                 {(pos_x, pos_y) : remaining turns}
                For example :
                 {(0, 1) : 2, (3, 2) : 1}
            3. A list of the ships found on the board (each ship should be
                represented by its __repr__ string).
        """
        represent = (self.get_board_size(),
                     self.get_bombs(),
                     self.get_ships())
        return str(represent)

    def play(self):
        """
        The main driver of the Game. Manages the game until completion.
        :return: None
        """
        for ship in self.__ships:
            self.__not_hit_coordinates.extend(ship.coordinates())

        gh.report_legend()

        gh.board_to_string(self.get_board_size(),
                           [],
                           {},
                           [],
                           deepcopy(self.get_not_hit_coordinates()))

        ships_quantity = len(self.__ships)

        while self.__terminated_ships != ships_quantity:
            self.__play_one_round()
        return None




############################################################
# An example usage of the game
############################################################
if __name__ == "__main__":
    game = Game(5, gh.initialize_ship_list(4, 2))
    game.play()
