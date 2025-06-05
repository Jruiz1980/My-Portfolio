"""
Handles mouse input for the chess game.
"""
import arcade
from components.pieces import Piece # For type hinting
from moves import move_logic # Corrected: import move_logic from parent directory

class InputHandler:
    def __init__(self, game_instance):
        self.game = game_instance  # Reference to the MyGame instance
        self.possible_moves_coords: list[tuple[int, int]] = [] # Store (row, col) of possible moves
        self.selected_piece_object: Piece | None = None

    def screen_to_board_coords(self, screen_x: int, screen_y: int) -> tuple[int, int] | None:
        """Converts screen pixel coordinates to board row and column."""
        if screen_x < self.game.MARGIN or screen_x > self.game.MARGIN + self.game.board_pixel_width or \
        screen_y < self.game.MARGIN or screen_y > self.game.MARGIN + self.game.board_pixel_height:
            return None  # Click was outside the board

        col = (screen_x - self.game.MARGIN) // self.game.SQUARE_SIZE
        row = (screen_y - self.game.MARGIN) // self.game.SQUARE_SIZE
        return row, col

    def get_piece_object_at_coords(self, board_row: int, board_col: int) -> Piece | None:
        """Finds the Piece object at the given board coordinates."""
        for piece_obj in self.game.all_piece_objects:
            if piece_obj.row == board_row and piece_obj.col == board_col:
                return piece_obj
        return None

    def on_mouse_press(self, x: int, y: int, button: int, modifiers: int):
        if button == arcade.MOUSE_BUTTON_LEFT:
            board_coords = self.screen_to_board_coords(x, y)
            if not board_coords:
                return # Clicked outside board

            row, col = board_coords
            clicked_piece_object = self.get_piece_object_at_coords(row, col)

            if self.selected_piece_object:
                # A piece is already selected, try to move it
                if move_logic.is_move_valid(self.selected_piece_object, row, col,
                                            self.game.all_piece_objects, self.game.BOARD_SIZE):
                    # Valid move: Update piece's board position
                    self.selected_piece_object.row = row
                    self.selected_piece_object.col = col
                    # Update the sprite's screen position
                    self.selected_piece_object.update_sprite_position()
                    print(f"Moved {self.selected_piece_object.piece_type} to ({row}, {col})")
                else:
                    print(f"Invalid move for {self.selected_piece_object.piece_type} to ({row}, {col})")
                
                # Deselect piece whether move was valid or not (for simplicity here)
                self.selected_piece_object = None
                self.possible_moves_coords = [] # Clear possible moves
                # You might want to visually deselect (e.g., remove highlight)

            elif clicked_piece_object:
                # No piece selected, and clicked on a piece: select it
                self.selected_piece_object = clicked_piece_object
                print(f"Selected {self.selected_piece_object.piece_type} at ({row}, {col})")
                # You might want to visually highlight the selected piece here
                self._calculate_possible_moves()
            else:
                # Clicked on an empty square and no piece selected
                self.selected_piece_object = None # Ensure deselection
                self.possible_moves_coords = [] # Clear possible moves
                print("Clicked on an empty square.")

    def _calculate_possible_moves(self):
        """Calculates and stores valid moves for the selected piece."""
        self.possible_moves_coords = []
        if self.selected_piece_object:
            # Iterate through all possible squares on the board
            for r in range(self.game.BOARD_SIZE):
                for c in range(self.game.BOARD_SIZE):
                    # Check if the move to (r, c) is valid for the selected piece
                    if move_logic.is_move_valid(self.selected_piece_object, r, c,
                                                self.game.all_piece_objects, self.game.BOARD_SIZE):
                        self.possible_moves_coords.append((r, c))