import arcade
from components.pieces import Piece, Pawn, Rook, Knight, Bishop, Queen, King # Import from pieces.py
from moves.input_handler import InputHandler
from board_renderer import BoardRenderer # Import BoardRenderer
from game_ui import GameUI # Import GameUI
import components.constants as c # Import constants
from moves import move_logic # For algebraic notation after promotion

class MyGame(arcade.Window):
    def __init__(self):
        self.SQUARE_SIZE = c.SQUARE_SIZE
        self.BOARD_SIZE = c.BOARD_SIZE
        self.MARGIN = c.MARGIN
        self.WHITE = c.WHITE_PLAYER_COLOR_NAME
        self.BLACK = c.BLACK_PLAYER_COLOR_NAME

        self.board_pixel_width = self.SQUARE_SIZE * self.BOARD_SIZE
        self.board_pixel_height = self.SQUARE_SIZE * self.BOARD_SIZE

        window_width = self.board_pixel_width + 2 * self.MARGIN + c.HISTORY_AREA_WIDTH
        # Ensure enough height for UI elements like reset button or promotion text
        # Extra margin at bottom, ensure it's at least board + 2*margin + some UI space
        window_height = max(self.board_pixel_height + 2 * self.MARGIN + self.MARGIN, 600) # Min height
        super().__init__(window_width, window_height, c.SCREEN_TITLE)
        arcade.set_background_color(c.BACKGROUND_COLOR)

        self.game_state = c.SETUP # Start in the setup state
        
        self.all_piece_objects: list[Piece] = [] # To store Piece objects for logic
        self.piece_sprites = arcade.SpriteList() # SpriteList for drawing pieces
        self.c = c # Make constants accessible via self.c

        # Game settings (can be updated by UI)
        self.player_color = self.WHITE # Default player color
        self.game_mode = "pvp" # Default game mode ("pvp" or "pvc")
        self.current_turn = self.WHITE # White always starts
        self.promoting_pawn: Piece | None = None # Stores the pawn being promoted
        self.game_over_message: str | None = None # To store "Checkmate" or "Stalemate" message
        self.move_history: list[str] = [] # To store algebraic notation of moves
        self.show_check_message_timer: float = 0.0 # Timer for "CHECK!" display

        self._setup_pieces()

        self.input_handler = InputHandler(self)
        self.board_renderer = BoardRenderer(self.SQUARE_SIZE, self.BOARD_SIZE, self.MARGIN)
        self.game_ui = GameUI(window_width, window_height)

    def _setup_pieces(self):
        """Initializes and places all pieces on the board."""
        # Clear existing pieces and sprites before setting up new ones
        self.all_piece_objects.clear()
        self.piece_sprites.clear()
        self.current_turn = self.WHITE # Reset turn to white
        self.promoting_pawn = None # Clear any promoting pawn
        self.game_over_message = None # Clear game over message
        self.move_history.clear() # Clear move history
        self.show_check_message_timer = 0.0 # Reset check message timer

        # White pieces
        for col in range(self.BOARD_SIZE):
            p = Pawn(self.WHITE, 1, col); self.all_piece_objects.append(p); self.piece_sprites.append(p.sprite)
        r1 = Rook(self.WHITE, 0, 0); self.all_piece_objects.append(r1); self.piece_sprites.append(r1.sprite)
        r2 = Rook(self.WHITE, 0, 7); self.all_piece_objects.append(r2); self.piece_sprites.append(r2.sprite)
        n1 = Knight(self.WHITE, 0, 1); self.all_piece_objects.append(n1); self.piece_sprites.append(n1.sprite)
        n2 = Knight(self.WHITE, 0, 6); self.all_piece_objects.append(n2); self.piece_sprites.append(n2.sprite)
        b1 = Bishop(self.WHITE, 0, 2); self.all_piece_objects.append(b1); self.piece_sprites.append(b1.sprite)
        b2 = Bishop(self.WHITE, 0, 5); self.all_piece_objects.append(b2); self.piece_sprites.append(b2.sprite)
        q = Queen(self.WHITE, 0, 3); self.all_piece_objects.append(q); self.piece_sprites.append(q.sprite)
        k = King(self.WHITE, 0, 4); self.all_piece_objects.append(k); self.piece_sprites.append(k.sprite)

        # Black pieces
        for col in range(self.BOARD_SIZE):
            p = Pawn(self.BLACK, 6, col); self.all_piece_objects.append(p); self.piece_sprites.append(p.sprite)
        r1_b = Rook(self.BLACK, 7, 0); self.all_piece_objects.append(r1_b); self.piece_sprites.append(r1_b.sprite)
        r2_b = Rook(self.BLACK, 7, 7); self.all_piece_objects.append(r2_b); self.piece_sprites.append(r2_b.sprite)
        n1_b = Knight(self.BLACK, 7, 1); self.all_piece_objects.append(n1_b); self.piece_sprites.append(n1_b.sprite)
        n2_b = Knight(self.BLACK, 7, 6); self.all_piece_objects.append(n2_b); self.piece_sprites.append(n2_b.sprite)
        b1_b = Bishop(self.BLACK, 7, 2); self.all_piece_objects.append(b1_b); self.piece_sprites.append(b1_b.sprite)
        b2_b = Bishop(self.BLACK, 7, 5); self.all_piece_objects.append(b2_b); self.piece_sprites.append(b2_b.sprite)
        q_b = Queen(self.BLACK, 7, 3); self.all_piece_objects.append(q_b); self.piece_sprites.append(q_b.sprite)
        k_b = King(self.BLACK, 7, 4); self.all_piece_objects.append(k_b); self.piece_sprites.append(k_b.sprite)

    def _draw_pieces(self):
        """Draws all the pieces on the board."""
        self.piece_sprites.draw()

    def on_draw(self):
        self.clear()

        if self.game_state == c.SETUP:
            self.game_ui.draw(self.game_state)
        elif self.game_state in [c.PLAYING, c.GAME_OVER, c.PAWN_PROMOTION]:
            self.board_renderer.draw_board()
            # Labels might be drawn over by promotion UI, consider order or conditional drawing
            self.board_renderer.draw_labels()

            # Draw selected square highlight (if a piece is selected)
            if self.input_handler.selected_piece_object:
                self.board_renderer.draw_selected_square_highlight(
                    (self.input_handler.selected_piece_object.row, self.input_handler.selected_piece_object.col)
                )

            self._draw_pieces() # Keep piece drawing here or move to a PieceManager
            # Draw possible move highlights using BoardRenderer
            if self.input_handler.possible_moves_coords:
                self.board_renderer.draw_highlighted_moves(self.input_handler.possible_moves_coords)
            
            # Draw UI elements (reset button, promotion choices, etc.)
            self.game_ui.draw(self.game_state)
            # Note: If PAWN_PROMOTION, game_ui.draw will handle promotion buttons.
            # If PLAYING or GAME_OVER, it will handle reset button.

            if self.game_state == c.GAME_OVER:
                # Display game over message (Checkmate or Stalemate)
                message = self.game_over_message if self.game_over_message else "GAME OVER"
                arcade.draw_text(message,
                                self.width / 2, self.height / 2 - self.SQUARE_SIZE, # Position it clearly
                                arcade.color.DARK_RED, font_size=40, anchor_x="center", bold=True)
            
            # Draw "CHECK!" message if timer is active
            if self.show_check_message_timer > 0 and self.game_state == c.PLAYING:
                # Calculate center of the board area for the "CHECK!" message
                board_center_x = self.MARGIN + self.board_pixel_width / 2
                board_center_y = self.MARGIN + self.board_pixel_height / 2
                arcade.draw_text("CHECK!",
                                board_center_x, board_center_y,
                                arcade.color.DARK_RED, font_size=60, anchor_x="center", anchor_y="center", bold=True)

            # Draw move history on the right side
            history_start_x = self.board_pixel_width + 2 * self.MARGIN + 10 # Start X for history text
            history_start_y = self.height - self.MARGIN - 30 # Start Y from top (use self.height)
            line_height = 18
            max_history_lines = (self.height - 2 * self.MARGIN - 30) // line_height # use self.height
            
            # Display latest moves first, or implement scrolling for full history
            start_index = max(0, len(self.move_history) - max_history_lines)
            for i, move_text in enumerate(self.move_history[start_index:]):
                display_y = history_start_y - i * line_height
                turn_number = (start_index + i) // 2 + 1
                player_indicator = " " if (start_index + i) % 2 == 0 else "..." # White move vs Black move
                formatted_move = f"{turn_number}.{player_indicator} {move_text}" if (start_index + i) % 2 == 0 else f"    {move_text}"
                arcade.draw_text(formatted_move, history_start_x, display_y, arcade.color.BLACK, font_size=12)

    def on_mouse_press(self, x: int, y: int, button: int, modifiers: int):
        """Called when the user presses a mouse button."""
        clicked_button_action = self.game_ui.handle_mouse_press(x, y, self.game_state)

        if clicked_button_action:
            if self.game_state == c.SETUP and clicked_button_action == "start":
                print(f"Start button clicked! Player: {self.player_color}, Mode: {self.game_mode}")
                self.game_state = c.PLAYING
            elif clicked_button_action == "new_game": # Goes back to SETUP screen
                print("New Game button clicked!")
                self._setup_pieces() # Reset pieces
                self.input_handler.selected_piece_object = None # Deselect any piece
                self.input_handler.possible_moves_coords = []
                # self.current_turn = self.WHITE # Already handled in _setup_pieces
                # self.game_over_message = None # Already handled in _setup_pieces
                self.game_state = c.SETUP # Go back to setup
            elif clicked_button_action == "reset_board": # Resets board, stays in PLAYING
                print("Reset Board button clicked!")
                self._setup_pieces() # Reset pieces, turn, promoting_pawn
                self.input_handler.selected_piece_object = None # Deselect any piece
                self.input_handler.possible_moves_coords = []
                self.game_state = c.PLAYING # Ensure game is in PLAYING state
                # self.game_over_message = None # Already handled in _setup_pieces
                # Any "Check!" message or game over state should be cleared implicitly by _setup_pieces and state change
            elif clicked_button_action == "white_color":
                if self.game_state == c.SETUP:
                    print("Selected White")
                    self.player_color = self.WHITE
            elif clicked_button_action == "black_color":
                if self.game_state == c.SETUP:
                    print("Selected Black")
                    self.player_color = self.BLACK
            elif clicked_button_action == "pvp":
                if self.game_state == c.SETUP:
                    print("Selected PvP")
                    self.game_mode = "pvp"
            elif clicked_button_action == "pvc":
                if self.game_state == c.SETUP:
                    print("Selected PvC")
                    self.game_mode = "pvc"
            
            # Handle promotion choice
            elif self.game_state == c.PAWN_PROMOTION and self.promoting_pawn:
                new_piece_type = None
                if clicked_button_action == "promote_queen": new_piece_type = Queen
                elif clicked_button_action == "promote_rook": new_piece_type = Rook
                elif clicked_button_action == "promote_bishop": new_piece_type = Bishop
                elif clicked_button_action == "promote_knight": new_piece_type = Knight

                if new_piece_type:
                    pawn = self.promoting_pawn
                    # Remove pawn
                    if pawn in self.all_piece_objects:
                        self.all_piece_objects.remove(pawn)
                    if pawn.sprite in self.piece_sprites:
                        self.piece_sprites.remove(pawn.sprite)
                    
                    # Add new piece
                    new_piece = new_piece_type(pawn.color, pawn.row, pawn.col)
                    self.all_piece_objects.append(new_piece)
                    self.piece_sprites.append(new_piece.sprite)
                    print(f"Pawn promoted to {new_piece.piece_type}")
                    promoted_char_for_notation = move_logic.get_promoted_piece_char(new_piece.piece_type) # e.g. "Q"

                    # Algebraic notation for the promotion part
                    # The move to the promotion square was already noted by InputHandler.
                    # Here we complete it with "=Q", and check/mate status *after* new piece is on board.
                    # original_piece_info for the pawn was captured in InputHandler.
                    # We need the state of the board *before* the pawn was replaced.
                    # This is tricky as InputHandler doesn't easily pass that original board state here.
                    # For simplicity, we'll print the "=Q+#" part based on current board.
                    
                    # Update the last move in history with the promotion suffix
                    opponent_color_after_promo = self.BLACK if new_piece.color == self.WHITE else self.WHITE
                    check_after_promo_choice = move_logic.is_king_in_check(opponent_color_after_promo, self.all_piece_objects, self.BOARD_SIZE)
                    checkmate_after_promo_choice = False
                    if check_after_promo_choice:
                        if not self.input_handler._has_legal_moves(opponent_color_after_promo): # Check opponent
                            checkmate_after_promo_choice = True
                            self.game_over_message = f"CHECKMATE! {new_piece.color.upper()} wins." # Set mate message here
                            self.game_state = c.GAME_OVER # End game on mate by promotion
                        else: # Just a check, not mate
                            self.show_check_message_timer = c.CHECK_MESSAGE_DURATION

                    # This is a simplified notation for the promotion suffix.
                    # A full algebraic move would combine the pawn's move and the promotion.
                    # e.g. if InputHandler printed "e8", this would add "=Q#"
                    promo_suffix = "=" + promoted_char_for_notation if promoted_char_for_notation else ""
                    if checkmate_after_promo_choice: promo_suffix += "#"
                    elif check_after_promo_choice: promo_suffix += "+"
                    print(f"Promotion completed: {promo_suffix}")
                    
                    if self.move_history:
                        self.move_history[-1] += promo_suffix # Append to the pawn's move notation

                    self.promoting_pawn = None
                    if self.game_state != c.GAME_OVER: # If not mated by promotion
                        self.game_state = c.PLAYING
                        # Switch turn and check for check (if game not over)
                        self.current_turn = opponent_color_after_promo # It's now the opponent's turn
                        print(f"Turn: {self.current_turn}")
                        # _check_for_check here would check if the current player (whose turn it became)
                        # is now in mate/stalemate due to the board state after promotion.
                        # This is generally not needed if the promotion itself caused mate.
                        # However, if the promotion did NOT cause mate, we still need to check if the
                        # player whose turn it now is has any moves (e.g. for stalemate).
                        self.input_handler._check_for_check()

        elif self.game_state == c.PLAYING:
            # If no UI button was clicked and game is playing, handle board interaction
            self.input_handler.on_mouse_press(x, y, button, modifiers)

    def update(self, delta_time: float):
        if self.show_check_message_timer > 0:
            self.show_check_message_timer -= delta_time

def main():
    game = MyGame()
    arcade.run()

if __name__ == "__main__":
    main()
