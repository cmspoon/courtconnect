# 🏀 courtconnect

courtconnect is a graph traversal engine and terminal game suite that connects NBA players across league history through mutual teammates.

---

## Game Modes

* **CourtConnection (`courtconnector.py`)**: Finds the shortest teammate chain between any two players
* **Three-Man Weave (`courtconnector.py`)**: Connects three players in a continuous relay (Player A → Player B → Player C)
* **Journeyman (`journeyman.py`)**: Given a start and target player, guess intermediate teammates to connect them

---

## Installation & Setup

1. **Clone the repository:**
   ```bash
   git clone [https://github.com/cmspoon/courtconnect.git](https://github.com/cmspoon/courtconnect.git)
   cd courtconnect
   ```

2. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

---

## Usage

* **Run Standard Modes (CourtConnection & Three-Man Weave):**
  ```bash
  python courtconnector.py
  ```

* **Run Journeyman:**
  ```bash
  python journeyman.py
  ```

* **Run Test Suite:**
  ```bash
  python -m pytest tests/ -v
  ```

---

## Project Structure

```text
courtconnect/
├── courtconnector.py          # Graph builder, BFS engine, and name resolution
├── journeyman.py              # Journeyman game state machine
├── graph.py                   # PyVis + NetworkX graph generator
├── nba_players.csv            # NBA roster dataset
├── requirements.txt           # Project dependencies
├── tests/
│   ├── test_courtconnect.py   # Two-player path unit tests
│   ├── test_threemanweave.py  # Three-player path unit tests
│   ├── players1.csv           # Test dataset
│   └── players2.csv           # Test dataset
└── .gitignore                 # Ignore files
```