
# Battleship Game

**Updated with AI opponents, Offline Scoreboard, and Custom Ship Shapes**

This game allows players to battle either against each other or against AI-controlled opponents. Additionally, the game includes an offline-compatible scoreboard and introduces customizable ship shapes. Below is an in-depth explanation of how each feature works, detailing the key functions involved and their purposes.

---

## New Features

### 1. **AI Opponents (Single Player Mode)**
We added an AI opponent system with three difficulty levels: Easy, Medium, and Hard. Each difficulty level employs a different strategy when taking its turn.

#### How it works:
- **Easy Difficulty:**
    - The AI fires randomly at unguessed positions.
    - The function `random_fire()` is responsible for generating a random coordinate that hasn't been targeted yet. It uses a list of possible coordinates, shuffling or filtering out the ones that have already been hit.
    - **Key Functions:**
        - `AI.easy_turn()`: Calls `random_fire()` and marks the grid with the result of the shot (hit or miss).

- **Medium Difficulty:**
    - The AI starts firing randomly but once it hits a ship, it continues to fire in adjacent orthogonal directions (up, down, left, or right) to try to sink the ship.
    - The function `target_adjacent()` is used to focus the AI's subsequent shots after a hit is detected.
    - **Key Functions:**
        - `AI.medium_turn()`: First calls `random_fire()` for the initial shot. If a hit is registered, it calls `target_adjacent()` to focus on sinking the ship.
        - `target_adjacent()`: Determines the next direction (up, down, left, right) to fire based on the previous successful hit.
        
- **Hard Difficulty:**
    - The AI knows where all the player's ships are located and will hit a ship every turn.
    - The function `cheat_fire()` is used, which directly targets the next unsunk ship.
    - **Key Functions:**
        - `AI.hard_turn()`: Uses `cheat_fire()` to select the exact coordinates of the next ship location and guarantees a hit every turn.
        
**Functional Flow**:
- The function `start_game()` is responsible for initializing the game mode. If the player chooses to play against the AI, the game sets up the AI's difficulty level and links the corresponding AI function (easy, medium, or hard) to the game loop.
- During the game loop, `take_turn()` is called to alternate between the player and the AI's turns, invoking the appropriate AI function based on the selected difficulty.

---

### 2. **Scoreboard**
We implemented an scoreboard system that allows players to track their wins and losses throughout games even when the program has stopped. This scoreboard is persistent, storing results locally in a JSON file.

#### How it works:
- The `SaveGame.py` file manages saving and loading game data, including the scoreboard. We use the JSON module to write and read from the local storage.
- **Key Functions:**
    - `save_score()`:
        - This function is called at the end of each game to store the result (win or loss) in a local JSON file. It appends the current score to the existing records.
        - `save_score()` first checks if the scoreboard file exists. If it does, it updates the file; if not, it creates a new one.
    - `load_scoreboard()`:
        - This function loads the scoreboard from the local storage when the game starts or when the player requests to view it. It reads the JSON file and converts the data into a usable format.
        
**Functional Flow**:
- After each game, `update_scoreboard()` is called, which in turn calls `save_score()`. This ensures that the latest game result is saved immediately.
- During initialization (`start_game()`), `load_scoreboard()` is called to bring in the existing scoreboard data, so that previous results are available to the player.

---

### 3. **New Ship Shapes**
To add more variety and challenge to the gameplay, we introduced new ship shapes that deviate from the standard rectangular forms. These include dot, line, L shaped, S shaped, and U shaped.


![image](https://github.com/user-attachments/assets/fe95aada-a28d-4acd-990e-cc2b79476d93)



#### How it works:
- The `Ship.py` file handles the configuration and placement of these new ship shapes. Each shape is represented as a collection of relative coordinates.
- **Key Functions:**
    - `Ship.__init__()`:
        - This constructor is called when creating a new ship. It assigns a shape and validates the placement based on the game grid’s boundaries.
        - The `ship_shape` parameter passed to the constructor determines the shape of the ship. Shapes are defined as a list of relative coordinates.
    - `place_ship()`:
        - Called during the setup phase to randomly place a ship on the grid. The function ensures that ships do not overlap and fit within the grid's dimensions, regardless of their shape.
        - It loops over the possible placements and checks that each part of the ship fits and does not collide with other ships.
    - `validate_placement()`:
        - This function ensures that all parts of the ship lie within the grid and do not overlap with existing ships. It is crucial for managing complex shapes.
        
**Functional Flow**:
- When starting a new game, `setup_ships()` is called, which in turn calls `place_ship()` for each ship, passing a unique shape for each one.
- The `validate_placement()` function is invoked inside `place_ship()` to confirm that each ship is placed legally on the grid.

---

## Code Architecture and Functionality

- **Battleship.py**: The main entry point that manages the game’s flow.
    - Calls functions like `start_game()` to initialize settings, `take_turn()` for alternating between players or AI, and `update_scoreboard()` for saving results.
- **Player.py**: Contains the logic for AI decision-making.
    - Functions like `random_fire()`, `target_adjacent()`, and `cheat_fire()` are used depending on the AI difficulty.
- **SaveGame.py**: Manages saving and loading game states.
    - `save_score()` and `load_scoreboard()` ensure the persistence of game results.
- **Ship.py**: Handles ship shapes and placement logic.
    - `place_ship()` and `validate_placement()` ensure correct ship placement and shape usage.
- **Common.py**: Contains utility functions and shared constants.
    - Provides useful constants and helper functions used throughout the code.

---
## Project Additions Done By:
### Gianni Louisa, Brinley Hull, Ben Renner, Kyle Moore, Connor Bennudriti
