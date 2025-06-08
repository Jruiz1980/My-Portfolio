import arcade
import components.constants as c

class BoardRenderer:
    def __init__(self, square_size: int, board_size: int, margin: int):
        self.SQUARE_SIZE = square_size
        self.BOARD_SIZE = board_size
        self.MARGIN = margin
        self.board_pixel_width = self.SQUARE_SIZE * self.BOARD_SIZE
        self.board_pixel_height = self.SQUARE_SIZE * self.BOARD_SIZE

        self.bottom_labels = []
        self.top_labels = []
        self.left_labels = []
        self.right_labels = []
        self._create_labels_as_text_objects()

    def draw_board(self):
        """Draws the chessboard squares."""
        for row in range(self.BOARD_SIZE):
            for col in range(self.BOARD_SIZE):
                left = col * self.SQUARE_SIZE + self.MARGIN
                right = (col + 1) * self.SQUARE_SIZE + self.MARGIN
                bottom = row * self.SQUARE_SIZE + self.MARGIN
                top = (row + 1) * self.SQUARE_SIZE + self.MARGIN

                if (row + col) % 2 == 0:
                    color = c.PICTON_BLUE
                else:
                    color = c.BISQUE
                arcade.draw_lrbt_rectangle_filled(left, right, bottom, top, color)

    def _create_labels_as_text_objects(self):
        """Creates arcade.Text objects for all labels."""
        # Draw A-H labels below the board
        for col in range(self.BOARD_SIZE):
            label_text = chr(ord('A') + col)
            text_x = self.MARGIN + col * self.SQUARE_SIZE + self.SQUARE_SIZE // 2
            text_y = self.MARGIN // 2
            self.bottom_labels.append(arcade.Text(label_text, text_x, text_y, c.LABEL_COLOR,
                font_size=c.LABEL_FONT_SIZE, anchor_x="center", anchor_y="center"))

        # Draw A-H labels above the board
        for i in range(self.BOARD_SIZE):
            char_offset = (self.BOARD_SIZE - 1) - i
            label_text = chr(ord('A') + char_offset)
            text_x = self.MARGIN + i * self.SQUARE_SIZE + self.SQUARE_SIZE // 2
            text_y = self.MARGIN + self.board_pixel_height + self.MARGIN // 2
            self.top_labels.append(arcade.Text(label_text, text_x, text_y, c.LABEL_COLOR,
                font_size=c.LABEL_FONT_SIZE, anchor_x="center", anchor_y="center"))

        # Draw 1-8 labels to the left of the board
        for row in range(self.BOARD_SIZE):
            label_text = str(row + 1)
            text_x = self.MARGIN // 2
            text_y = self.MARGIN + row * self.SQUARE_SIZE + self.SQUARE_SIZE // 2
            self.left_labels.append(arcade.Text(label_text, text_x, text_y, c.LABEL_COLOR,
                font_size=c.LABEL_FONT_SIZE, anchor_x="center", anchor_y="center"))

        # Draw 1-8 labels to the right of the board
        for row in range(self.BOARD_SIZE):
            label_text = str(self.BOARD_SIZE - row)
            text_x = self.MARGIN + self.board_pixel_width + self.MARGIN // 2
            text_y = self.MARGIN + row * self.SQUARE_SIZE + self.SQUARE_SIZE // 2
            self.right_labels.append(arcade.Text(label_text, text_x, text_y, c.LABEL_COLOR,
                font_size=c.LABEL_FONT_SIZE, anchor_x="center", anchor_y="center"))

    def draw_labels(self):
        """Draws the algebraic notation labels around the board."""
        for label_list in [self.bottom_labels, self.top_labels, self.left_labels, self.right_labels]:
            for label in label_list:
                label.draw()

    def draw_highlighted_moves(self, coords: list[tuple[int, int]]):
        for row, col in coords:
            center_x = self.MARGIN + col * self.SQUARE_SIZE + self.SQUARE_SIZE // 2
            center_y = self.MARGIN + row * self.SQUARE_SIZE + self.SQUARE_SIZE // 2
            radius = self.SQUARE_SIZE * 0.2
            fill_color = c.HIGHLIGHT_MOVE_FILL_COLOR # Usar el nuevo verde claro
            border_color = c.BUTTON_ORANGE # Usamos el naranja para el borde
            border_width = 3 # Ancho del borde en píxeles
            arcade.draw_circle_filled(center_x, center_y, radius, fill_color) # Dibujar relleno verde
            arcade.draw_circle_outline(center_x, center_y, radius, border_color, border_width)

    def draw_selected_square_highlight(self, coord: tuple[int, int]):
        """Draws a highlight on the selected piece's square."""
        if not coord:
            return
        row, col = coord
        left = col * self.SQUARE_SIZE + self.MARGIN
        right = (col + 1) * self.SQUARE_SIZE + self.MARGIN
        bottom = row * self.SQUARE_SIZE + self.MARGIN
        top = (row + 1) * self.SQUARE_SIZE + self.MARGIN
        arcade.draw_lrbt_rectangle_filled(left, right, bottom, top, c.SELECTED_SQUARE_HIGHLIGHT_COLOR)