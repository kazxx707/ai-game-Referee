AI Game Referee – Rock–Paper–Scissors–Plus

## Overview

This project implements a minimal conversational **AI game referee** for a modified version of Rock–Paper–Scissors, called **Rock–Paper–Scissors–Plus**.

The bot acts as a neutral referee between the user and itself. It explains the rules, validates user intent, enforces constraints (such as one-time bomb usage), tracks state across turns, and ends the game automatically after three rounds.

The focus of this assignment is not UI polish, but correctness of logic, clarity of state modeling, and clean agent design.



## Game Rules

- The game is **best of 3 rounds**
- Valid moves:
  - `rock`
  - `paper`
  - `scissors`
  - `bomb` (can be used **once per game**)
- Bomb beats all other moves
- Bomb vs bomb results in a draw
- Invalid input wastes the round
- After 3 rounds, the game ends automatically with a final result


## State Model

All game-related information is stored in a single `GameState` object, which acts as the **single source of truth**. It contains:

- Current round number
- User score and bot score
- Whether the user or bot has already used their bomb
- Whether the game has ended

The agent itself does not mutate state directly.  
All state changes happen through explicit tools to keep behavior predictable and easy to reason about.



## Agent and Tool Design

The system is designed with a clear separation of responsibilities.

### Intent Understanding
User input is treated as an attempted move. The agent never assumes correctness and always validates intent first.

### Game Logic (Tools)
Core logic is split into focused tools:
- `validate_move`  
  Ensures the move is valid and enforces bomb usage rules.
- `resolve_round`  
  Determines the winner of a single round based on the two moves.
- `update_game_state`  
  Updates round count, scores, bomb usage, and automatically ends the game after three rounds.

This separation improves clarity, testability, and maintainability.

### Response Generation
The agent is responsible only for:
- Calling tools in the correct order
- Producing clear, human-readable responses

Each round response includes:
- Round number
- Moves played by both sides
- Round outcome
- Updated score

When the game ends, a clear final result is shown.

##Tradeoffs Made
	⁃	The bot uses a simple random strategy instead of a smart or adaptive one.
	⁃	The game runs in a CLI instead of a UI to keep focus on agent logic.
	⁃	State is not persisted beyond a single game session.
These choices were made to prioritize clarity, correctness, and alignment with the assignment scope.

##What I’d Improve with More Time
	⁃	Smarter bot strategies based on previous rounds
	⁃	Structured JSON outputs alongside text responses
	⁃	Automated tests for edge cases
	⁃	Multi-agent separation (referee vs player agents)
	⁃	A lightweight chat or web interface
