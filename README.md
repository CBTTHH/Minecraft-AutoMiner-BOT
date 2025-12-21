# Minecraft Auto-Miner Bot (v1.0) 🤖

> **Note:**  ⚠️  
> This branch has **version 1.0 (stable)** of the Minecraft Auto-Miner agent.  
> Active development for **version 2.0 (in process)** is happening on `v2-dev` branch.

---

## Overview 📑
The Minecraft Auto-Miner Bot is an automation system built in Python using the
MineScript library. The script autonomously takes the player from the surface
down to the mining level (Y = -58), handles hazards situations, and performs automated mining
behavior with almost no user intervention.

This project focuses on applying data structures, algorithms, and logic in a interactive real-time environment.

---

## Features ⚙️
- Automatic descent from surface level down to Y-level -58
- Hazard detection:
  - Water (prevent drowning)
  - Open caves (prevent fall damage)
  - Lava at the bottom (prevent burning)
- Autonomous movement and block interaction
- Hotbar monitoring and management
- Tool switching based on block type
- Continuous environment awareness

---

## Algorithms & Computer Science Concepts 💻
This project was designed to put into practice real application of core CS concepts:

- **Data Structures**
  - OOP for player state tracking
  - Hash maps and sets for hotbar and searching variables
  - Queues and lists for movement logic

- **Algorithms**
  - Graph traversal concepts DFS for diamond searching
  - Rule based decision for hazard handling

- **Software Design**
  - State based logic for player behavior
  - Modular functions for movement, mining, and hazard handling
 
---

## Architecture 🧩
Minecraft Auto-Miner Bot v1.0 follows a functional and event-driven structure:

- PlayerTracker class manages player position, velocity, rotation and tool selection
- Main control loop checks player state
- Independent functions handle:
  - Descending logic
  - Hazard detection
  - Hotbar checks
- Real-time checks allow the bot to adapt to unexpected situations
  (e.g., falling into water or encountering huge caves)

This version focuses on functionality and correctness.  
Version 2.0 focuses on architectural improvements, better awareness handling, faster diamond searching, and bugs fixes.

---

## Video Explanation 🎥 
I created a video explaining how the bot works, the logic behind its behavior, and how to set it put:  
  
🔗 [YouTube Video]: https://youtu.be/IdFy5w9tKBE

---

## How to Run ⏯️
### Installation Requirements
- Python 3.13 or 3.14
- MineScript mod [Download Link] (https://modrinth.com/mod/minescript)
- mod.py (inside minescript folder)

Check video explanation for correct installation

### Run
- Inside minecraft, set pickaxe in slot 3, shovel in slot 4, water bucket in slot 5, 
and blocks (cobble deepslate preferable) in slot 9.  
- Type in the chat "\mod" (start bot)
- Type in the chat "\killjob 1" (stop bot)















