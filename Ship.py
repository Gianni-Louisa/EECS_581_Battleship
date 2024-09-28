'''
Creation date: 9/28/24
'''

from Common import convert_position_to_indices

class Ship:
    def __init__(self):
        self.coordinates = []
        self.size = -1
        self.direction = "-1"

    def add_coordinate(self, position):
        col, row = convert_position_to_indices(position)  # Convert the position to board indices

        if self.size != 1 and self.size != 2: #sets up the unique ship shapes for ships 3-5
            if self.size == 5: #U-shaped ship
                if self.direction == 'N': #ships is an actual U
                    self.coordinates = [(row, col), (row, col-1), (row, col-2), (row-1, col), (row-1, col-2)] #sets up the ship starting from the bottom right of the u
                elif self.direction == 'S': #the U shape is flipped upside down
                    self.coordinates = [(row, col), (row, col+1), (row, col+2), (row+1, col), (row+1, col+2)] #sets up the ship starting from the top left of the upside down u
                elif self.direction == 'E': #the U shape is 90 degrees to the right
                    self.coordinates = [(row, col), (row-1, col), (row-2, col), (row, col+1), (row-2, col+1)] #sets up the ship starting from the bottom left of the right rotated u
                elif self.direction == 'W': #the U shape is 90 degrees to the left
                    self.coordinates = [(row, col), (row+1, col), (row+2, col), (row, col-1), (row+2, col-1)] #sets up the ship starting from the top right of the left rotated u
                else:
                    return False  # Return False for invalid direction.
            elif self.size == 4: #S-shaped ship
                if self.direction == 'N' or self.direction == 'S': #the S shape is rotated 90 degrees to the right
                    self.coordinates = [(row, col), (row+1, col), (row+1, col+1), (row+2, col+1)] #sets up the ship starting from the top of the rotated s
                elif self.direction == 'E' or self.direction == 'W': #the ship is an actual S
                    self.coordinates = [(row, col), (row, col+1), (row-1, col+1), (row-1, col+2)] #sets up the ship starting from the bottom left of the s
                else:
                    return False  # Return False for invalid direction.
            elif self.size == 3: # 3/4-square shaped ship
                if self.direction == 'N': #the square is missing its top right corner
                    self.coordinates = [(row, col), (row+1, col), (row+1, col+1)] #sets up the ship starting from the top of the shape
                elif self.direction == 'S': #the square is missing its bottom left corner
                    self.coordinates = [(row, col), (row-1, col), (row-1, col-1)] #sets up the ship starting from the bottom of the shape
                elif self.direction == 'E': #the square is missing its bottom right corner
                    self.coordinates = [(row, col), (row, col-1), (row+1, col-1)] #sets up the ship starting from the top right of the shape
                elif self.direction == 'W': #the square is missing its top left corner
                    self.coordinates = [(row, col), (row, col+1), (row-1, col+1)] #sets up the ship starting from the bottom left of the ship
                else:
                    return False  # Return False for invalid direction.
        else:
            # Handle regular horizontal or vertical placement for size 1 and 2
            if self.size == 1: #ship size is 1
                self.direction = 'H'  # For a 1x1 ship, direction is irrelevant
            if self.direction == 'H': #ship is being placed horizontally
                self.coordinates = [(row, col + i) for i in range(self.size)] #place the ship starting from the left of the shape
            elif self.direction == 'V': #ship is being placed vertically
                self.coordinates = [(row + i, col) for i in range(self.size)] #place the ship starting from the top of the shape
            else:
                return False  # Invalid direction
            
        return True