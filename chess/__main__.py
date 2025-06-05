import arcade
from components.pieces import Piece, Pawn, Rook, Knight, Bishop, Queen, King # Import from pieces.py

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

        self.pieces = arcade.SpriteList()
        self._setup_pieces()

    def _setup_pieces(self):
        """Initializes and places all pieces on the board."""
        # White pieces
        for col in range(BOARD_SIZE):
            self.pieces.append(Pawn(WHITE, 1, col).sprite)
        self.pieces.append(Rook(WHITE, 0, 0).sprite)
        self.pieces.append(Rook(WHITE, 0, 7).sprite)
        self.pieces.append(Knight(WHITE, 0, 1).sprite)
        self.pieces.append(Knight(WHITE, 0, 6).sprite)
        self.pieces.append(Bishop(WHITE, 0, 2).sprite)
        self.pieces.append(Bishop(WHITE, 0, 5).sprite)
        self.pieces.append(Queen(WHITE, 0, 3).sprite)
        self.pieces.append(King(WHITE, 0, 4).sprite)

        # Black pieces
        for col in range(BOARD_SIZE):
            self.pieces.append(Pawn(BLACK, 6, col).sprite)
        self.pieces.append(Rook(BLACK, 7, 0).sprite)
        self.pieces.append(Rook(BLACK, 7, 7).sprite)
        self.pieces.append(Knight(BLACK, 7, 1).sprite)
        self.pieces.append(Knight(BLACK, 7, 6).sprite)
        self.pieces.append(Bishop(BLACK, 7, 2).sprite)
        self.pieces.append(Bishop(BLACK, 7, 5).sprite)
        self.pieces.append(Queen(BLACK, 7, 3).sprite)
        self.pieces.append(King(BLACK, 7, 4).sprite)

    def _draw_pieces(self):
        """Draws all the pieces on the board."""
        for piece in self.pieces:
            # The piece.draw() method uses constants (SQUARE_SIZE, MARGIN)
            # defined in pieces.py. Ensure these are consistent or pass
            # them as arguments if they can vary.
            piece.draw()
        self.pieces.draw()

    def _draw_board(self):
        """Draws the chessboard squares."""
        for row in range(BOARD_SIZE):
            for col in range(BOARD_SIZE):
                left = col * SQUARE_SIZE + MARGIN
                right = (col + 1) * SQUARE_SIZE + MARGIN
                bottom = row * SQUARE_SIZE + MARGIN
                top = (row + 1) * SQUARE_SIZE + MARGIN

                if (row + col) % 2 == 0:
                    color = arcade.color.BISTRE
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
        for col in range(BOARD_SIZE):
            label_text = chr(ord('A') + col)
            text_x = MARGIN + col * SQUARE_SIZE + SQUARE_SIZE // 2
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
            label_text = str(row + 1)
            text_x = MARGIN + self.board_pixel_width + MARGIN // 2
            text_y = MARGIN + row * SQUARE_SIZE + SQUARE_SIZE // 2
            arcade.draw_text(label_text, text_x, text_y, LABEL_COLOR,
                            font_size=LABEL_FONT_SIZE, anchor_x="center", anchor_y="center")

    def on_draw(self):
        self.clear()
        self._draw_board()
        self._draw_labels()
        self._draw_pieces()


def main():
    game = MyGame()
    arcade.run()

if __name__ == "__main__":
    main()
