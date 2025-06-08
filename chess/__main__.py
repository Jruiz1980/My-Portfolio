import arcade
from components.pieces import Piece, Pawn, Rook, Knight, Bishop, Queen, King # Import from pieces.py
from moves.input_handler import InputHandler
from board_renderer import BoardRenderer # Import BoardRenderer
from game_ui import GameUI # Import GameUI
import components.constants as c # Import constants

class MyGame(arcade.Window):
    def __init__(self):
        self.SQUARE_SIZE = c.SQUARE_SIZE
        self.BOARD_SIZE = c.BOARD_SIZE
        self.MARGIN = c.MARGIN
        self.WHITE = c.WHITE_PLAYER_COLOR_NAME
        self.BLACK = c.BLACK_PLAYER_COLOR_NAME

        self.board_pixel_width = self.SQUARE_SIZE * self.BOARD_SIZE
        self.board_pixel_height = self.SQUARE_SIZE * self.BOARD_SIZE

        window_width = self.board_pixel_width + 2 * self.MARGIN
        # Ensure enough height for UI elements like reset button or promotion text
        window_height = self.board_pixel_height + 2 * self.MARGIN + self.MARGIN # Extra margin at bottom
        super().__init__(window_width, window_height, c.SCREEN_TITLE)
        arcade.set_background_color(c.BACKGROUND_COLOR)

        self.game_state = c.SETUP # Start in the setup state
        
        self.all_piece_objects: list[Piece] = [] # To store Piece objects for logic
        self.piece_sprites = arcade.SpriteList() # SpriteList for drawing pieces
        self.c = c # Make constants accessible via self.c
        self._setup_pieces()

        self.input_handler = InputHandler(self)
        self.board_renderer = BoardRenderer(self.SQUARE_SIZE, self.BOARD_SIZE, self.MARGIN)
        self.game_ui = GameUI(window_width, window_height)

        # Game settings (can be updated by UI)
        self.player_color = self.WHITE # Default player color
        self.game_mode = "pvp" # Default game mode ("pvp" or "pvc")
        self.current_turn = self.WHITE # White always starts
        self.promoting_pawn: Piece | None = None # Stores the pawn being promoted


    def _setup_pieces(self):
        """Initializes and places all pieces on the board."""
        # Clear existing pieces and sprites before setting up new ones
        self.all_piece_objects.clear()
        self.piece_sprites.clear()
        self.current_turn = self.WHITE # Reset turn to white
        self.promoting_pawn = None # Clear any promoting pawn

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
                # Example: Display game over message
                arcade.draw_text("GAME OVER", self.width / 2, self.height / 2 - 50,
                                 arcade.color.RED, font_size=40, anchor_x="center")

    def on_mouse_press(self, x: int, y: int, button: int, modifiers: int):
        """Called when the user presses a mouse button."""
        clicked_button_action = self.game_ui.handle_mouse_press(x, y, self.game_state)

        if clicked_button_action:
            if self.game_state == c.SETUP and clicked_button_action == "start":
                print(f"Start button clicked! Player: {self.player_color}, Mode: {self.game_mode}")
                self.game_state = c.PLAYING
            elif clicked_button_action == "reset": # Reset can be clicked in PLAYING or GAME_OVER
                print("Reset button clicked!")
                self._setup_pieces() # Reset pieces
                self.input_handler.selected_piece_object = None # Deselect any piece
                self.input_handler.possible_moves_coords = []
                # self.current_turn = self.WHITE # Already handled in _setup_pieces
                self.game_state = c.SETUP # Go back to setup
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

                    self.promoting_pawn = None
                    self.game_state = c.PLAYING
                    
                    # Switch turn and check for check
                    self.current_turn = self.BLACK if self.current_turn == self.WHITE else self.WHITE
                    print(f"Turn: {self.current_turn}")
                    self.input_handler._check_for_check()

        elif self.game_state == c.PLAYING:
            # If no UI button was clicked and game is playing, handle board interaction
            self.input_handler.on_mouse_press(x, y, button, modifiers)

def main():
    game = MyGame()
    arcade.run()

if __name__ == "__main__":
    main()
