# 🏰 Burgverlies (The Dungeon)
A 2D grid-based dungeon crawler built with Python and Pygame Zero. Navigate the dungeon, collect keys, and avoid the guards to find the exit. This project showcases the transition from script-based automation to object-oriented game logic.

🌟 Key Features
Grid-Based Movement: Precision movement system using a $16 \times 12$ raster grid.
Dynamic Guard AI: Guards utilize a basic "chase" logic, recalculating the path to the player every 0.5 seconds.
State Management: Fully implemented game states (Start, Playing, Win, Loss) with a restart mechanism.
Visual Polish: Randomized floor textures and animations for smooth transitions between tiles.

🛠️ Technical Deep Dive
The core of Burgverlies lies in the translation between the Logical Grid and the Visual Screen:
Coordinate Mapping:
  raster_koord(): Converts pixel positions to grid indices for collision logic.
  fenster_koord(): Converts grid indices back to pixels for rendering.
Collision System:
  The game uses an Axis-Aligned Bounding Box (AABB) logic mapped to a string-based MAP array.
  Walls ("W") act as solid boundaries, while the Door ("T") remains impassable until all Keys ("K") are collected.

🚀 How to PlayRequirements: 
Ensure you have Python and the pgzero library installed.
  Run:
    pip install pgzero
  
Assets: 
  Place your .png files in an images/ folder relative to the script. 
  Required assets: player, guard, key, wall, door, floor1, floor2, crack1, crack2.
  Run:
    pgzrun Burgverlies.py
    
🤝 Collaborative Design (The "Independent" Approach)

As an developer who is "independent by nature, but collaborative by design," I built this dungeon with the user’s experience in mind:
  Code Readability: 
    I’ve structured the code into distinct sections (Drawing, Logic, Setup) to make it easy for others to peer-review or extend.
  Diplomatic Difficulty: 
    The guard AI is balanced to be challenging but predictable. I value feedback on the game's difficulty—if the guards are too "relentless," let's discuss how to implement a line-of-sight system!
  Open for Partnership: 
    While I enjoy solving the logic puzzles of game development alone, I am eager to hear from designers or fellow coders on how to improve the "feel" of the game.
    
🗺️ Roadmap
  [ ] Add a "Fog of War" system to hide parts of the map.
  [ ] Implement a step counter (Highscore system).
  [ ] Create multiple levels by loading different MAP arrays.
