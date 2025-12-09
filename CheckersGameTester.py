# Author: Trevor DePalatis
# GitHub username: TDePalatis
# Date: 3/14/2023 (updated for portfolio)
# Description: Unit tests for the Checkers game engine.

import unittest

from CheckersGame import (
    Checkers,
    Player,
    InvalidPlayer,
    InvalidMove,
    InvalidSquare,
    OutofTurn,
)


class TestCheckers(unittest.TestCase):
    """
    Unit tests for the Checkers game engine.
    """

    def setUp(self):
        """
        Create a fresh game and two players for each test.
        """
        self.game = Checkers()
        self.black = self.game.create_player("Trevor", "Black")
        self.white = self.game.create_player("Rovert", "White")

    # ----------------------------------------------------------------------
    # Basic player and board tests
    # ----------------------------------------------------------------------

    def test_create_player_and_get_player_object(self):
        """
        Players are created correctly and stored in the game.
        """
        player = self.game.get_player_object("Trevor")
        self.assertIsInstance(player, Player)
        self.assertEqual(player.get_player_name(), "Trevor")
        self.assertEqual(player.get_piece_color(), "Black")

    def test_get_checker_details_after_simple_moves(self):
        """
        get_checker_details() returns the correct piece after valid moves.
        """
        # Black moves first
        self.game.play_game("Trevor", (5, 6), (4, 7))
        # White moves
        self.game.play_game("Rovert", (2, 1), (3, 0))

        self.assertEqual(self.game.get_checker_details((3, 0)), "White")
        self.assertIsNone(self.game.get_checker_details((2, 1)))

    # ----------------------------------------------------------------------
    # Capturing and promotion tests
    # ----------------------------------------------------------------------

    def test_single_capture_increments_captured_count(self):
        """
        A simple jump should increment the capturing player's captured pieces.
        """
        # Setup a capture: Black and White move toward each other.
        self.game.play_game("Trevor", (5, 2), (4, 3))
        self.game.play_game("Rovert", (2, 5), (3, 4))
        # Now Black captures White
        self.game.play_game("Trevor", (4, 3), (2, 5))

        self.assertEqual(self.black.get_captured_pieces_count(), 1)

    def test_promotion_to_king(self):
        """
        Moving a piece to the far side should promote it to a king.
        (Uses the sequence you originally wrote in test_4.)
        """
        self.game.play_game("Trevor", (5, 2), (4, 3))
        self.game.play_game("Rovert", (2, 5), (3, 4))
        self.game.play_game("Trevor", (4, 3), (2, 5))  # capture
        self.game.play_game("Rovert", (2, 3), (3, 2))
        self.game.play_game("Trevor", (5, 6), (4, 7))
        self.game.play_game("Rovert", (1, 2), (2, 3))
        self.game.play_game("Trevor", (4, 7), (3, 6))
        self.game.play_game("Rovert", (0, 3), (1, 2))
        self.game.play_game("Trevor", (2, 5), (0, 3))  # reach back row

        self.assertEqual(self.black.get_king_count(), 1)

    def test_king_can_capture_backwards(self):
        """
        A promoted king should be able to capture moving backwards.
        (Uses your original test_5 sequence.)
        """
        self.game.play_game("Trevor", (5, 2), (4, 3))
        self.game.play_game("Rovert", (2, 5), (3, 4))
        self.game.play_game("Trevor", (4, 3), (2, 5))  # capture
        self.game.play_game("Rovert", (2, 3), (3, 2))
        self.game.play_game("Trevor", (5, 6), (4, 7))
        self.game.play_game("Rovert", (1, 2), (2, 3))
        self.game.play_game("Trevor", (4, 7), (3, 6))
        self.game.play_game("Rovert", (0, 3), (1, 2))
        self.game.play_game("Trevor", (2, 5), (0, 3))  # promote to king
        self.game.play_game("Rovert", (2, 1), (3, 0))
        self.game.play_game("Trevor", (0, 3), (2, 1))  # backward capture as king

        self.assertEqual(self.black.get_captured_pieces_count(), 3)

    # ----------------------------------------------------------------------
    # Error / exception tests
    # ----------------------------------------------------------------------

    def test_invalid_player_name_raises(self):
        """
        Playing a move with an unknown player name should raise InvalidPlayer.
        """
        with self.assertRaises(InvalidPlayer):
            self.game.play_game("NotAPlayer", (5, 0), (4, 1))

    def test_out_of_turn_raises(self):
        """
        White moving first should raise OutofTurn since Black always moves first.
        """
        with self.assertRaises(OutofTurn):
            self.game.play_game("Rovert", (2, 1), (3, 0))

    def test_invalid_square_off_board_raises(self):
        """
        Using a square that is off the board should raise InvalidSquare.
        """
        with self.assertRaises(InvalidSquare):
            self.game.play_game("Trevor", (8, 0), (7, 1))

        with self.assertRaises(InvalidSquare):
            self.game.play_game("Trevor", (5, 0), (8, 1))

    def test_invalid_move_not_diagonal_raises(self):
        """
        Non-diagonal moves should raise InvalidMove.
        """
        # Valid first move
        self.game.play_game("Trevor", (5, 2), (4, 3))

        # White tries a non-diagonal move
        with self.assertRaises(InvalidMove):
            self.game.play_game("Rovert", (2, 1), (2, 3))

    def test_game_winner_before_end(self):
        """
        Before the game ends, game_winner should report that the game has not ended.
        """
        self.assertEqual(self.game.game_winner(), "Game has not ended")


if __name__ == "__main__":
    unittest.main()
