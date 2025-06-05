import arcade
import os

SQUARE_SIZE = 75  # Assuming this is consistent with your main game file
MARGIN = 40
PIECE_SCALE = 0.8

WHITE = "white"
BLACK = "black"

# Define the path to your assets directory
ASSET_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "image")

# Helper to get image path
def get_image_path(piece_type: str, color: str) -> str:
    prefix = "w_" if color == WHITE else "b_"
    return os.path.join(ASSET_PATH, f"{prefix}{piece_type}.png")

class Piece:
    def __init__(self, piece_type: str, color: str, row: int, col: int):
        self.piece_type = piece_type
        self.color = color
        self.row = row
        self.col = col

        image_path = get_image_path(self.piece_type, self.color)
        self.sprite = arcade.Sprite(image_path, PIECE_SCALE)
        self.update_sprite_position()
    
    def update_sprite_position(self):
        self.sprite.center_x = MARGIN + self.col * SQUARE_SIZE + SQUARE_SIZE // 2
        self.sprite.center_y = MARGIN + self.row * SQUARE_SIZE + SQUARE_SIZE // 2


    def draw(self):
        self.sprite.draw()


class Pawn(Piece):
    def __init__(self, color: str, row: int, col: int):
        super().__init__("pawn", color, row, col)


class Rook(Piece):
    def __init__(self, color: str, row: int, col: int):
        super().__init__("rook", color, row, col)

class Knight(Piece):
    def __init__(self, color: str, row: int, col: int):
        super().__init__("knight", color, row, col)

class Bishop(Piece):
    def __init__(self, color: str, row: int, col: int):
        super().__init__("bishop", color, row, col) 

class Queen(Piece):
    def __init__(self, color: str, row: int, col: int):
        super().__init__("queen", color, row, col)

class King(Piece):
    def __init__(self, color: str, row: int, col: int):
        super().__init__("king", color, row, col)   
