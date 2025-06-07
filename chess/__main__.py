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
        window_height = self.board_pixel_height + 2 * self.MARGIN
        super().__init__(window_width, window_height, c.SCREEN_TITLE)
        arcade.set_background_color(c.BACKGROUND_COLOR)

        self.game_state = c.SETUP # Start in the setup state
        
        self.all_piece_objects: list[Piece] = [] # To store Piece objects for logic
        self.piece_sprites = arcade.SpriteList() # SpriteList for drawing pieces
        self._setup_pieces()

        self.input_handler = InputHandler(self)
        self.board_renderer = BoardRenderer(self.SQUARE_SIZE, self.BOARD_SIZE, self.MARGIN)
        self.game_ui = GameUI(window_width, window_height)

        # Game settings (can be updated by UI)
        self.player_color = self.WHITE # Default player color
        self.game_mode = "pvp" # Default game mode ("pvp" or "pvc")


    def _setup_pieces(self):
        """Initializes and places all pieces on the board."""
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
            # Draw setup UI elements using GameUI
            self.game_ui.draw(self.game_state)
        elif self.game_state == c.PLAYING or self.game_state == c.GAME_OVER:
            self.board_renderer.draw_board()
            self.board_renderer.draw_labels()
            self._draw_pieces() # Keep piece drawing here or move to a PieceManager
            
            # Draw possible move highlights using BoardRenderer
            if self.input_handler.possible_moves_coords:
                self.board_renderer.draw_highlighted_moves(self.input_handler.possible_moves_coords)
            
            # Draw reset button and other relevant UI using GameUI
            self.game_ui.draw(self.game_state)

            if self.game_state == c.GAME_OVER:
                # Example: Display game over message
                arcade.draw_text("GAME OVER", self.width / 2, self.height / 2 - 50,
                                 arcade.color.RED, font_size=40, anchor_x="center")

    def on_mouse_press(self, x: int, y: int, button: int, modifiers: int):
        """Called when the user presses a mouse button."""
        clicked_button_action = self.game_ui.handle_mouse_press(x, y, self.game_state)

        if clicked_button_action:
            if clicked_button_action == "start":
                print(f"Start button clicked! Player: {self.player_color}, Mode: {self.game_mode}")
                self.game_state = c.PLAYING
            elif clicked_button_action == "reset":
                print("Reset button clicked!")
                self._setup_pieces() # Reset pieces
                self.input_handler.selected_piece_object = None # Deselect any piece
                self.input_handler.possible_moves_coords = []
                self.game_state = c.SETUP # Go back to setup
            elif clicked_button_action == "white_color":
                print("Selected White")
                self.player_color = self.WHITE
            elif clicked_button_action == "black_color":
                print("Selected Black")
                self.player_color = self.BLACK
            elif clicked_button_action == "pvp":
                print("Selected PvP")
                self.game_mode = "pvp"
            elif clicked_button_action == "pvc":
                print("Selected PvC")
                self.game_mode = "pvc"
            # Add more button actions as needed

        elif self.game_state == c.PLAYING:
            # If no UI button was clicked and game is playing, handle board interaction
            self.input_handler.on_mouse_press(x, y, button, modifiers)

        # Potentially, if game_state is GAME_OVER and a click occurs not on reset,
        # you might want to transition to SETUP or show a main menu.
        # For now, only reset is handled in GAME_OVER via game_ui.


def main():
    game = MyGame()
    arcade.run()

if __name__ == "__main__":
    main()
