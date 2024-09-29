"""
Player.py
A player class to keep track of the battleship players and their attributes
Inputs: nothing
Outputs: nothing
Other sources of code: chatgpt
Authors: Previous Team and Connor Bennudriti, Brinley Hull, Gianni Louisa, Kyle Moore, Ben Renner
Creation date: 9/28/24
"""

import re  # Import the regular expressions module for pattern matching Logic based on chatgpt query and research due to the first time implementing regular expression logic.
import random
from Ship import Ship

class Player:
    def __init__(self):
        # Initialize a 10x10 board filled with zeros to represent empty cells.
        self.board = [[0]*10 for _ in range(10)]  
        # List to keep track of the ships placed by the player.
        self.ships = []  
        # Set to keep track of hit positions.
        self.hits = set()  
        # Set to keep track of miss positions.
        self.misses = set()  
        # Bool to set the Player to be an AI
        self.is_ai = False
        # A string to track where the player hit on their previous turn (equal to None if player did not get a hit on the previous turn, otherwise it is the location of the hit)
        self.previous_turn_hit_location = None
        # A list to store points orthogonal to a hit point 
        self.orthogonal_points_to_shoot = None

#start of team, chat gpt, and previous team authored

    def place_ship(self, size):
        """Place a ship on the board."""
        current_ship = Ship()  # Initialize a new ship
        current_ship.size = size  # Add the size property to the ship
        print()
        
        if self.is_ai:
            # AI will place ships randomly without printing the placement details
            while True: # Loop until ship is placed in a valid position
                position = f"{random.choice('ABCDEFGHIJ')}{random.randint(1, 10)}"  # Randomly select a position
                if size <= 2:
                    current_ship.direction = random.choice('HV')  # Randomly choose orientation for size 1 and 2 ships
                else:
                    current_ship.direction = random.choice('NSEW')  # Randomly choose orientation for larger ships

                # Don't print AI's chosen position or direction
                valid_placement = current_ship.set_coordinates(position)  # Set the ship's coordinate
                for r, c in current_ship.coordinates:  # Check if ship placement is valid (within bounds and no overlap)
                    if r >= 10 or c >= 10 or r < 0 or c < 0 or self.board[r][c] != 0:  # Check boundaries and overlap
                        valid_placement = False
                        break
                if valid_placement:
                    break  # Break the loop if the ship is placed successfully
        else:  # If the player is a human
            print(f"Placing your {1}x{size} ship:")
            while True:
                position = input(f"Enter the position (A-J, 1-10) for your {1}x{size} ship: ").strip().upper()  # Prompt for ship position.
                if size == 1:
                    direction = "H"  # It doesn't matter what direction it is
                elif size == 2:
                    direction = input("Enter direction (H for horizontal, V for vertical): ").strip().upper()  # Prompt user for direction
                else:
                    direction = input("Enter direction (N for north, S for south, E for east, W for west): ").strip().upper()  # Prompt user for direction
                
                if re.match(r'^[A-J](?:[1-9]|10)$', position) and (direction in ('H', 'V', 'N', 'S', 'E', 'W')):  # Validate input
                    current_ship.direction = direction  # Set the ship's direction
                    valid_placement = current_ship.set_coordinates(position)  # Set the ship's coordinate
                    for r, c in current_ship.coordinates:  # Check if ship placement is valid
                        if r >= 10 or c >= 10 or r < 0 or c < 0 or self.board[r][c] != 0:  # Check boundaries and overlap
                            valid_placement = False
                            break
                    if valid_placement:  # Convert the position to a coordinate and set the ship's coordinate
                        break  # Break the loop if the ship is placed successfully
                    else:
                        print(f"Error placing {1}x{size} ship: Check ship placement rules and try again.")  # Notify of placement error.
                else:
                    if not re.match(r'^[A-J](?:[1-9]|10)$', position):
                        print(f"Invalid position format. Please use format like A1, B2 for your {1}x{size} ship.")  # Notify of position format error.
                    if size > 1 and direction not in ('H', 'V', 'N', 'S', 'E', 'W'):
                        print(f"Invalid direction. Please enter 'H' for horizontal or 'V' for vertical for your {1}x{size} ship.")  # Notify of direction error.

        for r, c in current_ship.coordinates:  # Place the ship on the board
            self.board[r][c] = size  # Add numbers to the board equal to the total size of the ship

        self.ships.append(current_ship)  # Record the ship's coordinates and size

        if not self.is_ai:  # Make sure we don't reveal the AI board
            self.print_board(reveal_ships=True)  # Show the player's board after placing the ship.

        return True

    
#end of team, chat gpt, and previous team authored
    def receive_shot(self, position):
        """Receive a shot on the board and return the result."""
        col, row = self.convert_position_to_indices(position)  # Convert the shot position to board indices.
        
        # Check if the shot has already been made
        if position in self.hits or position in self.misses:
            return 'Already Shot'  # Notify that the position has already been shot at
        
        cell_Value = self.board[row][col]

        if cell_Value != 0 and position not in self.hits:
            self.hits.add(position)
            
            sunk = True

            for i in range(10):
                for j in range(10):
                    if self.board[i][j] == cell_Value:
                        if ( str( chr(j + ord("A")) ) + str(i+1) ) not in self.hits:
                            sunk = False
            if sunk:
                return 'Sunk'
            else:
                return 'Hit'
        else:
            self.misses.add(position)
            return 'Miss'


    def print_board(self, reveal_ships=False, show_shots_only=False):
        """Print the board. If reveal_ships is True, show ships. If show_shots_only is True, only show shots."""
        # Print column labels from A to J.
        print("   " + " ".join(chr(ord('A') + i) for i in range(10)))
        for i in range(10):
            # Print the row label and the data for each cell in the row.
            row_index = i + 1
            if row_index < 10:
                row = str(i + 1) + "  "
            else:
                row = str(i + 1) + " "
            for j in range(10):
                position = chr(ord('A') + j) + str(i + 1)  # Get the position (e.g., A1, B2)
                if show_shots_only:
                    # Display only the shots taken (hits/misses) for the AI opponent
                    if position in self.hits:
                        row += "X "  # Print an 'X' for hit positions.
                    elif position in self.misses:
                        row += "O "  # Print an 'O' for miss positions.
                    else:
                        row += ". "  # Print a dot for unexplored positions.
                elif reveal_ships:
                    # Reveal ships on the board
                    cell = self.board[i][j]
                    if position in self.hits:
                        row += "X "  # Print an 'X' for hit positions.
                    elif position in self.misses:
                        row += "O "  # Print an 'O' for miss positions.
                    else:
                        if cell == 0:
                            row += ". "  # Print a dot for unexplored positions.
                        else:
                            row += str(cell) + " "  # Show ship number (or whatever identifier)
                else:
                    # Standard view without revealing ships
                    if position in self.hits:
                        row += "X "  # Print an 'X' for hit positions.
                    elif position in self.misses:
                        row += "O "  # Print an 'O' for miss positions.
                    else:
                        row += ". "  # Print a dot for unexplored positions.
            print(row)
        print()


    def convert_position_to_indices(self, position):
        """Convert board position from letter-number format to indices."""
        col = ord(position[0]) - ord('A')  # Convert column letter to index (0-9).
        row = int(position[1:]) - 1  # Convert row number to index (0-9).
        return col, row  # Return the column and row indices.
