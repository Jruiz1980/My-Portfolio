import arcade

SCREEN_WIDTH = 600
SCREEN_HEIGHT = 600
SCREEN_TITLE = "Chess"

SQUARE_SIZE = 75
BOARD_SIZE = 8

class MyGame(arcade.Window):
    def __init__(self):
        window_width = SQUARE_SIZE * BOARD_SIZE
        window_height = SQUARE_SIZE * BOARD_SIZE
        super().__init__(window_width, window_height, SCREEN_TITLE)
        arcade.set_background_color(arcade.color.BEIGE)

    def on_draw(self):
        self.clear()   
        for row in range(BOARD_SIZE):
            for col in range(BOARD_SIZE):
                left = col * SQUARE_SIZE
                right = (col + 1) * SQUARE_SIZE
                bottom = row * SQUARE_SIZE
                top = (row + 1) * SQUARE_SIZE

                if (row +col) % 2 == 0:
                    color = arcade.color.BISTRE
                else:
                    color = arcade.color.BEAVER
                
                arcade.draw_lrbt_rectangle_filled(left, right, bottom, top, color)

def main():
    game = MyGame()
    arcade.run()

if __name__ == "__main__":
    main()
