# Knight's Conquest

## Overview
"Knight's Conquest" is an action-adventure game inspired by the classic Castlevania series. It combines traditional platformer elements with innovative enemy AI and level design.

## Credits
- **Artist**: LuizMelo 

## Current Progress

### July 16, 2024
- **Player Movement**: Player can be controlled using keyboard and mouse inputs.
- **Attack Mechanics**: Basic attack animations and mechanics for engaging enemies are functional.
- **Animations**: Player movements and attacks are fully animated.
- **Player Camera**: Camera follows the player, though some issues persist.
- **Basic Audio**: Basic audio playback is implemented.

### July 17, 2024
- **Enemy AI**: Basic enemy AI for attacking the player is implemented (enemies currently deal no damage).
- **Health Bar**: Health bar for the player is added.

### July 18, 2024
- **Bug Fixing**: Addressed issues from the previous day.
- **Audio Improvements**: Worked on synchronizing audio better.
- **Enemy State Transition**: Enhanced enemy state transitions and fixed an issue where enemies would spin out of control at the game start by adding an idle state.
- **New Enemy**: Added a goblin enemy.
- **State Fix**: Fixed the transition between the goblin's attack1 and attack2.
- **New Enemy**: Introduced a mushroom-like enemy.

### July 19, 2024
- **Enemy AI Issues**: Continued resolving enemy AI bugs.
- **Mushroom Enemy Update**: Added dynamic sound effects for movement and attack.
- **Enemy AI Status**: Most bugs are fixed.
- **New Enemy**: Added a bat enemy.
- **New Enemy Status**: Bats have distinctive behaviors and sounds, though some bugs remain.
- **Gravity Class**: Developed with the help of ChatGPT (not yet implemented in the game mode, further changes planned).

### July 21, 2024
- **Gravity**: Tweaking gravity logic to affect both player and enemies.
- **Save and Load Game**: Preliminary implementation as a test for future checkpoints, with assistance from ChatGPT[For Encryption].
- **Tile Loader + Collision**: Player can collide with tiles [not yet tested]

### July 24, 2024
- **Implemented a state machine**: Hoping to fix most of the spinning animation effect while switching through states...works for skeleton and goblin. [No so much for the Mushroom and the Flying Eye]

## Objectives
The primary goals of this project are:
- **Understanding Particle Effects**: Enhancing knowledge of particle effects to improve the visual appeal of enemy attacks and player movements, and to create a more immersive and engaging gameplay experience.
- **Learning Enemy AI**: Developing and understanding the dynamics of enemy AI using Python.
- **Mastering Tiled**: Gaining proficiency in using the Tiled level editor to create engaging and visually appealing levels.

## Technologies Used
- **Programming Language**: Python
- **Level Design**: Tiled Level Editor
- **Game Engine**: Pygame

Feel free to contribute or suggest improvements!
