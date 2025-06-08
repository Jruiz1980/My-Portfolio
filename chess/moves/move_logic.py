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

def coords_to_algebraic(row: int, col: int) -> str:
    """Converts 0-indexed board coordinates to algebraic notation (e.g., (0,0) -> "a1")."""
    file = chr(ord('a') + col)
    rank = str(row + 1) # Assuming row 0 is rank '1'
    return f"{file}{rank}"

def get_piece_algebraic_prefix(piece_type: str) -> str:
    """Gets the algebraic notation prefix for a piece type (empty for pawn)."""
    if piece_type == "pawn": return ""
    if piece_type == "knight": return "N"
    if piece_type == "bishop": return "B"
    if piece_type == "rook": return "R"
    if piece_type == "queen": return "Q"
    if piece_type == "king": return "K"
    return "?" # Should not happen for valid piece types

def get_promoted_piece_char(piece_type_name: str | None) -> str | None:
    """Converts promoted piece type name (e.g., 'Queen') to its algebraic character (e.g., 'Q')."""
    if not piece_type_name:
        return None
    # Assuming piece_type_name matches the class name like 'Queen', 'Rook'
    if piece_type_name == "Queen": return "Q"
    if piece_type_name == "Rook": return "R"
    if piece_type_name == "Bishop": return "B"
    if piece_type_name == "Knight": return "N"
    return None

def format_move_to_algebraic(
    all_pieces_before_move: list[Piece], # Board state *before* this move
    board_size: int,
    moved_piece_original_row: int,
    moved_piece_original_col: int,
    moved_piece_type: str,
    moved_piece_color: str,
    dest_row: int,
    dest_col: int,
    was_capture: bool,
    promoted_to_char: str | None, # Single character like "Q", "N"
    is_check_after_move: bool,
    is_checkmate_after_move: bool,
    # TODO: Add is_castling_kingside, is_castling_queenside flags
) -> str:
    """
    Formats a move into short algebraic notation.
    Note: Disambiguation logic is complex and is simplified here.
    Castling notation (O-O, O-O-O) is not yet implemented.
    """
    notation_parts = []
    is_pawn = (moved_piece_type == "pawn")

    # 1. Piece Prefix (or pawn capture file)
    if is_pawn:
        if was_capture:
            notation_parts.append(chr(ord('a') + moved_piece_original_col)) # e.g., "e" for exd5
    else:
        notation_parts.append(get_piece_algebraic_prefix(moved_piece_type))

    # 2. Disambiguation (Simplified - TODO: Implement full disambiguation)
    # Full disambiguation requires checking if other identical pieces could also move to dest_square
    # from all_pieces_before_move, and then adding file, rank, or both from the original square.
    # Example: If two Knights can go to f3, it becomes Ngf3 or Ndf3.
    # For now, this is omitted for brevity in this initial implementation.

    # 3. Capture Indication
    if was_capture:
        notation_parts.append("x")

    # 4. Destination Square
    notation_parts.append(coords_to_algebraic(dest_row, dest_col))

    # 5. Pawn Promotion
    if promoted_to_char:
        notation_parts.append("=" + promoted_to_char)

    # 6. Check/Checkmate Suffix
    if is_checkmate_after_move:
        notation_parts.append("#")
    elif is_check_after_move:
        notation_parts.append("+")

    # Handle Castling (if implemented and flags are passed)
    # if is_castling_kingside: return "O-O" + ("#" if is_checkmate_after_move else "+" if is_check_after_move else "")
    # if is_castling_queenside: return "O-O-O" + ("#" if is_checkmate_after_move else "+" if is_check_after_move else "")

    return "".join(notation_parts)