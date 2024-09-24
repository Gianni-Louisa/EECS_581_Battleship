import re  # Import the regular expressions module for pattern matching Logic based on chatgpt query and research due to the first time implementing regular expression logic.
import os  # Import the operating system module for clearing the terminal.
import time  # Import the time module for implementing delays.
import random
from SaveGame import *

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

    def place_ship(self, size, position, direction=None):
        """Place a ship on the board."""
        col, row = self.convert_position_to_indices(position)  # Convert the position to board indices.
        
        if size == 1:
            direction = 'H'  # For a 1x1 ship, direction is irrelevant.

        if direction == 'H':
            if col + size > 10:  # Check if the ship fits horizontally on the board.
                return False
            for i in range(size):
                if col + i >= 10 or self.board[row][col + i] != 0:  # Check if the ship overlaps with existing ships.
                    return False
            for i in range(size):
                self.board[row][col + i] = size  # Place the ship on the board horizontally.
        elif direction == 'V':
            if row + size > 10:  # Check if the ship fits vertically on the board.
                return False
            for i in range(size):
                if row + i >= 10 or self.board[row + i][col] != 0:  # Check if the ship overlaps with existing ships.
                    return False
            for i in range(size):
                self.board[row + i][col] = size  # Place the ship on the board vertically.
        else:
            return False  # Return False for invalid direction.

        self.ships.append((position, size, direction))  # Add the ship details to the player's ships list.
        return True

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


    def print_board(self, reveal_ships=False):
        """Print the board. If reveal_ships is True, show ships."""
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
                if reveal_ships:
                    position = chr(ord('A') + j) + str(i + 1)
                    cell = self.board[i][j]
                    if position in self.hits:
                        row += "X "  # Print an 'X' for hit positions.
                    elif position in self.misses:
                        row += "O "  # Print an 'O' for miss positions.
                    else:
                        if cell == 0:
                            row += ". "  # Print a dot for unexplored positions.
                        else:
                            row += str(cell) + " "
                else:
                    position = chr(ord('A') + j) + str(i + 1)
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


