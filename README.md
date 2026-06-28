# ♟️ Bonnyrigg Chess Engine

A fully-featured desktop chess engine developed in **Python** using **Pygame** for the HSC Software Engineering course.

The project implements the official rules of chess and includes an AI opponent powered by the **Minimax algorithm** with **Alpha-Beta pruning**.

---

## Features

### Gameplay
- Player vs Player
- Player vs AI
- AI vs AI
- Drag-and-drop piece movement
- Interactive graphical interface
- Multiple board themes
- Fullscreen support
- Animated main menu

### Chess Rules
- Legal move validation
- Check detection
- Checkmate detection
- Stalemate detection
- Castling
- En Passant
- Pawn Promotion
- Draw by Insufficient Material

### Artificial Intelligence
- Minimax Search
- Alpha-Beta Pruning
- Material Evaluation
- Piece Development Evaluation
- Centre Control Evaluation
- King Safety Evaluation
- Bishop Pair Bonus
- Capture Prioritisation

---

## Technologies Used

- Python 3.x
- Pygame
- Object-Oriented Programming
- Minimax Algorithm
- Alpha-Beta Pruning
- Git
- GitHub

---

## Project Structure

```
Bonnyrigg-Chess-Engine/
│
├── src/
│   ├── main.py
│   ├── game.py
│   ├── board.py
│   ├── ai.py
│   ├── menu.py
│   ├── piece.py
│   ├── pawn.py
│   ├── knight.py
│   ├── bishop.py
│   ├── rook.py
│   ├── queen.py
│   ├── king.py
│   ├── square.py
│   ├── move.py
│   ├── dragger.py
│   ├── config.py
│   ├── const.py
│   ├── sound.py
│   └── theme.py
│
├── assets/
│
├── docs/
│
├── README.md
└── requirements.txt
```

---

## Installation

### 1. Clone the repository

```bash
git clone https://github.com/YourUsername/Bonnyrigg-Chess-Engine.git
```

### 2. Open the project

```bash
cd Bonnyrigg-Chess-Engine
```

### 3. Install dependencies

```bash
pip install pygame
```

Or if using a requirements file:

```bash
pip install -r requirements.txt
```

---

## Running the Program

Navigate to the source folder and run:

```bash
python main.py
```

---

## Controls

| Action | Control |
|---------|---------|
| Move Piece | Drag and Drop |
| Select Menu Option | Arrow Keys |
| Confirm Selection | Enter |
| Change Theme | T |
| Reset Game | R |
| Toggle Fullscreen | F11 *(if enabled)* |
| Quit | Close Window |

---

## Artificial Intelligence

The AI evaluates legal moves using the **Minimax algorithm** with **Alpha-Beta pruning**.

Board evaluation considers:

- Material balance
- Piece development
- Centre control
- King safety
- Bishop pair
- Castling
- Pawn advancement
- Tactical opportunities

---

## Future Improvements

- Multiple AI difficulty levels
- Opening book
- Endgame tablebases
- Undo / Redo
- Save and Load games
- PGN Import / Export
- Chess Clock
- Tournament Mode
- Online Multiplayer
- Stockfish Integration
- Move History
- Position Analysis

---

Requirements
Software
Python 3.12 or newer
Visual Studio Code (recommended)
Git (optional, for version control)
Python Package

Install the required library before running the project:

pip install pygame
Built-in Python Modules

The following modules are included with Python and do not require installation:

copy
random
os
sys
Project Assets

The following folders and files must remain in the project directory:

assets/images/imgs-80px/
assets/images/imgs-128px/
assets/sounds/move.wav
assets/sounds/capture.wav
Hardware Requirements
Windows 10/11, macOS, or Linux
4 GB RAM minimum (8 GB recommended)
Keyboard and mouse
250 MB available storage
Display resolution of at least 800 × 800
Running the Program

Open a terminal in the project folder and run:

python main.py

or

py main.py

---

## Testing

The project has been tested for:

- Legal move generation
- Check
- Checkmate
- Stalemate
- Castling
- En Passant
- Pawn Promotion
- Draw by Insufficient Material
- AI move generation
- Player vs Player
- Player vs AI
- AI vs AI

---

## Software Engineering Concepts

This project demonstrates:
- Event-Driven Programming
- Artificial Intelligence
- Search Algorithms
- Software Testing
- Agile Development
- Version Control using Git

---

## Author

**Allan Luong**

HSC Software Engineering Major Project

Bonnyrigg High School

---

#Copy Write 
Code was orignally Made by Coding Sport
But code was edited to include AI
Video Link: https://www.youtube.com/watch?v=OpL0Gcfn4B4
