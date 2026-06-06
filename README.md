# Minecraft Auto-Miner Bot (v2.0)

> **Note**
> This branch contains **release v2.0**, a major architectural refactor of the project.  
> The old, stable and fully working **version (v1.0)** is available on the **release v1.0** branch.

---

## Overview

The **Minecraft Auto-Miner Bot** is a fully autonomous mining bot built on top of the **MineScript** mod.
It is designed to safely and efficiently mine resources underground while reacting to hazards such as lava,
hostile entities, low health, or movement stalls.

This project focuses on:

* Reliability during long mining sessions
* Clear separation between decision-making and execution
* Safe automation with automatic recovery and restart logic

The bot is modular, extensible, and designed similarly to real-world robotics and game AI systems.

---

## Requirements

* Minecraft (Fabric / Forge / NeoForge)
* **MineScript 4.0+**
* Python 3.9-3.x

MineScript can be downloaded from:

* [https://modrinth.com/mod/minescript](https://modrinth.com/mod/minescript)
* [https://www.curseforge.com/minecraft/mc-mods/minescript](https://www.curseforge.com/minecraft/mc-mods/minescript)

---

## Installation

1. Install **MineScript** for your Minecraft version
2. Launch Minecraft once to generate the `minescript` folder
3. Copy this [/bot](/bot) folder into:

   ```
   # Before
   .minecraft/minescript/

   # After
   .minecraft/minescript/bot
   ```
4. Ensure the folder structure matches the project layout

---

## Usage

### Start the Bot

From the Minecraft chat, type:

```
\bot\main
```

### Available Commands  

Type these commands in chat:  
```
.bot <mode>      # Commands usage
```

```
.bot auto        # Start full autonomous mining
.bot descend     # Only descend to target Y-level
.bot scan        # Scan ores without mining
.bot restart     # Restart the bot safely
.bot stop        # Stop current bot jobs
.bot stop all    # Stop all MineScript jobs including main
.bot help        # Show help commands
```

---

## Notes & Warnings

* Designed for **single-player or controlled environments**
* Use at your own risk on multiplayer servers
* Automatic safety logic may interrupt/stop mining when hazards are detected

---

## System Architecture

![Architecture Diagram](bot/docs/ArchitectureDiagram.drawio.svg)

The architecture is split into two layers:

* **Core systems**: low-level execution and sensing
* **Modes**: high-level behaviors composed from core systems

---

## Features

### Autonomous Mining

* Automatically descends to a target Y-level (default: **Y = -58**)
* Scans for nearby ore clusters
* Prioritizes and mines the best reachable cluster
* Repeats the process indefinitely

### Safety & Hazard Detection

* Lava detection in the surrounding area
* Hostile entity detection
* Health monitoring
* Tool and weapon state detection
* Automatic shutdown or recovery when danger is detected

### Stuck Detection & Recovery

* Detects lack of positional progress over time
* Differentiates between being stuck and slow mining
* Attempts local recovery before restarting
* Automatically restarts the bot if recovery fails

### Modular Command System

* Chat-based command interface (`.bot <mode>`)
* Run, stop, or restart modes without restarting Minecraft
* Supports isolated testing modes

---

## Algorithms & Techniques

### Shell / Frontier Expansion Search

Instead of rescanning entire regions repeatedly, the bot explores only the boundary between known and unknown blocks.
This significantly reduces redundant checks and improves performance.

### Ore Clustering

Detected ore blocks are grouped into clusters based on spatial proximity.
Clusters are scored and prioritized instead of mining single blocks blindly.

### Reachability Filtering

Before committing to a cluster, the bot verifies that it is physically reachable
based on current terrain and player position.

### Path Mining (unsing A* algorithm)

The bot mines a clear path toward the target cluster, ensuring:

* Stable footing
* Proper floor placement
* Centered player movement

### Autonomous Restart Logic

If the bot becomes irrecoverably stuck or encounters unsafe conditions,
it safely shuts down current jobs and restarts a fresh execution cycle.

---

## Project Structure

```
bot/
├── core/        # Low-level systems (movement, safety, mining, decision)
├── modes/       # High-level behaviors (auto, descend, scan)
├── test/        # Isolated test scripts
├── docs/        # Architecture diagrams
└── main.py      # Entry point
```

### Core Systems (`bot/core`)

| File               | Responsibility                                            |
| ------------------ | --------------------------------------------------------- |
| `player.py`        | Player state tracking (position, velocity, health, tools) |
| `movement.py`      | Movement primitives and path execution                    |
| `mining.py`        | Block breaking and cluster mining                         |
| `decision.py`      | Cluster scoring and selection                             |
| `safety_mining.py` | Hazard handling and emergency logic                       |
| `constants.py`     | Physics, timings, thresholds                              |

### Modes (`bot/modes`)

| Mode      | Description                                   |
| --------- | --------------------------------------------- |
| `descend` | Safely mines down to target Y-level           |
| `scan`    | Scans and reports ore clusters without mining |
| `auto`    | Fully autonomous mining loop                  |

---

## Author  

**SH1FTEDWASTAKEN**  
Computer Science student  
GitHub: [https://github.com/sh1ftedwastaken](https://github.com/sh1ftedwastaken)  
YouTube: [https://www.youtube.com/@sh1ftedwastaken](https://www.youtube.com/@sh1ftedwastaken)  

Making projects just for fun! :D

