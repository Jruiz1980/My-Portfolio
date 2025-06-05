# c:\Users\hualc\OneDrive-BYU-Idaho\Documents\Portfolio\My-Portfolio\chess\constants.py
import arcade

# Game States
SETUP = 0
PLAYING = 1
GAME_OVER = 2

# Board and UI Dimensions
SQUARE_SIZE = 75
BOARD_SIZE = 8
MARGIN = 40
LABEL_FONT_SIZE = 14

# Colors
LABEL_COLOR = arcade.color.BLACK
WHITE_PLAYER_COLOR_NAME = "white" # Renamed to avoid conflict with arcade.color.WHITE
BLACK_PLAYER_COLOR_NAME = "black" # Renamed to avoid conflict with arcade.color.BLACK
BACKGROUND_COLOR = arcade.color.BEIGE
PICTON_BLUE = arcade.color.PICTON_BLUE
BISQUE = arcade.color.BISQUE
BUTTON_GREEN = arcade.color.GREEN
BUTTON_RED = arcade.color.RED
BUTTON_TEXT_BLACK = arcade.color.BLACK
BUTTON_TEXT_WHITE = arcade.color.WHITE
BUTTON_BLUE = arcade.color.BLUE
BUTTON_ORANGE = arcade.color.ORANGE
HIGHLIGHT_YELLOW_TRANSPARENT = (arcade.color.YELLOW[0], arcade.color.YELLOW[1], arcade.color.YELLOW[2], 100) # (R, G, B, Alpha)


# Screen
SCREEN_TITLE = "Chess"

# Piece Types (if you want to centralize these strings too, though they are often tied to Piece classes)
# PAWN = "pawn"
# ROOK = "rook"
# etc.

# Button Properties (could also be a candidate for moving, or kept in UI specific module)
# This is just an example if you wanted to move more complex structures
# BUTTON_FONT_SIZE_LARGE = 16
# BUTTON_FONT_SIZE_SMALL = 14
