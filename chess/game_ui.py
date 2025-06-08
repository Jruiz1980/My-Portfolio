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
                    "width": 100, "height": 40, "text": "Play human", # Ancho se actualizará dinámicamente abajo
                    "color": c.BUTTON_BLUE, "text_color": c.BUTTON_TEXT_WHITE, "font_size": 14, "action": "pvp"},
            "pvc": {"center_x": self.window_width / 2 + 80, "center_y": self.window_height / 2 - 60,
                    "width": 100, "height": 40, "text": "Play with AI",
                    "color": c.BUTTON_ORANGE, "text_color": c.BUTTON_TEXT_BLACK, "font_size": 14, "action": "pvc"},
        }

        # Ajustar dinámicamente el ancho del botón "pvp" según su texto
        pvp_button_props = self.setup_buttons["pvp"]
        pvp_text = pvp_button_props["text"]
        pvp_font_size = pvp_button_props["font_size"]

        # Crear un objeto de texto temporal para medir su ancho.
        # La propiedad .width debería estar disponible después de crear el objeto.
        # Si text_width resulta ser None, podría ser un problema con la carga de la fuente.
        # En ese caso, especificar un font_name común como "Arial" podría ayudar:
        # font_name="Arial"
        temp_text_obj = arcade.Text(
            text=pvp_text,
            x=0,  # Posición inicial no afecta la medición del ancho
            y=0,
            color=pvp_button_props["text_color"], # Usar el color del texto del botón
            font_size=pvp_font_size,
            font_name="Arial"  # Especificar una fuente común
        )
        text_width = temp_text_obj.width

        if text_width is not None:
            horizontal_padding = 20  # Añadir 10px de padding a cada lado
            self.setup_buttons["pvp"]["width"] = text_width + horizontal_padding
        else:
            # Fallback si la medición del texto falla
            print("Advertencia: No se pudo medir el ancho del texto para el botón PvP. Usando ancho predeterminado.")
        # For PLAYING or GAME_OVER state (Reset button is below the board)
        # The board itself is MARGIN + board_pixel_height + MARGIN high.
        # Reset button y position needs to be calculated based on board height.
        # Assuming board is centered, or at least top part is fixed.
        # For simplicity, let's place it near the bottom of the window.
        # A more robust way would be to pass board_pixel_height or calculate it.
        # For now, placing it relative to window_height.
        gameplay_button_y = c.MARGIN / 2 # Place it in the bottom margin area
        if self.window_height < (c.SQUARE_SIZE * c.BOARD_SIZE + 2 * c.MARGIN + 50): # check if enough space
            gameplay_button_y = self.window_height - 30 # fallback if window too small

        button_width = 160
        button_spacing = 20

        self.gameplay_buttons = {
            "reset_board": {"center_x": self.window_width / 2 - button_width / 2 - button_spacing / 2,
                            "center_y": gameplay_button_y, "width": button_width, "height": 40,
                            "text": "Reset Board", "color": c.BUTTON_ORANGE,
                            "text_color": c.BUTTON_TEXT_BLACK, "font_size": 16, "action": "reset_board"},
            "new_game": {"center_x": self.window_width / 2 + button_width / 2 + button_spacing / 2,
                        "center_y": gameplay_button_y, "width": button_width, "height": 40,
                        "text": "New Game", "color": c.BUTTON_RED,
                        "text_color": c.BUTTON_TEXT_WHITE, "font_size": 16, "action": "new_game"},
        }

        # For PAWN_PROMOTION state
        # Position these buttons, e.g., horizontally in the middle of the screen
        promo_btn_y = self.window_height / 2
        promo_btn_width = 100
        promo_btn_height = 50
        spacing = 10
        total_width = 4 * promo_btn_width + 3 * spacing
        start_x = (self.window_width - total_width) / 2 + promo_btn_width / 2

        self.promotion_buttons = {
            "promote_queen": {"center_x": start_x, "center_y": promo_btn_y, "width": promo_btn_width, "height": promo_btn_height,
                            "text": "Queen", "color": c.BUTTON_BLUE, "text_color": c.BUTTON_TEXT_WHITE, "font_size": 16, "action": "promote_queen"},
            "promote_rook": {"center_x": start_x + promo_btn_width + spacing, "center_y": promo_btn_y, "width": promo_btn_width, "height": promo_btn_height,
                            "text": "Rook", "color": c.BUTTON_BLUE, "text_color": c.BUTTON_TEXT_WHITE, "font_size": 16, "action": "promote_rook"},
            "promote_bishop": {"center_x": start_x + 2 * (promo_btn_width + spacing), "center_y": promo_btn_y, "width": promo_btn_width, "height": promo_btn_height,
                            "text": "Bishop", "color": c.BUTTON_BLUE, "text_color": c.BUTTON_TEXT_WHITE, "font_size": 16, "action": "promote_bishop"},
            "promote_knight": {"center_x": start_x + 3 * (promo_btn_width + spacing), "center_y": promo_btn_y, "width": promo_btn_width, "height": promo_btn_height,
                            "text": "Knight", "color": c.BUTTON_BLUE, "text_color": c.BUTTON_TEXT_WHITE, "font_size": 16, "action": "promote_knight"},
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
            # Draw gameplay buttons (Reset Board, New Game)
            for button_props in self.gameplay_buttons.values():
                self._draw_button(button_props)
        elif game_state == c.PAWN_PROMOTION:
            arcade.draw_text("Promote Pawn to:", self.window_width / 2, self.window_height / 2 + 100,
                            arcade.color.BLACK, font_size=24, anchor_x="center")
            for button_props in self.promotion_buttons.values():
                self._draw_button(button_props)

    def handle_mouse_press(self, x: int, y: int, game_state: int) -> str | None:
        """Checks if a button was clicked and returns its action string, or None."""
        buttons_to_check = {}
        if game_state == c.SETUP:
            buttons_to_check = self.setup_buttons
        elif game_state == c.PLAYING or game_state == c.GAME_OVER:
            buttons_to_check = self.gameplay_buttons
        elif game_state == c.PAWN_PROMOTION:
            buttons_to_check = self.promotion_buttons

        for button_name, props in buttons_to_check.items():
            if self._is_point_in_button(x, y, props):
                return props.get("action") # Return the action string
        return None