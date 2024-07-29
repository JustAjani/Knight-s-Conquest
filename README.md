# Knight's Conquest

## Overview
"Knight's Conquest" is an action-adventure game inspired by the classic Castlevania series. It combines traditional platformer elements with innovative enemy AI and level design.

## Credits
- **Artist**: LuizMelo 

## Current Progress

### July 16, 2024
- **Player Movement**: Player control using keyboard and mouse inputs.
- **Attack Mechanics**: Basic attack animations and mechanics for engaging enemies are functional.
- **Animations**: Player movements and attacks are fully animated.
- **Player Camera**: Camera follows the player, though some issues persist.
- **Basic Audio**: Basic audio playback is implemented.

### July 17, 2024
- **Enemy AI**: Basic enemy AI for attacking the player is implemented (enemies currently deal no damage).
- **Health Bar**: Health bar for the player is added.

### July 18, 2024
- **Bug Fixing**: Addressed issues from the previous day.
- **Audio Improvements**: Improved audio synchronization.
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
- **Gravity**: Tweaked gravity logic to affect both player and enemies.
- **Save and Load Game**: Preliminary implementation as a test for future checkpoints, with assistance from ChatGPT (for encryption).
- **Tile Loader + Collision**: Player can collide with tiles (not yet tested).

### July 24, 2024
- **State Machine Implementation**: Attempting to fix most of the spinning animation effects while switching through states. Works for the skeleton and goblin, but not for the mushroom and the flying eye.
- **Animations Fix**: Fixed movement animations broken by the state machine implementation.
- **Flip Direction Fix**: Added a delay to the flip trigger to prevent frequent direction changes causing the spinning effect.

### July 25, 2024
- **Refactoring**: Significant refactoring led to broken audio and animations for enemies.
- **AI States Fix**: Fixed the enemy AI animations and logic. Audio issues persist.
- **Audio Fix**: Addressed most audio issues, added threading to manage the queue, though some inconsistencies remain.

### July 26, 2024
- **Audio Fix**: Properly outputted respective audio (except for the player).
- **Animation Fix**: Fixed most animation issues (except for the skeleton enemy).
- **Audio Update**: Added a debounce system to prevent repeated audio triggers. However, this sometimes breaks the game over time.
- **Audio Fix**: Implemented error handling in enqueue_sound() to deal with null data, edited debounce system to prevent rapid channel creation.
- **Attempting to fix Flying Eye State Manager**: it's comming along slowly...to slow to be honest

### July 27, 2024
- **added docstring to files**: Trying to improve readility also for future me to remember what each of these functions do.
- **controller compatibility**: PlayStation & Xbox 
- **Improved Save State Manager**: Using Firebase to handle save and load state data.
- **More AI work**: Attempting to Fix the Flying Eye Enemy...not comming along good.

### July 29,2024
- **Sqlite integration**: I made a sqlite datbase to store data locally
- **Sqlite N Firebase Syncronization**: Save the game locally and backs it up on the cloud
- **Delete Save Data**: Function to delete the game save added.


## Objectives
The primary goals of this project are:
- **Understanding Particle Effects**: Enhance knowledge of particle effects to improve the visual appeal of enemy attacks and player movements, creating a more immersive gameplay experience.
- **Learning Enemy AI**: Develop and understand the dynamics of enemy AI using Python.
- **Mastering Tiled**: Gain proficiency in using the Tiled level editor to create engaging and visually appealing levels.

## Technologies Used
- **Programming Language**: Python
- **Level Design**: Tiled Level Editor
- **Game Engine**: Pygame

Feel free to contribute or suggest improvements!