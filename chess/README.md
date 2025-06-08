# Python Arcade Chess

A simple chess game implemented in Python using the Arcade library.

## Video Demostration

[Chess game](https://youtu.be/rBnnk67N0Lw)

## Description

This project is an implementation of a chess game with a graphical interface. It allows players to play against each other (PvP) or against a basic artificial intelligence (PvAI). The game includes most standard chess rules, such as pawn promotion, check and checkmate detection, and displays moves in algebraic notation.

## Features

- Graphical chessboard with pieces.
- Modos de juego:
  - Player vs. Player (PvP)
  - Player vs. AI (PvAI - the AI makes random valid moves)
- Color selection (play as White or Black).
- Highlighting of the selected piece and its possible moves.
- Movement logic for all standard chess pieces.
- Check detection.
- Checkmate and stalemate detection.
- Pawn promotion (player can choose Queen, Rook, Bishop, or Knight).
- Move history in short algebraic notation displayed on screen.
- Temporary visual "CHECK!" message when a check occurs.
- Buttons to reset the board or start a new game.

## How to Run

1. Ensure you have Python installed (version 3.9 or higher recommended).
2. Install the Arcade library:

    ```bash
    pip install arcade
    ```

3. Navigate to the project's root directory (`chess`).
4. Run the game:

    ```bash
    python __main__.py
    ```

## Dependencies

- [Python 3](https://www.python.org/)
- [Pyglet](http://www.pyglet.org/)
- [Pillow](https://pillow.readthedocs.io/en/stable/)
- [Arcade](https://arcade.academy/)
