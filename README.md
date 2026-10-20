# Mega Man Remake

A 2D platformer inspired by Capcom's *Mega Man*, built in **Python** with **Pygame**. Created as my coursework (NEA) for **OCR A Level Computer Science**.
Atained an A* (67/80)


## Features

- Side-scrolling platforming with a controllable player character
- Shooting mechanic with projectiles (`bullet.py`)
- Enemies and a boss fight (`enemy.py`, `boss.py`)
- Collectable items and pickups (`items.py`)
- Multiple levels built from walls and platforms (`levels.py`, `wall.py`, `platform_1.py`)
- Scrolling camera that follows the player (`camera.py`)
- Custom collision detection (`collisions.py`)
- Game state management, e.g. menu, playing, game over (`game_states.py`)
- On-screen UI such as health display (`ui.py`)
- Checkpoint / level-end flag (`flag.py`)


## Requirements

- Python 3.[X] or newer
- [Pygame](https://www.pygame.org/)

## Installation and Running

1. Clone the repository:
   ```bash
   git clone https://github.com/Niel-Tailor/A-level-OCR-NEA-Project.git
   cd A-level-OCR-NEA-Project
   ```
2. Install Pygame:
   ```bash
   pip install pygame
   ```
3. Run the game:
   ```bash
   python Main.py
   ```

## Controls

| Action | Key |
| ------ | --- |
| Move left / right |  A / D or ← / →|
| Jump | w |
| Shoot | spacebar |
| Pause / Quit |  Esc |


## Project Structure

| File | Purpose |
| ---- | ------- |
| `Main.py` | Entry point and main game loop |
| `settings.py` | Game constants and configuration |
| `game_states.py` | Handles menus and the different game states |
| `game_drawings.py` | Rendering and drawing routines |
| `player.py` | Player character logic, movement and input |
| `enemy.py` | Enemy behaviour |
| `boss.py` | Boss behaviour and attack patterns |
| `bullet.py` | Projectile logic |
| `items.py` | Collectables and pickups |
| `levels.py` | Level layouts and loading |
| `wall.py`, `platform_1.py` | Level geometry |
| `collisions.py` | Collision detection and response |
| `camera.py` | Scrolling camera |
| `background.py` | Background rendering |
| `flag.py` | Checkpoint / level-complete flag |
| `ui.py` | HUD and interface elements |
| `IMG/` | Sprites and image assets |

## What I Learned

I learnt the foundations of pygame and learnt how to implement them into a fully working game that allowed me to understand how to code 

## Known Issues / Future Improvements

Making the boss battle more intense and making it so the boss is stronger 

## Credits

- Built with [Pygame](https://www.pygame.org/)
- *Mega Man* is © Capcom
- [Credit any sprite, music or tutorial sources you used here]

## Author

**Niel Tailor** · [GitHub](https://github.com/Niel-Tailor)