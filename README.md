# Battleship Game

## Overview

This project is a Python-based implementation of the classic **Battleship** board game, developed for **EECS 581**. The game allows two players to strategically place their fleets of ships on a grid, take turns attacking, and attempt to sink each other’s ships. The first player to sink all of their opponent's ships wins the game.

This project demonstrates key concepts in software engineering, such as modularity, user interface design, input validation, and turn-based gameplay. It is designed to provide an engaging experience with clear game logic and visual feedback.

## Table of Contents
1. [Game Setup](#game-setup)
2. [Game Rules](#game-rules)
3. [Ship Placement](#ship-placement)
4. [Turn Mechanics](#turn-mechanics)
5. [Project Structure](#project-structure)
6. [How to Play](#how-to-play)
7. [Contributing](#contributing)

## Game Setup

The game begins by asking each player to place their fleet on a 10x10 grid. Players can choose the number of ships to place, with a minimum of 1 and a maximum of 5. Once all ships are placed, players take turns attacking each other's grids until one player sinks all of their opponent's ships.

### Ship Placement Overview
Players will specify the starting coordinate of each ship (e.g., A1) and its orientation (horizontal or vertical), except for 1x1 ships, which don't require orientation. The placement must be within bounds, and ships cannot overlap.

## Game Rules

Battleship is a turn-based game played on two 10x10 grids per player:
- **Your Board**: Tracks your ship locations and your opponent’s hits and misses.
- **Opponent's Board**: Shows your attempts to hit and sink their ships.

The goal is to destroy all of your opponent's ships before they destroy yours. Each ship occupies a number of consecutive grid cells, depending on its size, and the objective is to hit every grid cell occupied by a ship.

### Game End
The game ends when one player has successfully hit and destroyed all of their opponent's ships.

## Ship Placement

The ship placement process is dynamic and adapts based on the number of ships the player chooses to place.

- **1 Ship**: A single 1x1 ship
- **2 Ships**: One 1x1 ship and one 1x2 ship
- **3 Ships**: One 1x1, one 1x2, and one 1x3 ship
- **4 Ships**: One 1x1, one 1x2, one 1x3, and one 1x4 ship
- **5 Ships**: One 1x1, one 1x2, one 1x3, one 1x4, and one 1x5 ship

### Steps for Ship Placement
1. **Choosing Ships**: Players choose the number of ships to place, from 1 to 5. The ship sizes vary, and players must place all ships based on the number selected.
2. **Starting Coordinate**: The player specifies the starting coordinate for the ship (e.g., A1).
3. **Orientation (if applicable)**: For ships larger than 1x1, the player must specify the orientation: `H` for horizontal or `V` for vertical.
4. **Validation**: The game checks if the placement is valid (within the grid and non-overlapping with existing ships). Invalid entries prompt the player to try again.

For example:
- If a player chooses 2 ships, they must place one 1x1 ship and one 1x2 ship.
- For 5 ships, the player must place all five ship sizes (1x1, 1x2, 1x3, 1x4, 1x5) on the board.

### Input Format
- Starting coordinate (e.g., A1, B3, J10)
- Orientation for ships larger than 1x1 (e.g., H for horizontal, V for vertical)

## Turn Mechanics

Once both players have placed their ships, the game moves into the attack phase:
1. Players take turns entering coordinates to attack (e.g., B5).
2. The game checks whether the shot is a hit or a miss.
3. The result is displayed to both players: hits are marked, and if all cells of a ship are hit, the ship is announced as "sunk."
4. Play continues until all ships of one player are destroyed.

### Visual Feedback
- **Hit**: Displays on both players’ boards as a hit marker.
- **Miss**: Displays as a miss marker on the attacker’s board.

## Project Structure

The project is organized into several modules to separate different aspects of the game:
- `battleship.py`: Contains the main game loop and game logic.
- `Players`: Handles the individual player logic, such as placing ships, receiving shots, and keeping track of hits and misses.
- `Interface`: Manages the game setup, player interaction, and the main game loop.


## How to Play

### 1. Ship Placement
- Each player is prompted to place their ships on a 10x10 grid.
- Players can choose how many ships to place, from 1 to 5. The number of ships corresponds to the size and number of ships as follows:
  - **1 ship**: 1x1
  - **2 ships**: 1x1, 1x2
  - **3 ships**: 1x1, 1x2, 1x3
  - **4 ships**: 1x1, 1x2, 1x3, 1x4
  - **5 ships**: 1x1, 1x2, 1x3, 1x4, 1x5
- For each ship, the player is asked:
  - **Starting coordinate** (e.g., A1).
  - **Orientation**: Horizontal (`H`) or Vertical (`V`) for ships larger than 1x1.
- Example:
  - Start at A1.
  - Place a 1x3 ship horizontally (choose "H").

### 2. Attack Phase
- Players take turns attacking each other’s grids.
- The game will ask for an attack coordinate (e.g., B4).
- After an attack, the game will notify the player of the result:
  - **Hit**: The attacked location contains an opponent’s ship.
  - **Miss**: The attacked location is empty.
- Hits and misses are displayed on both players' boards, and the game tracks ship damage.
- When a ship is sunk, the game will announce it.

### 3. Winning the Game
- The game continues until one player sinks all of the opponent’s ships.
- The first player to sink all ships wins.

### 4. Exiting the Game
- To exit, close the terminal or stop the game using `Ctrl + C`.

## Contributing

Group 36: Hamza Jalil, Timo Aranjo, Lingfeng Li, Isaac Mohabbat, Harry Wang (listed in no particular order)
