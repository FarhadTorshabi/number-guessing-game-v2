# 🎯 Number Guessing Game v2

A CLI-based multiplayer number guessing game built with Python.

This version introduces scalable multiplayer support, persistent score tracking, improved architecture, and clean modular design.

---

## 🚀 Features

- 🎮 Multiple players supported
- 💾 Persistent scoreboard (JSON-based storage)
- 🔥 Hot & Cold hints
- 🎚 Difficulty levels (easy / medium / hard)
- 🏆 Best score tracking per player
- 📊 Win/Loss statistics
- 🧠 Clean modular design with separated logic layers
- 📝 Type hints and docstrings

---

## 🏗 Architecture Overview

The project is structured into logical layers:

- **Game Logic Layer** – handles guessing mechanics and hints
- **Persistence Layer** – loads and saves scoreboard data
- **User Interface Layer** – CLI interaction

The scoreboard is designed as a scalable dictionary structure:

```json
{
  "PlayerName": {
    "games": 0,
    "wins": 0,
    "losses": 0,
    "best_score": null
  }
}
