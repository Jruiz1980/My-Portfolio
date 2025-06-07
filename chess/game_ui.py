import arcade
import components.constants as c

class GameUI:
    def __init__(self, window_width: int, window_height: int):
        self.window_width = window_width
        self.window_height = window_height
        self._setup_ui_buttons()

    def _setup_ui_buttons(self):
        """Initializes properties for UI buttons."""
        # For SETUP state
        self.setup_buttons = {
            "start": {"center_x": self.window_width / 2, "center_y": self.window_height / 2 + 100,
                        "width": 200, "height": 50, "text": "Start Game",
                        "color": c.BUTTON_GREEN, "text_color": c.BUTTON_TEXT_BLACK, "font_size": 20, "action": "start"},
            "white_color": {"center_x": self.window_width / 2 - 80, "center_y": self.window_height / 2,
                            "width": 120, "height": 40, "text": "Play as White",
                            "color": arcade.color.WHITE_SMOKE, "text_color": c.BUTTON_TEXT_BLACK, "font_size": 14, "action": "white_color"},
            "black_color": {"center_x": self.window_width / 2 + 80, "center_y": self.window_height / 2,
                            "width": 120, "height": 40, "text": "Play as Black",
                            "color": arcade.color.DARK_GRAY, "text_color": c.BUTTON_TEXT_WHITE, "font_size": 14, "action": "black_color"},
            "pvp": {"center_x": self.window_width / 2 - 80, "center_y": self.window_height / 2 - 60,
                    "width": 100, "height": 40, "text": "PvP",
                    "color": c.BUTTON_BLUE, "text_color": c.BUTTON_TEXT_WHITE, "font_size": 14, "action": "pvp"},
            "pvc": {"center_x": self.window_width / 2 + 80, "center_y": self.window_height / 2 - 60,
                    "width": 100, "height": 40, "text": "PvC",
                    "color": c.BUTTON_ORANGE, "text_color": c.BUTTON_TEXT_BLACK, "font_size": 14, "action": "pvc"},
        }

        # For PLAYING or GAME_OVER state (Reset button is below the board)
        # The board itself is MARGIN + board_pixel_height + MARGIN high.
        # Reset button y position needs to be calculated based on board height.
        # Assuming board is centered, or at least top part is fixed.
        # For simplicity, let's place it near the bottom of the window.
        # A more robust way would be to pass board_pixel_height or calculate it.
        # For now, placing it relative to window_height.
        reset_button_y = c.MARGIN / 2 # Place it in the bottom margin area
        if self.window_height < (c.SQUARE_SIZE * c.BOARD_SIZE + 2 * c.MARGIN + 50): # check if enough space
            reset_button_y = self.window_height - 30 # fallback if window too small

        self.gameplay_buttons = {
            "reset": {"center_x": self.window_width / 2, "center_y": reset_button_y,
                        "width": 150, "height": 40, "text": "Reset Game",
                        "color": c.BUTTON_RED, "text_color": c.BUTTON_TEXT_WHITE, "font_size": 16, "action": "reset"},
        }


    def _draw_button(self, button_props):
        """Draws a button based on its properties."""
        # Calculate left, right, bottom, top from center_x, center_y, width, height
        half_width = button_props["width"] / 2
        half_height = button_props["height"] / 2
        left = button_props["center_x"] - half_width
        right = button_props["center_x"] + half_width
        bottom = button_props["center_y"] - half_height
        top = button_props["center_y"] + half_height

        arcade.draw_lrbt_rectangle_filled(left, right, bottom, top, button_props["color"])
        arcade.draw_text(button_props["text"], button_props["center_x"], button_props["center_y"],
                        button_props["text_color"], font_size=button_props["font_size"],
                        anchor_x="center", anchor_y="center")

    def _is_point_in_button(self, x, y, button_props):
        """Checks if a point (x, y) is inside a button."""
        return (button_props["center_x"] - button_props["width"] / 2 <= x <= button_props["center_x"] + button_props["width"] / 2 and
                button_props["center_y"] - button_props["height"] / 2 <= y <= button_props["center_y"] + button_props["height"] / 2)

    def draw(self, game_state: int):
        """Draws UI elements based on the game state."""
        if game_state == c.SETUP:
            arcade.draw_text("Game Setup", self.window_width / 2, self.window_height / 2 + 180,
                            arcade.color.BLACK, font_size=30, anchor_x="center")
            for button_props in self.setup_buttons.values():
                self._draw_button(button_props)
        elif game_state == c.PLAYING or game_state == c.GAME_OVER:
            # Only draw reset button during play or game over
            self._draw_button(self.gameplay_buttons["reset"])

    def handle_mouse_press(self, x: int, y: int, game_state: int) -> str | None:
        """Checks if a button was clicked and returns its action string, or None."""
        buttons_to_check = {}
        if game_state == c.SETUP:
            buttons_to_check = self.setup_buttons
        elif game_state == c.PLAYING or game_state == c.GAME_OVER:
            buttons_to_check = self.gameplay_buttons

        for button_name, props in buttons_to_check.items():
            if self._is_point_in_button(x, y, props):
                return props.get("action") # Return the action string
        return None