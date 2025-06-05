import arcade
from components.pieces import Piece, Pawn, Rook, Knight, Bishop, Queen, King # Import from pieces.py
from moves.input_handler import InputHandler

SCREEN_TITLE = "Chess"

SQUARE_SIZE = 75
BOARD_SIZE = 8
MARGIN = 40
LABEL_FONT_SIZE = 14
LABEL_COLOR = arcade.color.BLACK # Define label color as a constant
WHITE = "white"
BLACK = "black"

class MyGame(arcade.Window):
    def __init__(self):
        board_pixel_width = SQUARE_SIZE * BOARD_SIZE
        board_pixel_height = SQUARE_SIZE * BOARD_SIZE

        window_width = board_pixel_width + 2 * MARGIN
        window_height = board_pixel_height + 2 * MARGIN
        super().__init__(window_width, window_height, SCREEN_TITLE)
        arcade.set_background_color(arcade.color.BEIGE)

        self.board_pixel_width = board_pixel_width
        self.board_pixel_height = board_pixel_height

        self.all_piece_objects: list[Piece] = [] # To store Piece objects for logic
        self.piece_sprites = arcade.SpriteList()
        self._setup_pieces()

    def _setup_pieces(self):
        """Initializes and places all pieces on the board."""
        # White pieces
        for col in range(BOARD_SIZE):
            p = Pawn(WHITE, 1, col); self.all_piece_objects.append(p); self.piece_sprites.append(p.sprite)
        r1 = Rook(WHITE, 0, 0); self.all_piece_objects.append(r1); self.piece_sprites.append(r1.sprite)
        r2 = Rook(WHITE, 0, 7); self.all_piece_objects.append(r2); self.piece_sprites.append(r2.sprite)
        n1 = Knight(WHITE, 0, 1); self.all_piece_objects.append(n1); self.piece_sprites.append(n1.sprite)
        n2 = Knight(WHITE, 0, 6); self.all_piece_objects.append(n2); self.piece_sprites.append(n2.sprite)
        b1 = Bishop(WHITE, 0, 2); self.all_piece_objects.append(b1); self.piece_sprites.append(b1.sprite)
        b2 = Bishop(WHITE, 0, 5); self.all_piece_objects.append(b2); self.piece_sprites.append(b2.sprite)
        q = Queen(WHITE, 0, 3); self.all_piece_objects.append(q); self.piece_sprites.append(q.sprite)
        k = King(WHITE, 0, 4); self.all_piece_objects.append(k); self.piece_sprites.append(k.sprite)

        # Black pieces
        for col in range(BOARD_SIZE):
            p = Pawn(BLACK, 6, col); self.all_piece_objects.append(p); self.piece_sprites.append(p.sprite)
        r1_b = Rook(BLACK, 7, 0); self.all_piece_objects.append(r1_b); self.piece_sprites.append(r1_b.sprite)
        r2_b = Rook(BLACK, 7, 7); self.all_piece_objects.append(r2_b); self.piece_sprites.append(r2_b.sprite)
        n1_b = Knight(BLACK, 7, 1); self.all_piece_objects.append(n1_b); self.piece_sprites.append(n1_b.sprite)
        n2_b = Knight(BLACK, 7, 6); self.all_piece_objects.append(n2_b); self.piece_sprites.append(n2_b.sprite)
        b1_b = Bishop(BLACK, 7, 2); self.all_piece_objects.append(b1_b); self.piece_sprites.append(b1_b.sprite)
        b2_b = Bishop(BLACK, 7, 5); self.all_piece_objects.append(b2_b); self.piece_sprites.append(b2_b.sprite)
        q_b = Queen(BLACK, 7, 3); self.all_piece_objects.append(q_b); self.piece_sprites.append(q_b.sprite)
        k_b = King(BLACK, 7, 4); self.all_piece_objects.append(k_b); self.piece_sprites.append(k_b.sprite)

    def _draw_pieces(self):
        """Draws all the pieces on the board."""

        self.piece_sprites.draw()

    def _draw_board(self):
        """Draws the chessboard squares."""
        for row in range(BOARD_SIZE):
            for col in range(BOARD_SIZE):
                left = col * SQUARE_SIZE + MARGIN
                right = (col + 1) * SQUARE_SIZE + MARGIN
                bottom = row * SQUARE_SIZE + MARGIN
                top = (row + 1) * SQUARE_SIZE + MARGIN

                if (row + col) % 2 == 0:
                    color = arcade.color.PICTON_BLUE
                else:
                    color = arcade.color.BISQUE
                arcade.draw_lrbt_rectangle_filled(left, right, bottom, top, color)

    def _draw_labels(self):
        """Draws the algebraic notation labels around the board."""
        # Draw A-H labels below the board
        for col in range(BOARD_SIZE):
            label_text = chr(ord('A') + col)
            text_x = MARGIN + col * SQUARE_SIZE + SQUARE_SIZE // 2
            text_y = MARGIN // 2
            arcade.draw_text(label_text, text_x, text_y, LABEL_COLOR,
                            font_size=LABEL_FONT_SIZE, anchor_x="center", anchor_y="center")

        # Draw A-H labels above the board
        for i in range(BOARD_SIZE): # i is the column index from left (0) to right (7)
            char_offset = (BOARD_SIZE - 1) - i
            label_text = chr(ord('A') + char_offset)
            text_x = MARGIN + i * SQUARE_SIZE + SQUARE_SIZE // 2 # Position based on i
            text_y = MARGIN + self.board_pixel_height + MARGIN // 2
            arcade.draw_text(label_text, text_x, text_y, LABEL_COLOR,
                            font_size=LABEL_FONT_SIZE, anchor_x="center", anchor_y="center")

        # Draw 1-8 labels to the left of the board
        for row in range(BOARD_SIZE):
            label_text = str(row + 1)
            text_x = MARGIN // 2
            text_y = MARGIN + row * SQUARE_SIZE + SQUARE_SIZE // 2
            arcade.draw_text(label_text, text_x, text_y, LABEL_COLOR,
                            font_size=LABEL_FONT_SIZE, anchor_x="center", anchor_y="center")

        # Draw 1-8 labels to the right of the board
        for row in range(BOARD_SIZE):
            # To display 8 (bottom) to 1 (top)
            label_text = str(BOARD_SIZE - row)
            text_x = MARGIN + self.board_pixel_width + MARGIN // 2
            text_y = MARGIN + row * SQUARE_SIZE + SQUARE_SIZE // 2
            arcade.draw_text(label_text, text_x, text_y, LABEL_COLOR,
                            font_size=LABEL_FONT_SIZE, anchor_x="center", anchor_y="center")

    def on_draw(self):
        self.clear()
        self._draw_board()
        self._draw_labels()
        self._draw_pieces()

    def on_mouse_press(self, x: int, y: int, button: int, modifiers: int):
        """Called when the user presses a mouse button."""
        self.input_handler.on_mouse_press(x, y, button, modifiers)


def main():
    game = MyGame()
    arcade.run()

if __name__ == "__main__":
    main()
