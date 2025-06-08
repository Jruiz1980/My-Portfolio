"""
Handles mouse input for the chess game.
"""
import arcade
import copy # For deepcopying board state during simulation
from components.pieces import Piece, Pawn # For type hinting
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
                    
                    # Check if the move is a capture
                    captured_piece = self.get_piece_object_at_coords(row, col) # Piece at destination before move
                    if captured_piece and captured_piece.color != self.selected_piece_object.color:
                        # Remove captured piece
                        self.game.all_piece_objects.remove(captured_piece)
                        self.game.piece_sprites.remove(captured_piece.sprite)
                        print(f"Captured {captured_piece.piece_type} at ({row}, {col})")

                    # Update piece's board position and sprite
                    self.selected_piece_object.row = row
                    self.selected_piece_object.col = col
                    self.selected_piece_object.update_sprite_position()
                    print(f"Moved {self.selected_piece_object.piece_type} to ({row}, {col})")

                    # Check for pawn promotion
                    is_pawn = isinstance(self.selected_piece_object, Pawn)
                    is_promotion_rank_white = (self.selected_piece_object.color == self.game.WHITE and \
                                               row == self.game.BOARD_SIZE - 1)
                    is_promotion_rank_black = (self.selected_piece_object.color == self.game.BLACK and \
                                               row == 0)

                    if is_pawn and (is_promotion_rank_white or is_promotion_rank_black):
                        print(f"Pawn promotion for {self.selected_piece_object.color} at ({row}, {col})")
                        self.game.promoting_pawn = self.selected_piece_object
                        self.game.game_state = self.game.c.PAWN_PROMOTION
                        self.selected_piece_object = None # Move complete, awaiting promotion choice
                        self.possible_moves_coords = []
                        return # Skip turn switch and check for now
                    else:
                        # Switch turn
                        self.game.current_turn = self.game.BLACK if self.game.current_turn == self.game.WHITE else self.game.WHITE
                        print(f"Turn: {self.game.current_turn}")
                        # Check for check
                        self._check_for_check()

                    # Deselect piece (if not promoting)
                    self.selected_piece_object = None
                    self.possible_moves_coords = []
                else:
                    print(f"Invalid move for {self.selected_piece_object.piece_type} to ({row}, {col})")
                    self.selected_piece_object = None # Deselect on invalid move too
                    self.possible_moves_coords = []

            elif clicked_piece_object:
                # No piece selected, and clicked on a piece: select it
                self.selected_piece_object = clicked_piece_object
                # Only allow selecting pieces of the current turn's color
                if self.selected_piece_object.color == self.game.current_turn:
                    print(f"Selected {self.selected_piece_object.piece_type} at ({row}, {col})")
                    self._calculate_possible_moves()
                else:
                    self.selected_piece_object = None # Not this player's turn
                    print(f"Cannot select piece. It's {self.game.current_turn}'s turn.")
            else:
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
                    if move_logic.is_move_valid(self.selected_piece_object, r, c, self.game.all_piece_objects, self.game.BOARD_SIZE):
                        # Pseudo-legal move found, now check if it leaves the king in check
                        
                        # 1. Create a deep copy of the current board state for simulation
                        #    We only need to copy the logical attributes, not the sprite.
                        sim_all_pieces = []
                        for p_orig in self.game.all_piece_objects:
                            # Manually create a new Piece instance or a simple data structure
                            # For simplicity, let's assume Piece can be instantiated with its core attributes
                            # and doesn't strictly need a sprite for logical simulation.
                            # This requires your Piece subclasses to handle this.
                            # A more robust way is to add a .clone() method to your Piece class.
                            sim_p = p_orig.__class__(p_orig.color, p_orig.row, p_orig.col) # Re-create piece
                            sim_all_pieces.append(sim_p)

                        # 2. Find the piece to be moved in the simulated state
                        #    and the piece at the target square in the simulated state
                        sim_moving_piece = None
                        sim_piece_at_target = None
                        
                        for p_sim in sim_all_pieces:
                            # Match by original position and attributes, as deepcopy creates new objects
                            if p_sim.row == self.selected_piece_object.row and \
                               p_sim.col == self.selected_piece_object.col and \
                               p_sim.piece_type == self.selected_piece_object.piece_type and \
                               p_sim.color == self.selected_piece_object.color:
                                sim_moving_piece = p_sim
                            
                            if p_sim.row == r and p_sim.col == c: # Piece at destination in sim
                                sim_piece_at_target = p_sim
                        
                        if not sim_moving_piece:
                            print(f"Error: Simulated moving piece not found for {self.selected_piece_object.piece_type} from ({self.selected_piece_object.row},{self.selected_piece_object.col})")
                            continue # Should not happen if selected_piece_object is valid

                        # 3. Perform the move in the simulated state
                        #    If it's a capture, remove the captured piece from the simulated list
                        if sim_piece_at_target and sim_piece_at_target.color != sim_moving_piece.color:
                            sim_all_pieces.remove(sim_piece_at_target) 
                            # Note: Ensure sim_piece_at_target is the correct object from sim_all_pieces if multiple pieces could be at (r,c) before move
                            # This is generally safe as only one piece can occupy a square.
                        
                        sim_moving_piece.row = r
                        sim_moving_piece.col = c
                        
                        # 4. Check if the current player's king is in check in the simulated state
                        if not move_logic.is_king_in_check(self.selected_piece_object.color, 
                                                           sim_all_pieces, 
                                                           self.game.BOARD_SIZE):
                            self.possible_moves_coords.append((r, c))

    def _check_for_check(self):
        """Checks if the current player's king is in check."""
        # The turn has already switched, so we check the king of the player whose turn it now is.
        # However, for announcing "Check!", we are interested if the move JUST MADE put the OPPONENT in check.
        # So, we check the king of the player whose turn it just became.
        king_to_check_color = self.game.current_turn
        opponent_color = self.game.BLACK if king_to_check_color == self.game.WHITE else self.game.WHITE
        
        if move_logic.is_king_in_check(king_to_check_color, self.game.all_piece_objects, self.game.BOARD_SIZE):
            print(f"CHECK! {king_to_check_color} king is in check.")
            # Here you could also set a flag in MyGame to display "Check!" on screen