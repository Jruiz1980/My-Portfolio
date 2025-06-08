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

        col = int((screen_x - self.game.MARGIN) // self.game.SQUARE_SIZE)
        row = int((screen_y - self.game.MARGIN) // self.game.SQUARE_SIZE)
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

            row, col = map(int, board_coords) # Ensure row and col are integers
            clicked_piece_object = self.get_piece_object_at_coords(row, col)

            if self.selected_piece_object:
                # A piece is already selected, try to move it
                # A move is valid if it's in the pre-calculated possible_moves_coords,
                # which already ensures the move doesn't leave the current player's king in check.
                if (row, col) in self.possible_moves_coords:
                    
                    # --- For Algebraic Notation: Store info BEFORE the move ---
                    original_piece_info = {
                        "row": int(self.selected_piece_object.row), # Ensure int
                        "col": int(self.selected_piece_object.col), # Ensure int
                        "type": self.selected_piece_object.piece_type,
                        "color": self.selected_piece_object.color
                    }
                    # Create a snapshot of the board *before* the move for disambiguation logic
                    all_pieces_before_current_move = [p.__class__(p.color, p.row, p.col) for p in self.game.all_piece_objects]
                    
                    # Check if the move is a capture
                    captured_piece = self.get_piece_object_at_coords(row, col) # Piece at destination before move
                    if captured_piece and captured_piece.color != self.selected_piece_object.color:
                        # Remove captured piece
                        self.game.all_piece_objects.remove(captured_piece)
                        self.game.piece_sprites.remove(captured_piece.sprite)
                        print(f"Captured {captured_piece.piece_type} at ({row}, {col})")
                    was_capture_for_notation = captured_piece is not None

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
                        # Algebraic notation for promotion will be handled after choice.
                        # For now, the move itself is to the promotion square.
                        # We can print a partial notation here or wait for full after promotion.
                        
                        # Determine check/checkmate status *caused by pawn reaching promotion square*
                        opponent_color_promo = self.game.BLACK if original_piece_info["color"] == self.game.WHITE else self.game.WHITE
                        check_caused_by_promo_move = move_logic.is_king_in_check(opponent_color_promo, self.game.all_piece_objects, self.game.BOARD_SIZE)
                        checkmate_caused_by_promo_move = False
                        if check_caused_by_promo_move:
                            if not self._has_legal_moves(opponent_color_promo):
                                checkmate_caused_by_promo_move = True

                        # Print notation for pawn moving to promotion square (promotion piece itself is not yet chosen)
                        promo_move_alg = move_logic.format_move_to_algebraic(
                            all_pieces_before_current_move, self.game.BOARD_SIZE,
                            original_piece_info["row"], original_piece_info["col"], original_piece_info["type"], original_piece_info["color"],
                            row, col, was_capture_for_notation,
                            None, # No promotion piece char yet
                            check_caused_by_promo_move, checkmate_caused_by_promo_move
                        )
                        # print(f"Move to promotion square: {promo_move_alg}") # e.g., "e8" or "dxc8"
                        self.game.move_history.append(promo_move_alg) # Add base move to history

                        self.game.game_state = self.game.c.PAWN_PROMOTION
                        self.selected_piece_object = None # Move complete, awaiting promotion choice
                        self.possible_moves_coords = []
                        return # Skip turn switch and check for now
                    else:
                        # Switch turn
                        # --- For Algebraic Notation: Determine check/mate status caused by THIS move ---
                        opponent_color = self.game.BLACK if original_piece_info["color"] == self.game.WHITE else self.game.WHITE
                        check_caused_by_move = move_logic.is_king_in_check(opponent_color, self.game.all_piece_objects, self.game.BOARD_SIZE)
                        checkmate_caused_by_move = False
                        if check_caused_by_move:
                            if not self._has_legal_moves(opponent_color): # Checks opponent based on current board
                                checkmate_caused_by_move = True
                            # else: # It's a check, but not mate
                                # self.game.show_check_message_timer = self.game.c.CHECK_MESSAGE_DURATION
                                # This will be handled by _check_for_check after turn switch

                        alg_notation = move_logic.format_move_to_algebraic(
                            all_pieces_before_current_move, self.game.BOARD_SIZE,
                            original_piece_info["row"], original_piece_info["col"], original_piece_info["type"], original_piece_info["color"],
                            row, col, # dest_row, dest_col
                            was_capture_for_notation,
                            None, # promoted_to_piece_type_char (None for non-promotion moves)
                            check_caused_by_move,
                            checkmate_caused_by_move
                        )
                        print(f"Move: {alg_notation}")
                        self.game.move_history.append(alg_notation)

                        # Switch turn (if not promoting)
                        self.game.current_turn = opponent_color
                        print(f"Turn: {self.game.current_turn}")

                        # Deselect piece before checking for mate for the new turn
                        self.selected_piece_object = None
                        self.possible_moves_coords = []
                        self._check_for_check() # This will now also check for mate/stalemate for the player whose turn it became
                        
                        if self.game.game_state == self.game.c.GAME_OVER:
                            return

                else:
                    print(f"Invalid move for {self.selected_piece_object.piece_type} to ({row}, {col})")
                    self.selected_piece_object = None # Deselect on invalid move too
                    self.possible_moves_coords = []

            elif clicked_piece_object:
                # No piece selected, and clicked on a piece: select it
                # Only allow selecting pieces of the current turn's color
                if clicked_piece_object.color == self.game.current_turn:
                    self.selected_piece_object = clicked_piece_object
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
    
    def _has_legal_moves(self, player_color: str) -> bool:
        """
        Checks if the given player has any legal moves on the current game board state.
        (self.game.all_piece_objects).
        """
        for piece_to_move in self.game.all_piece_objects:
            if piece_to_move.color == player_color:
                for r_target in range(self.game.BOARD_SIZE):
                    for c_target in range(self.game.BOARD_SIZE):
                        if move_logic.is_move_valid(piece_to_move, r_target, c_target,
                                                    self.game.all_piece_objects, self.game.BOARD_SIZE):
                            # Simulate this pseudo-legal move
                            sim_all_pieces_after_move = []
                            for p_orig in self.game.all_piece_objects:
                                sim_p = p_orig.__class__(p_orig.color, p_orig.row, p_orig.col)
                                if hasattr(p_orig, 'has_moved'): sim_p.has_moved = p_orig.has_moved # For castling/pawn state
                                sim_all_pieces_after_move.append(sim_p)

                            sim_moving_piece_in_sim_list = None
                            sim_piece_at_target_in_sim_list = None

                            for p_sim_am in sim_all_pieces_after_move:
                                if p_sim_am.row == piece_to_move.row and \
                                p_sim_am.col == piece_to_move.col and \
                                p_sim_am.piece_type == piece_to_move.piece_type and \
                                p_sim_am.color == piece_to_move.color:
                                    sim_moving_piece_in_sim_list = p_sim_am
                                if p_sim_am.row == r_target and p_sim_am.col == c_target:
                                    sim_piece_at_target_in_sim_list = p_sim_am
                            
                            if not sim_moving_piece_in_sim_list: continue

                            if sim_piece_at_target_in_sim_list and \
                                sim_piece_at_target_in_sim_list.color != sim_moving_piece_in_sim_list.color:
                                sim_all_pieces_after_move.remove(sim_piece_at_target_in_sim_list)
                            
                            sim_moving_piece_in_sim_list.row = r_target
                            sim_moving_piece_in_sim_list.col = c_target
                            
                            if not move_logic.is_king_in_check(player_color,
                                                            sim_all_pieces_after_move,
                                                            self.game.BOARD_SIZE):
                                return True # Found a legal move
        return False # No legal moves found

    def _check_for_check(self):
        """Checks if the current player's king is in check, and if it's mate or stalemate."""
        # king_to_check_color is the player whose turn it is NOW.
        king_to_check_color = self.game.current_turn
        
        if move_logic.is_king_in_check(king_to_check_color, self.game.all_piece_objects, self.game.BOARD_SIZE):
            print(f"CHECK! {king_to_check_color} king is in check.")
            if not self._has_legal_moves(king_to_check_color):
                self.game.game_state = self.game.c.GAME_OVER
                winner = self.game.BLACK if king_to_check_color == self.game.WHITE else self.game.WHITE
                self.game.game_over_message = f"CHECKMATE! {winner} wins."
                print(self.game.game_over_message)
                self.game.show_check_message_timer = 0 # Don't show "CHECK!" if it's "CHECKMATE!"
            else:
                # It's a check, but not mate. Show "CHECK!" message.
                self.game.show_check_message_timer = self.game.c.CHECK_MESSAGE_DURATION
        else:
            # Not in check, clear any lingering check message timer
            self.game.show_check_message_timer = 0
            if not self._has_legal_moves(king_to_check_color):
                self.game.game_state = self.game.c.GAME_OVER
                self.game.game_over_message = "STALEMATE! It's a draw."
                print(self.game.game_over_message)