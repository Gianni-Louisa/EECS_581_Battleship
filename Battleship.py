import re  # Import the regular expressions module for pattern matching Logic based on chatgpt query and research due to the first time implementing regular expression logic.
import os  # Import the operating system module for clearing the terminal.
import time  # Import the time module for implementing delays.

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
        self.setup_player(self.player1, "Player 1")  # Setup Player 1's board.
        self.setup_player(self.player2, "Player 2")  # Setup Player 2's board.
        self.play_game()  # Start the game loop.

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
        #test
        # Inform the player how many ships they will be placing
        print("+=========================================+")
        print(f"|  {name}, you will be placing {num_ships} ships. |")
        print("+=========================================+")

        print()

        for size in range(1, num_ships + 1):
            self.place_ship(player, size)  # Place each ship on the board.
        self.clear_terminal_with_countdown()  # Clear the terminal after ship placement.

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
            position = input(f"Enter the position (A-J, 1-10) for your {size}x{size} ship: ").strip().upper()  # Prompt for ship position.
            if size > 1:
                direction = input("Enter direction (H for horizontal, V for vertical): ").strip().upper()  # Prompt for ship direction if size > 1.
            else:
                direction = None  # No need for direction if the ship size is 1x1.
            
            if re.match(r'^[A-J](?:[1-9]|10)$', position) and (direction in ('H', 'V') or direction is None): # Regular expression Logic based on chatgpt query and research due to first time implementing regular expression logic.
                if player.place_ship(size, position, direction):
                    print()
                    player.print_board(reveal_ships=True)  # Show the player's board after placing the ship.
                    break  # Break the loop if the ship is placed successfully.
                else:
                    print(f"Error placing {size}x{size} ship: Check ship placement rules and try again.")  # Notify of placement error.
            else:
                if not re.match(r'^[A-J](?:[1-9]|10)$', position): # Regular expression Logic based on chatgpt query and research due to first time implementing regular expression logic.
                    print(f"Invalid position format. Please use format like A1, B2 for your {size}x{size} ship.")  # Notify of position format error.
                if size > 1 and direction not in ('H', 'V'):
                    print(f"Invalid direction. Please enter 'H' for horizontal or 'V' for vertical for your {size}x{size} ship.")  # Notify of direction error.

    def play_game(self):
        """Main game loop."""
        while True:
            self.print_boards()  # Print both players' boards.
            print(f"{self.get_current_player_name()}'s turn:")  # Announce the current player's turn.
            if self.take_shot(self.opponent):
                break  # End the game if there is a winner.
            self.switch_players()  # Switch to the other player.
            self.clear_terminal_with_countdown()  # Clear the terminal before the next turn.

    def print_boards(self):
        """Print both the current player's and the opponent's boards."""
        print()
        print("+======================+")
        print(f"\n{self.get_current_player_name()}'s board:")  # Print the current player's board.
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
            return True  # Return True to indicate the game is won.
        return False  # Return False if no winner yet.

    def get_current_player_name(self):
        """Get the name of the current player."""
        return "Player 1" if self.current_player == self.player1 else "Player 2"  # Return Player 1 or Player 2 based on the current player.

    def switch_players(self):
        """Switch the current player and the opponent."""
        self.current_player, self.opponent = self.opponent, self.current_player  # Swap the current player and opponent.

    def clear_terminal_with_countdown(self):
        """Clear the terminal and show a countdown before changing turns."""
        for i in range(5, 0, -1):
            print(f"Changing turns in {i} seconds...", end='\r')  # Display countdown for 5 seconds.
            time.sleep(1)  # Wait for 1 second.
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
