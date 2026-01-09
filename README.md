# Minecraft Auto-Miner Bot (v2.0) 

> **Note:**   
> This branch contains **version 2.0**, a major architectural refactor of the project.  
> The stable, fully working **version (v1.0)** is available on the **main** branch.

--- 

## System Architecture

![Architecture Diagram](bot\docs\ArchitectureDiagram.drawio.svg)  
This diagram shows the separation between high-level systems (modes)
and low-level systems (core). Modes decide what the player do, while core systems
execution interact with the MineScript API.

---

## Overview 
**Version 2.0** is a full architectural redesign of the original Minecraft Auto-Miner Bot.  
This version is not only have more features; it focuses on improving clarity, scalability, testability, and
performance reasoning.

The project transitions from a single messy and compacted script (`mod.py`) to a modular, system oriented
bot framework, inspired by real world game AI, robotics, and software engineering systems.

---

## From Monolithic Script to Modular System

### Before (v1.0 — mod.py)
- One large file containing:
  - player tracking
  - movement
  - safety logic
  - ore searching
  - decision-making
  - mining
  - mode control
- Logic tightly coupled
- Difficult to debug or test
- Hard to reuse or extend functionality

### Now (v2.0 — `bot/`)
bot/  
├── core/        # Low-level systems  
├── modes/       # High-level systems  
├── test/        # Isolated test scripts  
└── main.py      # Entry point  

### Why this matters
- Each component has one responsibility
- Systems can be modified or replaced independently
- Mirrors real-world projects architectures
- Enables better experimentation and optimization

---

## Separation of Responsibilities

### Low-Level Systems (`core/`)
Low-level systems are how actions individual actions, not what the bot decides to do in the execution.
| File                 | Responsibility                                                |
| -------------------- | --------------------------------------------------------------|
| `player.py`          | Player state tracking (health, position, velocity, rotation)  |
| `movement.py`        | Movement primitives (center, descend, move, stop, unstuck)    |
| `safety.py`          | Awareness behaviors (water, lava, falling)                    |
| `searching.py`       | Ore detection and clustering                                  |
| `decision.py`        | Cluster scoring and priority selection                        |
| `mining.py`          | Mining execution                                              |
| `constants.py`       | Physics, thresholds, timings, slots, etc.                     |

- Reusable across multiple behaviors
- Enables isolation testing

---

## High-Level systems (`modes/`)
Modes are what the bot is trying to accomplish after execution, using the core systems.

| File            | Purpose                                                            |
| --------------- | -------------------------------------------------------------------|
| `descend.py`    | Safely mine down to target Y (Y-level -58 is the default value)    |
| `scan_only.py`  | Scan ores without mining (return diamonds coords and best cluster) |
| `auto_miner.py` | Full autonomous mining loop (descend, scan, and mine)              |

### Why this matters
- Modes are changeable depending on the user needs
- Behavior changes don’t affect low-level systems
- Better structure and organization

---

## Explicit Execution Flow
### Before
- Execution happened implicitly inside mod.py
- Hard to understand control flow
- Tightly coupled logic (different parts of a system are highly dependent on each other's)

### Now
- Explicit entry points  
- main.py or test scripts decide what to run independently
- Clear start -> behavior -> finish flow

Example:  

`import bot.modes.descend as descend`  
`  descend.run()`

This makes the system easier to reason about, debug, and extend.

---

## Testability Added (test/ Folder)
New capabilities:
- Run partial systems without full automation
- Debug player tracking independently
- Easier debugging of low-level systems
- Compare old vs new approaches safely

This was **not** possible with the v1.0 monolithic design.

---

## Centralized Constants & Physics Tuning
### Before
- Magic numbers scattered across files
- Unsafe tuning
- Hard to reason about physics behavior

### Now (`core/constants.py`)
All parameters are documented and centralized:
- Tick timing
- Physics thresholds
- Yaw/pitch values
- Inventory slots
- Mining parameters

Example:  
`FALLING_Y_VEL = (-0.6, -3.92)`  
`STOP_Y_LEVEL = -58`  
`MAX_CENTER_OFFSET = (0.01, 0.017)`  

### Benefits
- Safe experimentation
- Easier changing
- Cleaner logic everywhere

---

## Background Player Tracking System
### Before
- Player state queried inline
- Repeated API calls
- Mixed with decision logic

### Now 
- Maintains:
  - health
  - position
  - velocity
  - yaw
  - tool state
- Other systems read, not query
- Auto-stop upon detecting dangerous situations (enemies, lava, low health)

This design has characteristics:  
- Game engines
- Entity Component System (ECS) architectures

---

## Performance Reasoning Improvements
This v2.0 has faster algorithms and enables performance understanding:
- Decisions are data-driven
  - uses shell / frontier expansion algorithm
  - instead of re-checking everything, explore the new boundary between known and unknown space
- Optimization is targeted
  - cache-friendly
  - no repeats

Optimization focuses on reducing loop calls - went from `O(n^3)` to `O(number of blocks checked)`  
This way of reasoning is better than v1.0.

---

## Designed for Future Growth
This architecture enables future additions such as:  
- Pathfinding systems (**A***)
- Memory allocation of blocks of data directly from Minecraft
- Behavior trees
- ML-based decision scoring

---

## Summary
**Version 2.0** replaces the original `mod.py` with a modular bot architecture.  
Low-level systems handle individual actions such as states, movement, safety, and decision-making, while high-level
systems define behavior.  

This refactor prioritizes clarity, extensibility, testability, and performance logic, laying on AI-driven automation.  

---

## Author
CBTTHH  
Computer Science student  
GitHub: https://github.com/CBTTHH  
YouTube: https://www.youtube.com/@CBTTHH  








