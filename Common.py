"""
Creation date: 9/28/24
"""

def convert_position_to_indices(position):
    """Convert board position from letter-number format to indices."""
    col = ord(position[0]) - ord('A')  # Convert column letter to index (0-9).
    row = int(position[1:]) - 1  # Convert row number to index (0-9).
    return col, row  # Return the column and row indices.