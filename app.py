from typing import Literal, Dict
from dataclasses import dataclass
import random

# ============================================================
# GAME STATE
# ============================================================
# This object represents the single source of truth for the game.
# It persists across turns and is updated ONLY via tools.
# ============================================================

@dataclass
class GameState:
    round_number: int = 0
    user_score: int = 0
    bot_score: int = 0
    user_bomb_used: bool = False
    bot_bomb_used: bool = False
    game_over: bool = False


# ============================================================
# TOOL 1: MOVE VALIDATION
# ============================================================
# Responsible only for checking:
# - Is the move allowed?
# - Has bomb already been used?
# No game logic or scoring happens here.
# ============================================================

def validate_move(user_input: str, bomb_already_used: bool) -> Dict:
    move = user_input.lower().strip()
    allowed_moves = {"rock", "paper", "scissors", "bomb"}

    if move not in allowed_moves:
        return {
            "valid": False,
            "reason": "That is not a valid move."
        }

    if move == "bomb" and bomb_already_used:
        return {
            "valid": False,
            "reason": "Bomb can only be used once per game."
        }

    return {
        "valid": True,
        "move": move
    }


# ============================================================
# TOOL 2: ROUND RESOLUTION
# ============================================================
# Determines the winner of a single round.
# Returns: "user", "bot", or "draw"
# ============================================================

def resolve_round(user_move: str, bot_move: str) -> Literal["user", "bot", "draw"]:

    # Exact same move → draw
    if user_move == bot_move:
        return "draw"

    # Bomb rules
    if user_move == "bomb" and bot_move == "bomb":
        return "draw"
    if user_move == "bomb":
        return "user"
    if bot_move == "bomb":
        return "bot"

    # Classic RPS rules
    beats = {
        "rock": "scissors",
        "scissors": "paper",
        "paper": "rock"
    }

    if beats[user_move] == bot_move:
        return "user"
    else:
        return "bot"


# ============================================================
# TOOL 3: STATE UPDATE
# ============================================================
# Mutates the game state after each round.
# Handles:
# - Round increment
# - Score updates
# - Bomb usage tracking
# - Game termination after 3 rounds
# ============================================================

def update_game_state(
    state: GameState,
    winner: Literal["user", "bot", "draw"],
    user_move: str,
    bot_move: str
) -> GameState:

    state.round_number += 1

    # Track bomb usage
    if user_move == "bomb":
        state.user_bomb_used = True
    if bot_move == "bomb":
        state.bot_bomb_used = True

    # Update scores
    if winner == "user":
        state.user_score += 1
    elif winner == "bot":
        state.bot_score += 1

    # Automatically end game after 3 rounds
    if state.round_number >= 3:
        state.game_over = True

    return state


# ============================================================
# BOT MOVE SELECTION
# ============================================================
# Simple strategy:
# - Random move
# - Bomb available only if not already used
# ============================================================

def choose_bot_move(state: GameState) -> str:
    possible_moves = ["rock", "paper", "scissors"]

    if not state.bot_bomb_used:
        possible_moves.append("bomb")

    return random.choice(possible_moves)


# ============================================================
# MAIN CONVERSATIONAL AGENT
# ============================================================

class RPSPlusAgent:
    def __init__(self):
        self.state = GameState()

    def explain_rules(self) -> str:
        return (
            "Welcome to Rock–Paper–Scissors–Plus!\n"
            "• Best of 3 rounds\n"
            "• Moves: rock, paper, scissors\n"
            "• Bomb beats everything (usable once)\n"
            "• Bomb vs bomb = draw\n"
            "• Invalid input loses the round\n"
        )

    def handle_user_turn(self, user_input: str) -> str:
        if self.state.game_over:
            return "The game has already ended."

        # Step 1: Validate user intent
        validation = validate_move(user_input, self.state.user_bomb_used)

        # Step 2: Bot chooses its move
        bot_move = choose_bot_move(self.state)

        # Step 3: Handle invalid input
        if not validation["valid"]:
            winner = "bot"
            explanation = f"Invalid move: {validation['reason']}"

            self.state = update_game_state(
                self.state,
                winner,
                user_move="invalid",
                bot_move=bot_move
            )
        else:
            user_move = validation["move"]
            winner = resolve_round(user_move, bot_move)

            self.state = update_game_state(
                self.state,
                winner,
                user_move,
                bot_move
            )

            if winner == "draw":
                explanation = "This round is a draw."
            elif winner == "user":
                explanation = "You win this round!"
            else:
                explanation = "Bot wins this round."

        # Step 4: Build user-facing response
        response = (
            f"\nRound {self.state.round_number}\n"
            f"Your move: {user_input}\n"
            f"Bot move: {bot_move}\n"
            f"Outcome: {explanation}\n"
            f"Score → You: {self.state.user_score} | Bot: {self.state.bot_score}\n"
        )

        # Step 5: End-of-game summary
        if self.state.game_over:
            response += "\nFinal Result: " + self.get_final_result()

        return response

    def get_final_result(self) -> str:
        if self.state.user_score > self.state.bot_score:
            return "You win the game 🎉"
        elif self.state.bot_score > self.state.user_score:
            return "Bot wins the game 🤖"
        else:
            return "The game ends in a draw 🤝"


# ============================================================
# SIMPLE CLI RUNNER
# ============================================================

if __name__ == "__main__":
    agent = RPSPlusAgent()
    print(agent.explain_rules())

    while not agent.state.game_over:
        user_input = input("Your move: ")
        print(agent.handle_user_turn(user_input))
