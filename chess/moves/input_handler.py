"""
Handles mouse input for the chess game.
"""
import arcade
from ..components.pieces import Piece # For type hinting
from moves import move_logic # To use move validation

class InputHandler:
    def __init__(self, game_instance):
        self.game = game_instance  # Reference to the MyGame instance
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
                # You might want to visually deselect (e.g., remove highlight)

            elif clicked_piece_object:
                # No piece selected, and clicked on a piece: select it
                self.selected_piece_object = clicked_piece_object
                print(f"Selected {self.selected_piece_object.piece_type} at ({row}, {col})")
                # You might want to visually highlight the selected piece here
            else:
                # Clicked on an empty square and no piece selected
                self.selected_piece_object = None # Ensure deselection
                print("Clicked on an empty square.")