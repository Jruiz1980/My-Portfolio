import arcade
from components.pieces import Piece, Pawn, Rook, Knight, Bishop, Queen, King # Import from pieces.py
from moves.input_handler import InputHandler

class MyGame(arcade.Window):
    def __init__(self):
        self.SQUARE_SIZE = 75
        self.BOARD_SIZE = 8
        self.MARGIN = 40
        self.LABEL_FONT_SIZE = 14
        self.LABEL_COLOR = arcade.color.BLACK
        self.WHITE = "white"
        self.BLACK = "black"
        self.SCREEN_TITLE = "Chess"

        self.board_pixel_width = self.SQUARE_SIZE * self.BOARD_SIZE
        self.board_pixel_height = self.SQUARE_SIZE * self.BOARD_SIZE

        window_width = self.board_pixel_width + 2 * self.MARGIN
        window_height = self.board_pixel_height + 2 * self.MARGIN
        super().__init__(window_width, window_height, self.SCREEN_TITLE)
        arcade.set_background_color(arcade.color.BEIGE)

        self.board_pixel_width = self.board_pixel_width
        self.board_pixel_height = self.board_pixel_height

        self.all_piece_objects: list[Piece] = [] # To store Piece objects for logic
        self.piece_sprites = arcade.SpriteList()
        self._setup_pieces()

        self.input_handler = InputHandler(self)

        # Create Text objects for labels once
        self.bottom_labels = []
        self.top_labels = []
        self.left_labels = []
        self.right_labels = []
        self._create_labels_as_text_objects()


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

    def _draw_board(self):
        """Draws the chessboard squares."""
        for row in range(self.BOARD_SIZE):
            for col in range(self.BOARD_SIZE):
                left = col * self.SQUARE_SIZE + self.MARGIN
                right = (col + 1) * self.SQUARE_SIZE + self.MARGIN
                bottom = row * self.SQUARE_SIZE + self.MARGIN
                top = (row + 1) * self.SQUARE_SIZE + self.MARGIN


                if (row + col) % 2 == 0:
                    color = arcade.color.PICTON_BLUE
                else:
                    color = arcade.color.BISQUE
                arcade.draw_lrbt_rectangle_filled(left, right, bottom, top, color)

    def _create_labels_as_text_objects(self):
        """Creates arcade.Text objects for all labels."""
        # Draw A-H labels below the board
        for col in range(self.BOARD_SIZE):
            label_text = chr(ord('A') + col)
            text_x = self.MARGIN + col * self.SQUARE_SIZE + self.SQUARE_SIZE // 2
            text_y = self.MARGIN // 2
            self.bottom_labels.append(arcade.Text(label_text, text_x, text_y, self.LABEL_COLOR,
                font_size=self.LABEL_FONT_SIZE, anchor_x="center", anchor_y="center"))

        # Draw A-H labels above the board
        for i in range(self.BOARD_SIZE): # i is the column index from left (0) to right (7)
            char_offset = (self.BOARD_SIZE - 1) - i
            label_text = chr(ord('A') + char_offset)
            text_x = self.MARGIN + i * self.SQUARE_SIZE + self.SQUARE_SIZE // 2 # Position based on i
            text_y = self.MARGIN + self.board_pixel_height + self.MARGIN // 2
            self.top_labels.append(arcade.Text(label_text, text_x, text_y, self.LABEL_COLOR,
                font_size=self.LABEL_FONT_SIZE, anchor_x="center", anchor_y="center"))

        # Draw 1-8 labels to the left of the board
        for row in range(self.BOARD_SIZE):
            label_text = str(row + 1)
            text_x = self.MARGIN // 2
            text_y = self.MARGIN + row * self.SQUARE_SIZE + self.SQUARE_SIZE // 2
            self.left_labels.append(arcade.Text(label_text, text_x, text_y, self.LABEL_COLOR,
                font_size=self.LABEL_FONT_SIZE, anchor_x="center", anchor_y="center"))

        # Draw 1-8 labels to the right of the board
        for row in range(self.BOARD_SIZE):
            # To display 8 (bottom) to 1 (top)
            label_text = str(self.BOARD_SIZE - row)
            text_x = self.MARGIN + self.board_pixel_width + self.MARGIN // 2
            text_y = self.MARGIN + row * self.SQUARE_SIZE + self.SQUARE_SIZE // 2
            self.right_labels.append(arcade.Text(label_text, text_x, text_y, self.LABEL_COLOR,
                font_size=self.LABEL_FONT_SIZE, anchor_x="center", anchor_y="center"))

    def _draw_labels(self):
        """Draws the algebraic notation labels around the board."""
        for label in self.bottom_labels:
            label.draw()
        for label in self.top_labels:
            label.draw()
        for label in self.left_labels:
            label.draw()
        for label in self.right_labels:
            label.draw()

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
