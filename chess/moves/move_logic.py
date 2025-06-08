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

def find_king(player_color: str, all_pieces: list[Piece]) -> Piece | None:
    """Finds the king of the specified color."""
    for piece in all_pieces:
        if isinstance(piece, King) and piece.color == player_color:
            return piece
    return None # Should not happen in a normal game

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
        if abs(new_col - piece.col) == 1 and new_row == piece.row + direction: # Moving one step diagonally forward
            if target_piece and target_piece.color != piece.color: # Must be an opponent's piece on the target square
                return True
            
    elif isinstance(piece, Rook):
        if piece.row == new_row or piece.col == new_col:
            # Check for obstructions
            if piece.row == new_row: # Horizontal move
                step = 1 if new_col > piece.col else -1
                for c_col in range(int(piece.col + step), int(new_col), int(step)):
                    if get_piece_at_square(piece.row, c_col, all_pieces):
                        return False # Path blocked
            else: # Vertical move
                step = 1 if new_row > piece.row else -1
                for r_row in range(int(piece.row + step), int(new_row), int(step)):
                    if get_piece_at_square(r_row, piece.col, all_pieces):
                        return False # Path blocked
            return True # Path is clear or it's a capture on the target square

    elif isinstance(piece, Knight):
        # Knight can jump over pieces, so no obstruction check needed for its path.
        # The initial check for same-color piece on target square is sufficient.
        row_diff = abs(new_row - piece.row)
        col_diff = abs(new_col - piece.col)
        if (row_diff == 2 and col_diff == 1) or \
        (row_diff == 1 and col_diff == 2):
            return True

    elif isinstance(piece, Bishop):
        if abs(new_row - piece.row) == abs(new_col - piece.col):
            # Check for obstructions along the diagonal
            row_step = 1 if new_row > piece.row else -1
            col_step = 1 if new_col > piece.col else -1
            current_row, current_col = piece.row + row_step, piece.col + col_step
            while int(current_row) != int(new_row): # or current_col != new_col
                if get_piece_at_square(current_row, current_col, all_pieces):
                    return False # Path blocked
                current_row += row_step
                current_col += col_step
            return True # Path is clear or it's a capture on the target square

    elif isinstance(piece, Queen):
        if piece.row == new_row or piece.col == new_col: # Horizontal or Vertical (like Rook)
            if piece.row == new_row: # Horizontal move
                step = 1 if new_col > piece.col else -1
                for c_col in range(int(piece.col + step), int(new_col), int(step)):
                    if get_piece_at_square(piece.row, c_col, all_pieces):
                        return False # Path blocked
            else: # Vertical move
                step = 1 if new_row > piece.row else -1
                for r_row in range(int(piece.row + step), int(new_row), int(step)):
                    if get_piece_at_square(r_row, piece.col, all_pieces):
                        return False # Path blocked
            return True
        elif abs(new_row - piece.row) == abs(new_col - piece.col): # Diagonal (like Bishop)
            row_step = 1 if new_row > piece.row else -1
            col_step = 1 if new_col > piece.col else -1
            current_row, current_col = int(piece.row + row_step), int(piece.col + col_step)
            while int(current_row) != int(new_row):
                if get_piece_at_square(current_row, current_col, all_pieces):
                    return False # Path blocked
                current_row += row_step
                current_col += col_step
            return True

    elif isinstance(piece, King):
        # Basic king move: one square in any direction
        # King moves only one square, so no intermediate path to check for obstruction.
        # The initial check for same-color piece on target square is sufficient.
        row_diff = abs(new_row - piece.row)
        col_diff = abs(new_col - piece.col)
        if row_diff <= 1 and col_diff <= 1:
            return True

    return False # Default to invalid if no rule matches or for unhandled pieces

def _is_square_attacked_by_pawn(pawn: Pawn, target_row: int, target_col: int) -> bool:
    """Checks if a specific square is attacked by this pawn."""
    direction = 1 if pawn.color == WHITE else -1
    # A pawn attacks the squares one step diagonally forward from its current position.
    if pawn.row + direction == target_row:
        if pawn.col + 1 == target_col or pawn.col - 1 == target_col:
            return True
    return False

def is_square_attacked(target_row: int, target_col: int, attacker_color: str, all_pieces: list[Piece], board_size: int) -> bool:
    """
    Checks if a square (target_row, target_col) is attacked by any piece of attacker_color.
    """
    for piece in all_pieces:
        if piece.color == attacker_color:
            if isinstance(piece, Pawn):
                if _is_square_attacked_by_pawn(piece, target_row, target_col):
                    return True
            else:
                # For other pieces, their standard move validity (ignoring if target is same color for attack check)
                # is_move_valid already checks if piece can reach the square, including obstructions.
                # The initial check in is_move_valid (target_piece.color == piece.color) handles not "attacking" through own piece.
                if is_move_valid(piece, target_row, target_col, all_pieces, board_size):
                    return True
    return False

def is_king_in_check(king_color: str, all_pieces: list[Piece], board_size: int) -> bool:
    """Checks if the king of the specified color is currently in check."""
    king = find_king(king_color, all_pieces)
    if not king:
        return False # Should not happen
    opponent_color = BLACK if king_color == WHITE else WHITE
    return is_square_attacked(king.row, king.col, opponent_color, all_pieces, board_size)