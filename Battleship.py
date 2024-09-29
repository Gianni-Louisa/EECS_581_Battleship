"""
Battleship.py
A python base file to play battleship on console.
Inputs: nothing
Outputs: A functional battleship game!
Other sources of code: chatgpt and unknown from previous team
Authors: Previous Team and Connor Bennudriti, Brinley Hull, Gianni Louisa, Kyle Moore, Ben Renner
Creation date: unknown from previous team
"""

import re  # Import the regular expressions module for pattern matching Logic based on chatgpt query and research due to the first time implementing regular expression logic.
import os  # Import the operating system module for clearing the terminal.
import time  # Import the time module for implementing delays.
import random # Import the random module
from SaveGame import * # Import the scoreboard
from Player import Player # Import the Player class
from Common import convert_position_to_indices # Import the common functions

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
        
        if player == self.player1:
            print(f"{name}, place your ships.")  # Prompt the player to place ships.
            num_ships = self.get_number_of_ships()  # Get the number of ships to place.
            self.num_ships_to_place = num_ships  # Store this value for Player 2 to use later.
        else:
            num_ships = self.num_ships_to_place  # Player 2 places the same number of ships.

        print("+=========================================+")
        print(f"|  {name}, you will be placing {num_ships} ships. |")
        print("+=========================================+")
        print()

        player.print_board() # Print the player's board.

        if player.is_ai: # If the player is an AI
            # AI does not show placement details
            print("AI is placing its ships...") # Only show this message for AI
            for size in range(1, num_ships + 1): # Loop through the number of ships to place
                player.place_ship(size)  # Place each ship on the board.
            print("AI has placed its ships.")  # Only show this message for AI
        else: # If the player is not an AI
            for size in range(1, num_ships + 1): # Loop through the number of ships to place
                player.place_ship(size)  # Place each ship on the board.

        input("Press enter to continue...") # Wait for the user to acknowledge the ship placement.
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

    def play_game(self):
        """Main game loop."""
        while True:
            if not self.current_player.is_ai: # If the current player is not an AI
                self.print_boards()  # Print both players' boards only if it's not the AI's turn
            print(f"{self.get_current_player_name()}'s turn:")
            if self.take_shot(self.opponent):
                break  # End the game if there is a winner.
            input("Press enter to continue to the next player...")  # Wait to see hit or miss announcement
            self.switch_players()  # Switch to the other player.
            self.clear_terminal()  # Clear the terminal before the next turn.


    def print_boards(self):
        """Print both the current player's and the opponent's boards."""
        print()
        print("+======================+")
        print(f"| {self.get_current_player_name()}'s board:    |")
        print("+======================+")
        self.current_player.print_board(reveal_ships=True)

        print()
        print("+======================+")
        print("|  Opponent's board:   |")
        print("+======================+")
        # Only show AI's shots on the opponent's board
        self.opponent.print_board(show_shots_only=True)

    def take_shot(self, opponent):
        """Handle a shot taken by the current player at the opponent's board."""
        while True:
            # If player taking the shot is NOT an AI
            if not self.current_player.is_ai:
                position = input(f"Enter your shot (A-J, 1-10): ").strip().upper()  # Prompt for the shot position.
                if re.match(r'^[A-J](?:[1-9]|10)$', position): # Regular expression logic
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
                    position = f"{random.choice('ABCDEFGHIJ')}{random.randint(1,10)}"  # Randomly select a position 
                    print(f"AI chose position {position} to shoot.")  # Display AI's shot position
                    
                    result = opponent.receive_shot(position)  # Process the shot and get the result.
                    if result == 'Already Shot':
                        print("AI already shot at this position. Trying again.") # Notify of repeated shot.
                        continue  # Continue asking for a valid shot.
                    
                    if result == 'Hit': 
                        self.current_player.previous_turn_hit_location = position  # Set the previous_turn_hit_location to the location that was just hit
                        print(f"AI Hit at {position}!")  # Notify of a hit
                    elif result == 'Miss': 
                        self.current_player.previous_turn_hit_location = None  # Set the previous_turn_hit_location to None since AI did not hit anything
                        print(f"AI Missed at {position}.")  # Notify of a miss
                    elif result == 'Sunk':
                        self.current_player.previous_turn_hit_location = None  # Set the previous_turn_hit_location to None since AI sunk the ship 
                        print(f"AI Hit! Ship size {self.get_ship_size_at(position)}. Sunk at {position}!") # Notify of a sunk ship
                    
                    input("\nPress Enter to continue to the next player's turn...")  # Wait for the user to acknowledge the AI's move.
                    return self.check_winner()  # Check for a winner after the shot.
                
                # Medium mode - randomly shoot until a hit, then shoot spaces orthogonal to hit location
                elif self.current_player.difficulty == 'm': # If the AI is set to medium difficulty
                    if (self.current_player.previous_turn_hit_location is None) and (self.current_player.orthogonal_points_to_shoot is None): # If the AI did NOT hit a ship on the last turn, 
                        
                        position = f"{random.choice('ABCDEFGHIJ')}{random.randint(1,10)}" # Randomly select a position 
                        print("Medium AI randomly chose position =", position, "to shoot") 
                        result = opponent.receive_shot(position) # Process the shot and get the result.
                        if result == 'Already Shot':  # If the position was already shot at
                            print("already shot this position") # TODO: remove
                            continue  # Continue asking for a valid shot.
                        if result == 'Hit': # If the shot was a hit
                            self.current_player.previous_turn_hit_location = position # Set the previous_turn_hit_location to the location that was just hit
                            print("Hit!")  # print
                        elif result == 'Miss': # If the shot was a miss
                            self.current_player.previous_turn_hit_location = None # Set the previous_turn_hit_location to None since AI did not hit anything
                            print("Miss.")  # TODO: remove
                        elif result == 'Sunk': # If the shot sunk a ship
                            self.current_player.previous_turn_hit_location = None # Set the previous_turn_hit_location to None since AI sunk the ship 
                            print(f"Hit! Ship size {self.get_ship_size_at(position)}. Sunk!") # print the size of the ship that was sunk
                        return self.check_winner() # Check for a winner after the shot.
                    
                    # If AI DID hit a ship on last turn or is going through points orthogonal to a hit
                    else: # If the AI hit a ship on the last turn or is going through points orthogonal to a hit
                        # If have not started shooting at orthogonal points
                        if self.current_player.orthogonal_points_to_shoot is None: # If the AI has not started shooting at orthogonal points
                            orthogonal_point_locations = self.get_orthogonal_points(self.current_player.previous_turn_hit_location) # Get points orthogoanl to the last hit
                            print(f"Points orthogonal to {self.current_player.previous_turn_hit_location} are: ", orthogonal_point_locations) #print the orthogonal points
                            self.current_player.orthogonal_points_to_shoot = orthogonal_point_locations # Set AI Player's orthogonal_points_to_shoot to be the points orthogonal 
                            # self.current_player.previous_turn_hit_location = None # Set AI PLayer previous_turn_hit_location to None 
                        shot_location = self.current_player.orthogonal_points_to_shoot.pop() # Get one of the orthogonal points to shoot while popping it from the list
                        print("AI shooting an orthogonal point: ", shot_location) # print the point that the AI is shooting at
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
                            print(f"Hit! Ship size {self.get_ship_size_at(shot_location)}. Sunk!") 
                        return self.check_winner() # Check for a winner after the shot.
                # Hard mode - never miss, shoot directly at ship locations
                elif self.current_player.difficulty == 'h': # If the AI is set to hard difficulty
                    # Find the first cell that contains a ship that hasn't been hit yet
                    for i in range(10):  # Loop through the rows
                        for j in range(10): # Loop through the columns
                            position = f"{chr(ord('A') + j)}{i+1}"  # Convert the board indices to a position
                            if self.opponent.board[i][j] != 0 and position not in self.current_player.hits:  # Find unhit ship cells
                                result = opponent.receive_shot(position)  # Shoot at the found ship cell
                               
                                
                                if result == 'Already Shot': # If the position was already shot at
                                    continue  # If already shot, continue searching for another ship position
                                print(f"Hard AI shot at {position}")  # Print the position that the AI shot at
                                if result == 'Hit': # If the shot was a hit
                                    self.current_player.previous_turn_hit_location = position  # Set the previous_turn_hit_location to the location that was just hit
                                    print("Hit!")  # Print hit
                                elif result == 'Miss': # If the shot was a miss
                                    self.current_player.previous_turn_hit_location = None  # Set the previous_turn_hit_location to None since AI did not hit anything
                                    print("Miss.") # Print miss
                                elif result == 'Sunk': # If the shot sunk a ship
                                    self.current_player.previous_turn_hit_location = None  # Set the previous_turn_hit_location to None since AI sunk the ship
                                    print(f"Hit! Ship size {self.get_ship_size_at(position)}. Sunk!")  # Print the size of the ship that was sunk
                                
                                return self.check_winner()  # Check for a winner after the shot


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
        col, row = convert_position_to_indices(position)  # Convert position to board indices.
        for ship in self.opponent.ships:
            if (col, row) in ship.coordinates:
                return ship.size  # Return the size if the position is valid.
        return 0  # Return 0 if no ship is found at the position.

    def check_winner(self):
        """Check if the game has a winner."""
        total_ship_cells = 0 # Initialize the total ship cell count
        for ship in self.opponent.ships: # Iterate through opponents ships to calculate total number of ship cells
            for coordinate in ship.coordinates: # Iterate through the coordinates and count how many
                total_ship_cells += 1 # Add the count to the total count

        if len(self.opponent.hits) == total_ship_cells:  # Compare unique hits to total ship cells.
            winner_name = self.get_current_player_name()
            
            if winner_name == "Player 1":
                print(f"Player 1 wins!")
                updateSave(0)  # Update save for Player 1
            elif winner_name == "Player 2":
                print(f"Player 2 wins!")
                updateSave(1)  # Update save for Player 2
            else:
                print(f"CPU wins!")
                updateSave(2)  # Update save for CPU
            
            printScoreBoard()  # Show the updated scoreboard
            return True  # Return True to indicate game is over
        return False  # No winner yet, return False


    def get_current_player_name(self):
        """Get the name of the current player."""
        if self.current_player.is_ai: # If the current player is an AI
            return "CPU"  # Return "CPU" for AI player
        return "Player 1" if self.current_player == self.player1 else "Player 2"  # Return Player 1 or Player 2 based on the current player

    def get_current_player_number(self):
        return 0 if self.current_player == self.player1 else 1 if self.current_player == self.player2 else 2  # Return 1 or 2 based on the current player.
    
    def switch_players(self):
        """Switch the current player and the opponent."""
        self.current_player, self.opponent = self.opponent, self.current_player  # Swap the current player and opponent.

    def clear_terminal(self): # Clear the terminal
        """Clear the terminal before changing tyurns.""" 
        os.system('cls' if os.name == 'nt' else 'clear')  # Clear the terminal based on the operating system.
        input("\nPress Enter to continue to the next player's turn...")  # Pause for user input to continue.
        print()
        # print("\n" + "="*40)  # Print a separator line for clarity.

if __name__ == "__main__":
    game = Interface()  # Create an instance of the Interface class.
    game.start()  # Start the game.