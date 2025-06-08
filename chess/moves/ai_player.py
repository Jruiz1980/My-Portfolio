# c:\Users\hualc\OneDrive-BYU-Idaho\Documents\Portfolio\My-Portfolio\chess\moves\ai_player.py
import random
from components.pieces import Piece # For type hinting
# Import move_logic if needed for specific AI strategies, not for random moves via InputHandler

class AIPlayer:
    def __init__(self, game_instance, color: str):
        self.game = game_instance
        self.color = color # The color this AI plays as

    def choose_move(self) -> tuple[Piece, tuple[int, int]] | None:
        """
        Chooses a random legal move for the AI.
        Returns: (piece_to_move, (dest_row, dest_col)) or None if no legal moves.
        """
        # We'll use a method in InputHandler to get all legal moves
        # This keeps the move generation logic centralized
        all_legal_moves = self.game.input_handler.get_all_legal_moves_for_player(self.color)
        print(f"DEBUG: AI ({self.color}) found {len(all_legal_moves)} legal moves: {[(m[0].piece_type, m[1]) for m in all_legal_moves]}")


        if not all_legal_moves:
        # It's useful to know if the game should have ended here
            print(f"DEBUG: AI ({self.color}) has no legal moves. Is king in check? {self.game.input_handler.move_logic.is_king_in_check(self.color, self.game.all_piece_objects, self.game.BOARD_SIZE)}")
            return None # No legal moves (checkmate or stalemate)

        return random.choice(all_legal_moves)


