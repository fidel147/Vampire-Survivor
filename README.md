# Vampire Hunt

Vampire Hunt is a small top-down survival game built with Python, Pygame CE,
and Tiled maps. Survive the incoming enemies, aim with the mouse, and shoot
your way through the map.

## Requirements

- Python 3.10 or newer
- A graphical display and audio device
- The packages listed in [requirements.txt](requirements.txt)

The game assets are included in this repository. No external download is
needed after cloning.

## Installation

From the repository root, create a virtual environment and install the pinned
dependencies:

```sh
python3 -m venv .venv
.venv/bin/python -m pip install --upgrade pip
.venv/bin/python -m pip install -r requirements.txt
```

On Windows PowerShell, use the equivalent commands:

```powershell
py -m venv .venv
.venv\Scripts\python -m pip install --upgrade pip
.venv\Scripts\python -m pip install -r requirements.txt
```

## Start the game

```sh
.venv/bin/python code/main.py
```

On Windows PowerShell:

```powershell
.venv\Scripts\python code\main.py
```

The asset paths are resolved from the repository location, so the command can
also be launched from another working directory with an absolute path to
`code/main.py`.

## Controls

| Action | Input |
| --- | --- |
| Move | `W`, `A`, `S`, `D` or arrow keys |
| Aim | Mouse |
| Shoot | `Space` |
| Quit | `Escape` or close the window |

The player loses when an enemy collides with them. Enemies spawn continuously
from the positions defined in the Tiled map. Bullets disappear after their
configured lifetime, and defeated enemies remain briefly on screen before
being removed.

## Project structure

```text
audio/                 Sound effects and background music
code/main.py           Game loop, input, spawning, and collisions
code/player.py         Player movement, collision, and animation
code/sprites.py        Player weapon, bullets, enemies, and map sprites
code/groups.py         Camera offset and depth-aware sprite drawing
code/settings.py       Game configuration and asset paths
data/maps/             Tiled world map
data/tilesets/         Tiled tileset definitions
data/graphics/         Graphics referenced by the Tiled tilesets
images/                Player, weapon, and enemy animation frames
```

## Configuration

Gameplay values such as the window size, player speed, shooting cooldown,
enemy spawn interval, and asset locations are defined in
`code/settings.py`. The map's object layers provide the player start point,
enemy spawn points, map objects, and collision rectangles.

When editing the map in Tiled, keep the layer names used by the game:
`Ground`, `Objects`, `Collisions`, and `Entities`. The player entity must be
named `Player`; other entities are treated as enemy spawn points.

## Development checks

Compile the Python modules without starting the game:

```sh
python3 -m py_compile code/*.py
```

For a headless initialization check on Linux, use dummy SDL drivers:

```sh
SDL_VIDEODRIVER=dummy SDL_AUDIODRIVER=dummy \
	.venv/bin/python -c "import sys; sys.path.insert(0, 'code'); from main import Game; Game()"
```

The repository intentionally ignores `.venv/`, Python bytecode, editor files,
and local build or test output. Game assets, maps, and audio are versioned
because they are required to run the project.

## Current scope

This is a single-player prototype. It currently has no menu, save system,
score display, automated test suite, or packaged release build.
