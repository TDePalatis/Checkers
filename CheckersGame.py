"""
Checkers game engine.

Implements a two-player Checkers game (with kings and triple kings) using an
object-oriented design. The main public API is the `Checkers` class, which
manages the board, turn order, move validation, capturing, promotion, and
game winner detection, and the `Player` class, which tracks per-player stats.

Public API (as required by the original assignment):

- Checkers.create_player(player_name: str, piece_color: str) -> Player
- Checkers.play_game(player_name: str,
                     start: tuple[int, int],
                     dest: tuple[int, int]) -> int
- Checkers.get_checker_details(square: tuple[int, int]) -> str | None
- Checkers.print_board() -> None
- Checkers.game_winner() -> str

- Player.get_king_count() -> int
- Player.get_triple_king_count() -> int
- Player.get_captured_pieces_count() -> int
"""

class OutofTurn(Exception):
    """Raised when a player attempts to move out of turn."""
    pass


class InvalidSquare(Exception):
    """Raised when a square is off-board or otherwise invalid."""
    pass


class InvalidPlayer(Exception):
    """Raised when a player name is not recognized."""
    pass


class InvalidMove(Exception):
    """Raised when a move violates the rules of Checkers."""
    pass



class Checkers:
    """
    A class that sets up a game of checkers, including a board, basic stats,
    and the options to create players and take input that will move it’s pieces
    and determine if there is a winner.
    """

    def __init__(self):
        """
        Initializes the board, turn color, game status, a winner, the last destination, and
        if the last turn was finished. It takes no parameters. All data members are private.
        """
        self._board = [[None, "White", None, "White", None, "White", None, "White"],
                       ["White", None, "White", None, "White", None, "White", None],
                       [None, "White", None, "White", None, "White", None, "White"],
                       ["Empty", None, "Empty", None, "Empty", None, "Empty", None],
                       [None, "Empty", None, "Empty", None, "Empty", None, "Empty"],
                       ["Black", None, "Black", None, "Black", None, "Black", None],
                       [None, "Black", None, "Black", None, "Black", None, "Black"],
                       ["Black", None, "Black", None, "Black", None, "Black", None],]

        self._players = []
        self._turn = "Black"
        self._game_status = "Active"
        self._winner = None
        self._last_destination = None
        self._last_turn_finished = True

    def _is_on_board(self, row, col):
        """
        Return True if (row, col) is a valid board coordinate.
        """
        return 0 <= row <= 7 and 0 <= col <= 7

    def get_board(self):
        """
        Return the internal board representation.

        Returns:
            list[list[str | None]]:
                A nested list representing the 8×8 game board.
                Each element may be:
                    - None
                    - "White", "Black"
                    - "White_king", "Black_king"
                    - "White_Triple_King", "Black_Triple_King"

        Notes:
            This method exposes the board state primarily for debugging
            and unit testing purposes.
        """
        return self._board

    def get_player_object(self, player_name):
        """
        Retrieve the Player object for the given player name.

        Args:
            player_name (str): The name of the player to retrieve.

        Returns:
            Player:
                The Player instance associated with the given name.

        Raises:
            InvalidPlayer:
                If the name does not correspond to any existing player.
        """

        for player in self._players:
            if player_name == player.get_player_name():
                return player

        raise InvalidPlayer(f"Unknown player: {player_name}")


    def get_turn(self):
        """
        Gets the color of the current turn. Used to identify if it is the
        current players turn and as reference for changing the color when
        a turn is completed.
        """
        return self._turn

    def change_turn(self):
        """
        Changes the color of the current turn to set up the next turn.
        Used at the end of each turn.
        """
        turn = self.get_turn()

        if turn == "Black":
            self._turn = "White"

        elif turn == "White":
            self._turn = "Black"

    def get_last_destination(self):
        """
        Return the most recent destination square of the last completed move.

        Returns:
            tuple[int, int] | None:
                A (row, col) tuple indicating where the last move ended,
                or None if no moves have been played yet.

        Notes:
            Useful for debugging, UI display, and validating multi-jump sequences.
        """

        return self._last_destination

    def get_last_turn_finished(self):
        """
        Indicate whether the last player's turn fully completed.

        Returns:
            bool:
                True if the previous turn ended (no forced continuation),
                False if a multi-jump sequence must continue or
                if no moves have occurred yet.

        Notes:
            This supports correct enforcement of forced multi-jump behavior.
        """

        return self._last_turn_finished


    def get_status(self):
        """
        Returns the game status to determine if the game is active or if it is over.
        """

        return self._game_status

    def end_game(self, player_name):
        """
        Changes the game's status to over and records the winner as the players name.
        """

        self._game_status = "Over"
        self._winner = player_name



    def create_player(self, player_name, piece_color):
        """
        Create a new player and add them to the game.

        Args:
            player_name (str): Name of the player (must be unique).
            piece_color (str): "Black" or "White".

        Returns:
            Player: The created Player object.

        Raises:
            InvalidPlayer: If the color is invalid or a player with that
                           name already exists.        
        """
        if piece_color not in ("Black", "White"):
            raise InvalidPlayer(f"Invalid piece color: {piece_color}")

        # Enforce unique player names
        for player in self._players:
            if player.get_player_name() == player_name:
                raise InvalidPlayer(f"Player name already exists: {player_name}")

        player = Player(player_name, piece_color)
        self._players.append(player)
        return player

    def play_game(self, player_name, starting_square_location, destination_square_location):
        """
        Execute a move for the given player.

        Args:
            player_name (str): Name of the player making the move.
            starting_square_location (tuple[int, int]): (row, col) of the
                piece to move.
            destination_square_location (tuple[int, int]): (row, col) of the
                target square.

        Returns:
            int: Number of opponent pieces captured during this move (0 if none).

        Raises:
            OutofTurn: If it is not this player's turn.
            InvalidPlayer: If the player name is unknown.
            InvalidSquare: If either square is invalid or does not contain
                           a piece the player owns.
            InvalidMove: If the move does not comply with the rules.
        """

        player_object = self.get_player_object(player_name)

        piece = self.get_checker_details(starting_square_location)

        if piece is None:
            raise InvalidSquare  # no piece at starting location

        color = player_object.get_piece_color()

        if color == "White" and not piece.startswith("White"):
            raise InvalidSquare

        if color == "Black" and not piece.startswith("Black"):
            raise InvalidSquare

        movement_direction_x = int((destination_square_location[0] - starting_square_location[0]))

        movement_direction_y = int((destination_square_location[1] - starting_square_location[1]))

        # Enforce diagonal movement:
        # - Simple moves: exactly 1 square diagonally
        # - Jump moves: exactly 2 squares diagonally
        if not (
            (abs(movement_direction_x) == 1 and abs(movement_direction_y) == 1) or
            (abs(movement_direction_x) == 2 and abs(movement_direction_y) == 2)
        ):
            raise InvalidMove

        if starting_square_location == self.get_last_destination() and not self.get_last_turn_finished():
            self.change_turn()
            self._last_turn_finished = True


        if self.get_turn() != player_object.get_piece_color():
            raise OutofTurn

        if starting_square_location[0] > 7 or starting_square_location[1] > 7:
            raise InvalidSquare

        if starting_square_location[0] < 0 or starting_square_location[1] < 0:
            raise InvalidSquare

        if destination_square_location[0] > 7 or destination_square_location[1] > 7:
            raise InvalidSquare

        if destination_square_location[0] < 0 or destination_square_location[1] < 0:
            raise InvalidSquare

        if self._board[starting_square_location[0]][starting_square_location[1]] is None or\
                self._board[destination_square_location[0]][destination_square_location[1]] is None:
            raise InvalidSquare

        if self._board[starting_square_location[0]][starting_square_location[1]] == "White" and\
                movement_direction_x <= 0:
            raise InvalidMove

        if self._board[starting_square_location[0]][starting_square_location[1]] == "Black" and\
                movement_direction_x >= 0:
            raise InvalidMove

        if self._board[destination_square_location[0]][destination_square_location[1]] != "Empty":
            raise InvalidMove


        else:

            start_checker = self._board[starting_square_location[0]][starting_square_location[1]]


            self._board[destination_square_location[0]][destination_square_location[1]] = \
                self.get_checker_details(starting_square_location)
            self._board[starting_square_location[0]][starting_square_location[1]] = "Empty"

            jumped_piece = (int((starting_square_location[0] + destination_square_location[0]) / 2),
                            int((starting_square_location[1] + destination_square_location[1]) / 2))

            jumped_piece_color = self.get_checker_details(jumped_piece)

            jumped_check = int((jumped_piece[0] - starting_square_location[0]))


            #Code for jumping

            if abs(movement_direction_x) == 2 and abs(destination_square_location[1] - starting_square_location[1]) == 2 and \
                abs(jumped_check) == 1:

                white_pieces = ("White", "White_king", "White_Triple_king")
                black_pieces = ("Black", "Black_king", "Black_Triple_king")

                if start_checker in white_pieces and jumped_piece_color in black_pieces:
                    self._board[jumped_piece[0]][jumped_piece[1]] = "Empty"
                    player_object.add_captured_piece_count()

                elif start_checker in black_pieces and jumped_piece_color in white_pieces:
                    self._board[jumped_piece[0]][jumped_piece[1]] = "Empty"
                    player_object.add_captured_piece_count()

                elif start_checker in white_pieces and jumped_piece_color in white_pieces:
                    raise InvalidMove

                elif start_checker in black_pieces and jumped_piece_color in black_pieces:
                    raise InvalidMove


            #Code for King creation
            if destination_square_location[0] == 0 and self.get_checker_details(destination_square_location) == "Black": # Creation of black king
                self._board[destination_square_location[0]][destination_square_location[1]] = "Black_king"
                player_object.add_king()

            if destination_square_location[0] == 7 and self.get_checker_details(destination_square_location) == "White": # Creation of white king
                self._board[destination_square_location[0]][destination_square_location[1]] = "White_king"
                player_object.add_king()

            if destination_square_location[0] == 0 and self.get_checker_details(destination_square_location) == "White_king":  # Creation of white triple king
                self._board[destination_square_location[0]][destination_square_location[1]] = "White_Triple_king"
                player_object.add_triple_king()

            if destination_square_location[0] == 7 and self.get_checker_details(destination_square_location) == "Black_king":  # Creation of black triple king
                self._board[destination_square_location[0]][destination_square_location[1]] = "Black_Triple_king"
                player_object.add_triple_king()


            if player_object.get_captured_pieces_count() == 12:
                self.end_game(player_name)

            
            # Code for multiple jumps (edge-safe)
            dest_row, dest_col = destination_square_location
            piece_after_move = self._board[dest_row][dest_col]

            white_pieces = ("White", "White_king", "White_Triple_king")
            black_pieces = ("Black", "Black_king", "Black_Triple_king")

            # Directions: up-left, up-right, down-left, down-right
            directions = [(-1, -1), (-1, 1), (1, -1), (1, 1)]

            has_more_jumps = False

            for dr, dc in directions:
                mid_r, mid_c = dest_row + dr, dest_col + dc
                land_r, land_c = dest_row + 2 * dr, dest_col + 2 * dc

                # Skip if either square is off-board
                if not (self._is_on_board(mid_r, mid_c) and self._is_on_board(land_r, land_c)):
                    continue

                mid_piece = self._board[mid_r][mid_c]
                landing_square = self._board[land_r][land_c]

                if landing_square != "Empty":
                    continue

                # For normal pieces, restrict direction (Black moves up, White moves down)
                if piece_after_move == "Black" and dr != -1:
                    continue
                if piece_after_move == "White" and dr != 1:
                    continue
                # Kings and triple kings can move in all directions

                if piece_after_move in white_pieces and mid_piece in black_pieces:
                    has_more_jumps = True
                    break

                if piece_after_move in black_pieces and mid_piece in white_pieces:
                    has_more_jumps = True
                    break

            if has_more_jumps:
                self._last_turn_finished = False


        self._last_destination = destination_square_location

        self.change_turn()

        return player_object.get_captured_pieces_count()


    def get_checker_details(self, square_location):
        """
        Return the contents of the given board square.

        Args:
            square_location (tuple[int, int]):
                A (row, col) tuple representing a board position.

        Returns:
            str | None:
                - "White" for a normal white piece
                - "Black" for a normal black piece
                - "White_king" or "Black_king" for king pieces
                - "White_Triple_King" or "Black_Triple_King" for triple kings
                - None if the square is empty

        Raises:
            InvalidSquare:
                If the square is outside the bounds of the board.
        """

        x_coord, y_coord = square_location

        if x_coord < 0 or x_coord > 7 or y_coord < 0 or y_coord > 7:
            raise InvalidSquare

        checker = self._board[x_coord][y_coord]

        if checker == "Empty":
            return None
        else:
            return checker

    def print_board(self):
        """
        Print the current board state as a nested list.

        Output Format:
            A printed 2-D list representing the 8×8 board.
            Example row:
                [None, "White", None, "White", None, "White", None, "White"]

        Notes:
            - Only dark squares contain pieces; light squares remain None.
            - This function prints the board but does not return it.
        """

        print(self.get_board())

    def game_winner(self):
        """
        Determine whether the game has ended and return the winning player.

        Returns:
            str:
                - The name of the winning player if the opponent has no remaining pieces.
                - "Game has not ended" if both players still have pieces on the board.

        Notes:
            This method does NOT evaluate whether a player has no legal moves.
        """

        if self.get_status() != "Over":
            return "Game has not ended"
        else:
            winner = self._winner

            return winner