class Interface:
    def __init__(self):
        # Initialize two players and set Player 1 as the current player.
        self.player1 = Player()
        self.player2 = Player()
        self.current_player = self.player1
        self.opponent = self.player2

    def start(self):
        """Start the game by setting up players and beginning gameplay."""
        print("+====================================+")
        print("|       Welcome to Battleship!       |")  # Greet the players.
        print("+====================================+")
        print()

        self.query_mode() # Ask if playing AI or another player
        self.setup_player(self.player1, "Player 1")  # Setup Player 1's board.
        if not self.playing_ai: # If not playing an AI
            self.setup_player(self.player2, "Player 2")  # Setup Player 2's board.
        else: # If playing an AI
            self.player2.is_ai = True # Set the player's is_ai bool to be true
            self.query_ai_difficulty(self.player2) # Ask user for the difficulty to make the AI
            self.setup_player(self.player2, "Player 2 (AI)") # Setup AI player 2's board
        self.play_game()  # Start the game loop.

    def query_mode(self):
        """Ask player for gamemode"""

        while True: # Loop while getting user input
            playing_cpu = input("Play against CPU? (y/n): ").lower() # Ask user how many human players there will be
            if playing_cpu not in ['yes', 'y', 'no', 'n']: # Check for a valid input
                print("Invalid response. Input 'y' or 'n'") # Print error message if input was not valid
            else: # If valid input
                self.playing_ai = playing_cpu[0]=='y' # Set self.playing_ai boolean to be true if the user typed in a 'yes' or a 'y'
                break # Break out of loop

    def query_ai_difficulty(self, ai_player: Player):
        """Ask human player what difficulty to make the AI that they will be playing against"""
        
        while True: # Loop while getting input
            difficulty = input("What difficulty level should the AI be? Easy(e), Medium(m), or Hard(h): ").lower() # Ask user what difficutly to make AI (and make lowercase)
            if difficulty not in ['easy', 'e', 'medium', 'm', 'hard', 'h']: # If the response is not valid
                print("Invalid difficulty selected for the AI. Respond with 'e', 'm', or 'h' for Easy, Medium, or Hard difficulties respectively") # Print out error message
            else: # If response was valid
                ai_player.difficulty = difficulty[0] # Set ai Player's difficulty to be 'e', 'm', or 'h'
                break # Break out of loop


    def setup_player(self, player, name):
        """Guide a player through placing their ships."""
        #print(f"{name}, place your ships.")  # Prompt the player to place ships.
        
        # Check if the current player is Player 1
        if player == self.player1:
            print(f"{name}, place your ships.") # promt the player to place ships.
            num_ships = self.get_number_of_ships()  # Get the number of ships to place.
            self.num_ships_to_place = num_ships  # Store this value for Player 2 to use later.
        else:
            num_ships = self.num_ships_to_place  # Player 2 places the same number of ships.
        
        # Inform the player how many ships they will be placing
        # if not player.is_ai:
        print("+=========================================+")
        print(f"|  {name}, you will be placing {num_ships} ships. |")
        print("+=========================================+")

        print()

        for size in range(1, num_ships + 1):
            self.place_ship(player, size)  # Place each ship on the board.
        self.clear_terminal()  # Clear the terminal after ship placement.

    def get_number_of_ships(self):
        """Get the number of ships from the player."""
        while True:
            try:
                num_ships = int(input("How many different ships would you like to place (1-5)? "))  # Prompt for the number of ships.
                print()
                if 1 <= num_ships <= 5:
                    return num_ships  # Return the valid number of ships.
                else:
                    print("Please enter a number between 1 and 5.")  # Prompt for a valid number.
            except ValueError:
                print("Invalid input. Please enter a number.")  # Handle non-numeric input.

    def place_ship(self, player, size):
        """Guide the player through placing a single ship on their board."""
        print()
        player.print_board(reveal_ships=True)  # Show the player's board after placing the ship.
        print(f"Placing your 1x{size} ship:")  # Prompt the player to place a ship of given size.
        while True:
            if not player.is_ai: # If the player is a human
                position = input(f"Enter the position (A-J, 1-10) for your {1}x{size} ship: ").strip().upper()  # Prompt for ship position.
            else: # If the player is an AI
                position = f"{random.choice('ABCDEFGHIJ')}{random.randint(1,10)}" # Randomly select a position 
                print("AI randomly chose position =", position) # TODO: debugging

            if size > 1:
                if not player.is_ai: # If player is a human
                    direction = input("Enter direction (H for horizontal, V for vertical): ").strip().upper()  # Prompt for ship direction if size > 1.
                else: # If player is an AI
                    direction = random.choice('HV') # Randomly choose an orientation
                    print("AI randomly choose direction =", direction) # TODO: debugging
            else:
                direction = None  # No need for direction if the ship size is 1x1.
            
            if re.match(r'^[A-J](?:[1-9]|10)$', position) and (direction in ('H', 'V') or direction is None): # Regular expression Logic based on chatgpt query and research due to first time implementing regular expression logic.
                if player.place_ship(size, position, direction):
                    # if not player.is_ai: 
                    print()
                    player.print_board(reveal_ships=True)  # Show the player's board after placing the ship.
                    break  # Break the loop if the ship is placed successfully.
                else:
                    # if not player.is_ai: # Only print if player is a human
                    print(f"Error placing {1}x{size} ship: Check ship placement rules and try again.")  # Notify of placement error.
            else:
                if not re.match(r'^[A-J](?:[1-9]|10)$', position): # Regular expression Logic based on chatgpt query and research due to first time implementing regular expression logic.
                    print(f"Invalid position format. Please use format like A1, B2 for your {1}x{size} ship.")  # Notify of position format error.
                if size > 1 and direction not in ('H', 'V'):
                    print(f"Invalid direction. Please enter 'H' for horizontal or 'V' for vertical for your {1}x{size} ship.")  # Notify of direction error.

    def play_game(self):
        """Main game loop."""
        while True:
            self.print_boards()  # Print both players' boards.
            print(f"{self.get_current_player_name()}'s turn:")  # Announce the current player's turn.
            if self.take_shot(self.opponent):
                break  # End the game if there is a winner.
            self.switch_players()  # Switch to the other player.
            self.clear_terminal()  # Clear the terminal before the next turn.

    def print_boards(self):
        """Print both the current player's and the opponent's boards."""
        print()
        print("+======================+")
        print(f"| {self.get_current_player_name()}'s board:    |")  # Print the current player's board.
        print("+======================+")
        self.current_player.print_board(reveal_ships=True)

        print()
        print("+======================+")
        print("|  Opponent's board:   |")  # Print the opponent's board.
        print("+======================+")
        self.opponent.print_board()  

    def take_shot(self, opponent):
        """Handle a shot taken by the current player at the opponent's board."""
        while True:
            # If the player taking the shot is NOT an AI
            if not self.current_player.is_ai:
                position = input(f"Enter your shot (A-J, 1-10): ").strip().upper()  # Prompt for the shot position.
                if re.match(r'^[A-J](?:[1-9]|10)$', position): # Regular expression Logic based on chatgpt query and research due to first time implementing regular expression logic.
                    result = opponent.receive_shot(position)  # Process the shot and get the result.
                    
                    if result == 'Already Shot':
                        print("You've already shot at this position. Try again.")  # Notify of repeated shot.
                        continue  # Continue asking for a valid shot.
                    
                    if result == 'Hit':
                        print("Hit!")  # Notify of a hit.
                    elif result == 'Miss':
                        print("Miss.")  # Notify of a miss.
                    elif result == 'Sunk':
                        print(f"Hit! Ship size {self.get_ship_size_at(position)}. Sunk!")  # Notify of a sunk ship.
                    return self.check_winner()  # Check for a winner after the shot.
                else:
                    print("Invalid input format or out of bounds. Please use format like A1, B2.")  # Notify of an invalid shot position.

            # If player taking shot IS an AI
            else:
                # Easy mode - randomly choose location and shoot at it
                if self.current_player.difficulty == 'e':
                    position = f"{random.choice('ABCDEFGHIJ')}{random.randint(1,10)}" # Randomly select a position 
                    print("AI randomly chose position =", position, "to shoot") # TODO: remove
                    result = opponent.receive_shot(position) # Process the shot and get the result.

                    if result == 'Already Shot':
                        print("You've already shot at this position. Try again.")  # Notify of repeated shot.
                        continue  # Continue asking for a valid shot.

                    if result == 'Hit': 
                        self.current_player.previous_turn_hit_location = position # Set the previous_turn_hit_location to the location that was just hit
                        print("Hit!")  # TODO: remove
                    elif result == 'Miss': 
                        self.current_player.previous_turn_hit_location = None # Set the previous_turn_hit_location to None since AI did not hit anything
                        print("Miss.")  # TODO: remove
                    elif result == 'Sunk':
                        self.current_player.previous_turn_hit_location = None # Set the previous_turn_hit_location to None since AI sunk the ship 
                        print(f"Hit! Ship size {self.get_ship_size_at(position)}. Sunk!") # TODO: remove
                    return self.check_winner()  # Check for a winner after the shot.

                # Medium mode - randomly shoot until a hit, then shoot spaces orthogonal to hit location
                elif self.current_player.difficulty == 'm':
                    if (self.current_player.previous_turn_hit_location is None) and (self.current_player.orthogonal_points_to_shoot is None): # If the AI did NOT hit a ship on the last turn, 
                        
                        position = f"{random.choice('ABCDEFGHIJ')}{random.randint(1,10)}" # Randomly select a position 
                        print("Medium AI randomly chose position =", position, "to shoot") # TODO: remove

                        result = opponent.receive_shot(position) # Process the shot and get the result.
                        if result == 'Already Shot': 
                            print("already shot this position") # TODO: remove
                            continue  # Continue asking for a valid shot.
                        if result == 'Hit': 
                            self.current_player.previous_turn_hit_location = position # Set the previous_turn_hit_location to the location that was just hit
                            print("Hit!")  # TODO: remove
                        elif result == 'Miss': 
                            self.current_player.previous_turn_hit_location = None # Set the previous_turn_hit_location to None since AI did not hit anything
                            print("Miss.")  # TODO: remove
                        elif result == 'Sunk': 
                            self.current_player.previous_turn_hit_location = None # Set the previous_turn_hit_location to None since AI sunk the ship 
                            print(f"Hit! Ship size {self.get_ship_size_at(position)}. Sunk!") # TODO: remove
                        return self.check_winner() # Check for a winner after the shot.
                    
                    # If AI DID hit a ship on last turn or is going through points orthogonal to a hit
                    else:
                        # If have not started shooting at orthogonal points
                        if self.current_player.orthogonal_points_to_shoot is None:
                            orthogonal_point_locations = self.get_orthogonal_points(self.current_player.previous_turn_hit_location) # Get points orthogoanl to the last hit
                            print(f"Points orthogonal to {self.current_player.previous_turn_hit_location} are: ", orthogonal_point_locations) # TODO: remove
                            self.current_player.orthogonal_points_to_shoot = orthogonal_point_locations # Set AI Player's orthogonal_points_to_shoot to be the points orthogonal 

                            # self.current_player.previous_turn_hit_location = None # Set AI PLayer previous_turn_hit_location to None 

                        shot_location = self.current_player.orthogonal_points_to_shoot.pop() # Get one of the orthogonal points to shoot while popping it from the list
                        print("AI shooting an orthogonal point: ", shot_location)
                        result = opponent.receive_shot(shot_location) # Shoot at location
                        if result == 'Already Shot': 
                            print("already shot this position") # TODO: remove
                            continue  # Continue asking for a valid shot.
                        if result == 'Hit': 
                            self.current_player.previous_turn_hit_location = shot_location # Set the previous_turn_hit_location to the location that was just hit
                            self.current_player.orthogonal_points_to_shoot = None # Set AI Player orthogonal_points_to_shoot to None since we hit another point which will now be the point to be shot around
                            print("Hit!")  # TODO: remove
                        elif result == 'Miss': 
                            self.current_player.previous_turn_hit_location = None # Set the previous_turn_hit_location to None since AI did not hit anything
                            print("Miss.")  # TODO: remove
                        elif result == 'Sunk': 
                            self.current_player.previous_turn_hit_location = None # Set the previous_turn_hit_location to None since AI sunk the ship 
                            self.current_player.orthogonal_points_to_shoot = None # Set AI Player orthogonal_points_to_shoot to None since the ship was sunk
                            print(f"Hit! Ship size {self.get_ship_size_at(shot_location)}. Sunk!") # TODO: remove
                        return self.check_winner() # Check for a winner after the shot.


                # TODO: Hard mode - shoot at player's ships every time
                elif self.current_player.difficulty == 'h':
                    pass

    def get_orthogonal_points(self, hit_location: str) -> list:
        """Get positions orthogonal to the 'hit_location'"""

        cols = "ABCDEFGHIJ" # String of the possible columns
        hit_col_inx = cols.index(hit_location[0]) # Get the index of the column where the hit was
        hit_row = int(hit_location[1:]) # Get the row number of the hit

        ortho_points = [] # Create a list to store the points orthogonal
        if hit_col_inx > 0: # Check there is a column to the LEFT the point being checked
            ortho_points.append(f"{cols[hit_col_inx-1]}{hit_row}") # Add position to the LEFT to list of orthogonal points
        if hit_col_inx < 9: # Check there is a column to the RIGHT of the point being checked
            ortho_points.append(f"{cols[hit_col_inx+1]}{hit_row}") # Add position to the RIGHT to list of orthogonal points
        if hit_row > 1: # Check there is a row ABOVE the point being checked
            ortho_points.append(f"{cols[hit_col_inx]}{hit_row-1}") # Add position ABOVE to list of orthogonal points
        if hit_row < 10: # Check there is a row below the point being checked
            ortho_points.append(f"{cols[hit_col_inx]}{hit_row+1}") # Add position BELOW to the list of orthogonal points

        return ortho_points

            

    def get_ship_size_at(self, position):
        """Get the size of the ship at a specific position."""
        col, row = self.convert_position_to_indices(position)  # Convert position to board indices.
        for (pos, size, direction) in self.opponent.ships:
            ship_col, ship_row = self.convert_position_to_indices(pos)  # Convert ship position to board indices.
            if direction == 'H' and ship_row == row and ship_col <= col < ship_col + size:
                return size  # Return the size if the ship is placed horizontally and the position is valid.
            if direction == 'V' and ship_col == col and ship_row <= row < ship_row + size:
                return size  # Return the size if the ship is placed vertically and the position is valid.
        return 0  # Return 0 if no ship is found at the position.

    def check_winner(self):
        """Check if the game has a winner."""
        # Calculate the total number of ship cells based on placed ships.
        total_ship_cells = sum(size for _, size, _ in self.opponent.ships)

        # Compare the number of unique hits to the total number of ship cells.
        if len(self.opponent.hits) == total_ship_cells:
            print(f"{self.get_current_player_name()} wins!")  # Announce the winner.
            num = self.get_current_player_number()
            updateSave(num) #updates the save file
            printScoreBoard() #shows the score board
            #
            #scorebard additionts here
            #
            return True  # Return True to indicate the game is won.
        return False  # Return False if no winner yet.

    def get_current_player_name(self):
        """Get the name of the current player."""
        return "Player 1" if self.current_player == self.player1 else "Player 2"  # Return Player 1 or Player 2 based on the current player.

    def get_current_player_number(self):
        return 0 if self.current_player == self.player1 else 1 if self.current_player == self.player2 else 2  # Return 1 or 2 based on the current player.
    
    def switch_players(self):
        """Switch the current player and the opponent."""
        self.current_player, self.opponent = self.opponent, self.current_player  # Swap the current player and opponent.

    def clear_terminal(self):
        return # TODO: debugging
        """Clear the terminal before changing turns."""
        os.system('cls' if os.name == 'nt' else 'clear')  # Clear the terminal based on the operating system.
        input("\nPress Enter to continue to the next player's turn...")  # Pause for user input to continue.
        print()
        # print("\n" + "="*40)  # Print a separator line for clarity.

    def convert_position_to_indices(self, position):
        """Convert board position from letter-number format to indices."""
        col = ord(position[0]) - ord('A')  # Convert column letter to index (0-9).
        row = int(position[1:]) - 1  # Convert row number to index (0-9).
        return col, row  # Return the column and row indices.

if __name__ == "__main__":
    game = Interface()  # Create an instance of the Interface class.
    game.start()  # Start the game.
