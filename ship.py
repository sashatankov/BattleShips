############################################################
# Helper class
############################################################

import ship_helper as sh
import game_helper as gh
from copy import deepcopy
class Direction:
    """
    Class representing a direction in 2D world.
    You may not change the name of any of the constants (UP, DOWN, LEFT, RIGHT,
     NOT_MOVING, VERTICAL, HORIZONTAL, ALL_DIRECTIONS), but all other
     implementations are for you to carry out.
    """
    UP = 'UP'  # Choose your own value
    DOWN = 'DOWN'  # Choose your own value
    LEFT = 'LEFT'  # Choose your own value
    RIGHT = 'RIGHT'  # Choose your own value

    NOT_MOVING = 'NOT MOVING'  # Choose your own value

    VERTICAL = (UP, DOWN)
    HORIZONTAL = (LEFT, RIGHT)

    ALL_DIRECTIONS = (UP, DOWN, LEFT, RIGHT)

    Y_AXIS = 1
    X_AXIS = 0

############################################################
# Class definition
############################################################


class Ship:
    """
    A class representing a ship in Battleship game.
    A ship is 1-dimensional object that could be laid in either horizontal or
    vertical alignment. A ship sails on its vertical\horizontal axis back and
    forth until reaching the board's boarders and then changes its direction to
    the opposite (left <--> right, up <--> down).
    If a ship is hit in one of its coordinates, it ceases its movement in all
    future turns.
    A ship that had all her coordinates hit is considered terminated.
    """

    def __init__(self, pos, length, direction, board_size):
        """
        A constructor for a Ship object
        :param pos: A tuple representing The ship's head's (x, y) position
        :param length: Ship's length
        :param direction: Initial direction in which the ship is sailing
        :param board_size: Board size in which the ship is sailing
        """
        self.__pos = pos
        self.__length = length
        self.__direction = direction
        self.__board_size = board_size
        self.__coordinates = list()

        # initialing the coordinates list
        if self.__direction == Direction.LEFT or \
           self.__direction == Direction.RIGHT:
            for i in range(self.__pos[Direction.X_AXIS], self.__pos[Direction.X_AXIS] + length):
                self.__coordinates.append((i, self.__pos[Direction.Y_AXIS]))
        else:
            for i in range(self.__pos[Direction.Y_AXIS], self.__pos[Direction.Y_AXIS] + length):
                self.__coordinates.append((pos[Direction.X_AXIS], i))

        self.__hit_coordinates = [False] * length

    def get_board_size(self):
        return self.__board_size

    def __repr__(self):
        """
        Return a string representation of the ship.
        :return: A tuple converted to string (that is, for a tuple x return
            str(x)).
        The tuple's content should be (in the exact following order):
            1. A list of all the ship's coordinates.
            2. A list of all the ship's hit coordinates.
            3. Last sailing direction.
            4. The size of the board in which the ship is located.
        """
        represantation = (self.coordinates(), self.generate_coordinates_from_boolean(),
                          sh.direction_repr_str(Direction, self.direction()),
                          self.get_board_size())
        return str(represantation)

    def generate_coordinates_from_boolean(self):
        generated_coordinates = list()
        for i in range(len(self.__hit_coordinates)):
            if self.__hit_coordinates[i]:
                generated_coordinates.append(self.__coordinates[i])
        return generated_coordinates

    def move(self):
        """
        Make the ship move one board unit.
        Movement is in the current sailing direction, unless such movement would
        take the ship outside of the board, in which case the ship switches
        direction and sails one board unit in the new direction.
        :return: A direction object representing the current movement direction.
        """
        if self.__direction == Direction.UP:
            if self.__pos[Direction.Y_AXIS] - 1 < 0:
                self.__direction = Direction.DOWN
            self.__coordinates = self.__update_position()

        elif self.__direction == Direction.DOWN:
            if self.__pos[Direction.Y_AXIS] + self.__length > self.__board_size:
                self.__direction = Direction.UP
            self.__coordinates = self.__update_position()

        elif self.__direction == Direction.LEFT:
            if self.__pos[Direction.X_AXIS] - 1 < 0:
                self.__direction = Direction.RIGHT
            self.__coordinates = self.__update_position()

        elif self.__direction == Direction.RIGHT:
            if self.__pos[Direction.X_AXIS] + self.__length > self.__board_size:
                self.__direction = Direction.LEFT
            self.__coordinates = self.__update_position()

        return self.__direction


    def __update_position(self):  # private method

        temp = deepcopy(self.coordinates())
        if self.__direction == Direction.UP:
            self.__pos = (self.__pos[Direction.X_AXIS], self.__pos[Direction.Y_AXIS] - 1)
            for i in range(len(temp)):
                temp[i] = (temp[i][Direction.X_AXIS], temp[i][Direction.Y_AXIS] - 1)

        elif self.__direction == Direction.DOWN:
            self.__pos = (self.__pos[Direction.X_AXIS], self.__pos[Direction.Y_AXIS] + 1)
            for i in range(len(temp)):
                temp[i] = (temp[i][Direction.X_AXIS], temp[i][Direction.Y_AXIS] + 1)

        elif self.__direction == Direction.LEFT:
            self.__pos = (self.__pos[Direction.X_AXIS] - 1, self.__pos[Direction.Y_AXIS])
            for i in range(len(temp)):
                temp[i] = (temp[i][Direction.X_AXIS] - 1, temp[i][Direction.Y_AXIS])

        elif self.__direction == Direction.RIGHT:
            self.__pos = (self.__pos[Direction.X_AXIS] + 1, self.__pos[Direction.Y_AXIS])
            for i in range(len(temp)):
                temp[i] = (temp[i][Direction.X_AXIS] + 1, temp[i][Direction.Y_AXIS])
        return temp

    def hit(self, pos):
        """
        Inform the ship that a bomb hit a specific coordinate. The ship updates
         its state accordingly.
        If one of the ship's body's coordinate is hit, the ship does not move
         in future turns. If all ship's body's coordinate are hit, the ship is
         terminated and removed from the board.
        :param pos: A tuple representing the (x, y) position of the hit.
        :return: True if the bomb generated a new hit in the ship, False
         otherwise.
        """
        for i in range(len(self.__coordinates)):
            if self.__coordinates[i] == pos and not self.__hit_coordinates[i]:
                self.__hit_coordinates[i] = True
                self.__direction = Direction.NOT_MOVING
                return True
        return False

    def terminated(self):
        """
        :return: True if all ship's coordinates were hit in previous turns, False
        otherwise.
        """
        for hit in self.__hit_coordinates:
            if not hit:
                return False
        return True

    def __contains__(self, pos):
        """
        Check whether the ship is found in a specific coordinate.
        :param pos: A tuple representing the coordinate for check.
        :return: True if one of the ship's coordinates is found in the given
        (x, y) coordinate, False otherwise.
        """
        for coordinate in self.__coordinates:
            if coordinate == pos:
                return True
        return False

    def coordinates(self):
        """
        Return ship's current coordinates on board.
        :return: A list of (x, y) tuples representing the ship's current
        occupying coordinates.
        """
        return self.__coordinates

    def damaged_cells(self):
        """
        Return the ship's hit positions.
        :return: A list of tuples representing the (x, y) coordinates of the
         ship which were hit in past turns (If there are no hit coordinates,
         return an empty list). There is no importance to the order of the
         values in the returned list.
        """
        damaged = list()
        for i in range(len(self.__hit_coordinates)):
            if self.__hit_coordinates[i]:
                damaged.append(self.__coordinates[i])
        return damaged

    def not_damaged_cells(self):

        damaged = list()
        for i in range(len(self.__hit_coordinates)):
            if not self.__hit_coordinates[i]:
                damaged.append(self.__coordinates[i])
        return damaged

    def direction(self):
        """
        Return the ship's current sailing direction.
        :return: One of the constants of Direction class :
         [UP, DOWN, LEFT, RIGHT] according to current sailing direction or
         NOT_MOVING if the ship is hit and not moving.
        """
        return self.__direction

    def cell_status(self, pos):
        """
        Return the status of the given coordinate (hit\not hit) in current ship.
        :param pos: A tuple representing the coordinate to query.
        :return:
            if the given coordinate is not hit : False
            if the given coordinate is hit : True
            if the coordinate is not part of the ship's body : None 
        """
        for i in range(len(self.__coordinates)):
            if self.__coordinates[i] == pos:
                return self.__hit_coordinates[i]
        return None