class Player:
    """
    Creates a player with a name and piece color. Used frequently throughout Checkers.
    """
    def __init__(self, player_name, piece_color):
        """
        Creates a player with a name and piece color from the two parameters taken.
        Values for king, triple king, and captured pieces are set to 0.
        """
        self._player_name = player_name
        self._piece_color = piece_color
        self._king = 0
        self._triple_king = 0
        self._captured_piece = 0


    def get_player_name(self):
        """
        Gets the name of the player.
        """
        return self._player_name

    def get_piece_color(self):
        """
        Gets the piece color of the player.
        """
        return self._piece_color

    def get_king_count(self):
        """
        Gets the number of kings .
        """
        return self._king

    def add_king(self):
        """
        Adds a king to the players count.
        """
        self._king = self._king + 1

    def get_triple_king_count(self):
        """
        Gets the number of triple kings the player has .
        """
        return self._triple_king

    def add_triple_king(self):
        """
        Adds a triple king to the players count.
        """
        self._triple_king = self._triple_king + 1

    def get_captured_pieces_count(self):
        """
        Gets the number of pieces the player has captured.
        """
        captured_piece_number = self._captured_piece

        return captured_piece_number

    def add_captured_piece_count(self):
        """
        Gets the number of pieces the player has captured.
        """
        self._captured_piece = self._captured_piece + 1

