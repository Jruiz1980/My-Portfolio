"""
Handles the logic for validating chess piece moves.
"""

from components.pieces import Piece, Pawn, Rook, Knight, Bishop, Queen, King, WHITE, BLACK

def get_piece_at_square(target_row: int, target_col: int, all_pieces: list[Piece]) -> Piece | None:
    """Checks if a piece exists at the given board coordinates."""
    for piece in all_pieces:
        if piece.row == target_row and piece.col == target_col:
            return piece
    return None

def is_move_valid(piece: Piece, new_row: int, new_col: int, all_pieces: list[Piece], board_size: int) -> bool:
    """
    Checks if a move is valid for a given piece.
    This is a placeholder and needs to be expanded for each piece type.
    """
    if not (0 <= new_row < board_size and 0 <= new_col < board_size):
        return False # Off the board

    # Basic check: cannot move to a square occupied by a piece of the same color
    target_piece = get_piece_at_square(new_row, new_col, all_pieces)
    if target_piece and target_piece.color == piece.color:
        return False

    # Add specific rules for each piece type
    if isinstance(piece, Pawn):
        # Basic pawn move: one step forward (simplistic, no capture/double step yet)
        direction = 1 if piece.color == WHITE else -1
        start_row_white = 1
        start_row_black = 6 # Assuming board_size 8, rows 0-7

        # Standard one-square move
        if new_col == piece.col and new_row == piece.row + direction:
            if not target_piece:  # Can only move forward to an empty square
                return True

        # Initial two-square move
        if piece.col == new_col: # Must be in the same column
            if piece.color == WHITE and piece.row == start_row_white and new_row == piece.row + 2 * direction:
                # Check if path is clear for white pawn's two-square move
                if not get_piece_at_square(piece.row + direction, new_col, all_pieces) and \
                   not target_piece: # Target square must also be empty
                    return True
            elif piece.color == BLACK and piece.row == start_row_black and new_row == piece.row + 2 * direction:
                # Check if path is clear for black pawn's two-square move
                if not get_piece_at_square(piece.row + direction, new_col, all_pieces) and \
                   not target_piece: # Target square must also be empty
                    return True

        # TODO: Add logic for diagonal captures
        # Example: if abs(new_col - piece.col) == 1 and new_row == piece.row + direction:
        #             if target_piece and target_piece.color != piece.color: return True
    elif isinstance(piece, Rook):
        # Basic rook move: horizontal or vertical (simplistic, no obstruction check yet)
        if piece.row == new_row or piece.col == new_col:
            # TODO: Add obstruction check (no pieces between start and end)
            return True
    elif isinstance(piece, Knight):
        row_diff = abs(new_row - piece.row)
        col_diff = abs(new_col - piece.col)
        if (row_diff == 2 and col_diff == 1) or \
        (row_diff == 1 and col_diff == 2):
            return True
    elif isinstance(piece, Bishop):
        # Basic bishop move: diagonal (simplistic, no obstruction check yet)
        if abs(new_row - piece.row) == abs(new_col - piece.col):
            # TODO: Add obstruction check
            return True
    elif isinstance(piece, Queen):
        # Basic queen move: horizontal, vertical, or diagonal (simplistic, no obstruction check yet)
        if piece.row == new_row or piece.col == new_col or \
            abs(new_row - piece.row) == abs(new_col - piece.col):
            # TODO: Add obstruction check
            return True
    elif isinstance(piece, King):
        # Basic king move: one square in any direction
        row_diff = abs(new_row - piece.row)
        col_diff = abs(new_col - piece.col)
        if row_diff <= 1 and col_diff <= 1:
            return True

    return False # Default to invalid if no rule matches or for unhandled pieces