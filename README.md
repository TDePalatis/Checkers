# Checkers Game Engine ♟️  
A Python implementation of the Checkers rules engine, including kings, triple kings, move validation, and full unit tests.

## 👋 About This Project
This project is a complete, object-oriented Checkers game engine that I built and later refined to strengthen my skills in Python, rule-based systems, and test-driven design. It simulates the internal logic of a playable Checkers match—tracking turns, validating moves, enforcing capture rules, handling promotions, and determining when the game ends.

Although this began as part of my coursework at Oregon State University, I have since cleaned it up, documented it, and expanded the testing to serve as a solid portfolio piece that demonstrates how I think through game logic, data modeling, and error handling.

## 🚀 What This Engine Can Do
### Game Logic
- Turn order is enforced (Black always moves first).
- All moves must be diagonal and legal.
- Supports capturing, forced captures, and multi-jump sequences.
- Implements king and triple-king promotions with their movement rules.
- Detects when the game ends and identifies the winner.

### Rule Enforcement & Error Handling
I created several custom exceptions to make invalid states explicit:

| Exception | Trigger |
|----------|----------|
| `OutofTurn` | A player moves when it isn’t their turn |
| `InvalidPlayer` | Unknown player or duplicate name |
| `InvalidSquare` | Off-board or invalid reference |
| `InvalidMove` | Illegal movement or capture attempt |

### Object-Oriented Structure
- The **`Checkers`** class manages board state, turn logic, move validation, and promotions.
- The **`Player`** class tracks king counts, triple-king counts, and captured pieces.

### Unit Tests Included
A full `unittest` suite (`CheckersGameTester.py`) validates:
- piece creation and retrieval  
- legal and illegal moves  
- capturing and multi-captures  
- king promotion and backward moves  
- exception behavior  
- game progression  

This helps ensure correctness and also shows how I approach writing automated tests.

---

## 🧠 Skills Demonstrated
This project highlights several core engineering skills I value:

- Python OOP design  
- Rule-based engine development  
- State management  
- Custom exception handling  
- Defensive programming  
- Unit testing with `unittest`  
- Writing clear, maintainable, well-documented code  

These are the same skills used heavily in backend engineering, QA automation, game logic systems, and state-driven applications.

---

## 📂 File Structure

CheckersGame/
├── CheckersGame.py # Game logic and classes
├── CheckersGameTester.py # Automated unit tests
└── README.md # Project documentation

---

## 🧩 Quick Example

```python
from CheckersGame import Checkers

game = Checkers()

black = game.create_player("Trevor", "Black")
white = game.create_player("Alice", "White")

# Black moves first
game.play_game("Trevor", (5, 0), (4, 1))

# White moves
game.play_game("Alice", (2, 1), (3, 0))

# Inspect the board
game.print_board()

# Check status
print(game.game_winner())  # "Game has not ended"
🧪 Running the Tests
python -m unittest CheckersGameTester.py
🏁 Final Thoughts
I’m proud of this project because it reflects how I approach problem-solving: breaking down a complex set of rules, enforcing them with clear logic, and validating behavior through automated testing.
If you’d like to chat about the implementation or discuss any part of the logic, feel free to reach out!

👋 Connect With Me
LinkedIn: https://www.linkedin.com/in/trevor-depalatis/
GitHub: https://github.com/TDePalatis