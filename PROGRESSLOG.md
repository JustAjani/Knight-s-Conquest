## Game Development Progress

## July 16, 2024
- **Player Movement:** Implemented player control using keyboard and mouse inputs.
- **Attack Mechanics:** Basic attack animations and mechanics for engaging enemies are functional.
- **Animations:** Player movements and attacks are fully animated.
- **Player Camera:** Camera follows the player, though some issues persist.
- **Basic Audio:** Basic audio playback is implemented.

## July 17, 2024
- **Enemy AI:** Basic enemy AI for attacking the player is implemented (enemies currently deal no damage).
- **Health Bar:** Health bar for the player is added.

## July 18, 2024
- **Bug Fixing:** Addressed issues from the previous day.
- **Audio Improvements:** Improved audio synchronization.
- **Enemy State Transition:** Enhanced enemy state transitions and fixed an issue where enemies would spin out of control at the game start by adding an idle state.
- **New Enemy:** Added a goblin enemy.
- **State Fix:** Fixed the transition between the goblin's attack1 and attack2.
- **New Enemy:** Introduced a mushroom-like enemy.

## July 19, 2024
- **Enemy AI Issues:** Continued resolving enemy AI bugs.
- **Mushroom Enemy Update:** Added dynamic sound effects for movement and attack.
- **Enemy AI Status:** Most bugs are fixed.
- **New Enemy:** Added a bat enemy.
- **New Enemy Status:** Bats have distinctive behaviors and sounds, though some bugs remain.
- **Gravity Class:** Developed with the help of ChatGPT (not yet implemented in the game mode, further changes planned).

## July 21, 2024
- **Gravity:** Tweaked gravity logic to affect both player and enemies.
- **Save and Load Game:** Preliminary implementation as a test for future checkpoints, with assistance from ChatGPT (for encryption).
- **Tile Loader + Collision:** Player can collide with tiles (not yet tested).

## July 24, 2024
- **State Machine Implementation:** Attempting to fix most of the spinning animation effects while switching through states. Works for the skeleton and goblin, but not for the mushroom and the flying eye.
- **Animations Fix:** Fixed movement animations broken by the state machine implementation.
- **Flip Direction Fix:** Added a delay to the flip trigger to prevent frequent direction changes causing the spinning effect.

## July 25, 2024
- **Refactoring:** Significant refactoring led to broken audio and animations for enemies.
- **AI States Fix:** Fixed the enemy AI animations and logic. Audio issues persist.
- **Audio Fix:** Addressed most audio issues, added threading to manage the queue, though some inconsistencies remain.

## July 26, 2024
- **Audio Fix:** Properly outputted respective audio (except for the player).
- **Animation Fix:** Fixed most animation issues (except for the skeleton enemy).
- **Audio Update:** Added a debounce system to prevent repeated audio triggers. However, this sometimes breaks the game over time.
- **Audio Fix:** Implemented error handling in `enqueue_sound()` to deal with null data, edited debounce system to prevent rapid channel creation.
- **Flying Eye State Manager:** Progressing slowly.

## July 27, 2024
- **Docstring Addition:** Added docstrings to files for improved readability and future reference.
- **Controller Compatibility:** Added support for PlayStation & Xbox controllers.
- **Improved Save State Manager:** Using Firebase to handle save and load state data.
- **More AI Work:** Attempted to fix the Flying Eye Enemy with limited success.

## July 29, 2024
- **SQLite Integration:** Created a SQLite database to store data locally.
- **SQLite & Firebase Synchronization:** Local save and cloud backup synchronization.
- **Delete Save Data:** Added function to delete game save data.
- **Asset Manager Tweak:** Made adjustments to asset management.
- **Game Saver Update:** Now saves enemy states.
- **Game Loop Tweak:** Improved error handling for clean termination instead of a white screen or unresponsive window.
- **Game Saver Update:** Game saves and loads the audio state.

## July 30, 2024
- **Skeleton Animation:** Fixed skeleton animation issues.
- **Enemy AI Ability Class:** Added a class for shooting projectiles when the enemy enters attack 3 (not yet tested).
- **New Enemy:** Added a fireworm.

## August 1, 2024
- **Refactoring Day:**
  - **Enemy Status:** Removed the Flying Eye Enemy, improved the Fire Worm enemy.
  - **Improving State Manager:** Enhanced responsiveness with added threading in each state class.
  - **Enemy Logic Update:** Simplified enemy logic, focusing on the `evaluate_combat_state(self, current_time, player)` to ensure more predictable and stable behavior.
  - **Performance Tracker:** Implemented FPS tracking for performance monitoring.
  - **Worm AI Tweak:** Added sound effects for the worm enemy.
  - **Ability Class Tweak:** Corrected minor mistakes and optimizations.

## August 3, 2024
- **Enemy AI Update:** I removed the `update_flip(self, player)` function in the enemy class because it was interuption the flip logic in other states. By centralizing the flip logic within each state and using consistent timing checks, conflicting flip commands are avoided and ensure that the enemy's behavior is more predictable and controlled.
- **Enemy Ai Update:** The enemy remebers the player last positon after exiting chase mode and patrols that area until the enemy is inrange
- **Enemy Ai Emotional State [Implemented not yet functional]:** A state that will affect both player and enemy on how they attack and respond to things example - Nuetral(blue), Fear(silver) and Anger(red).

- **Fear Triggers:**
  - Enemy witnesses the player defeating other enemies.
  - Isolation or being outnumbered.

- **Anger Triggers:**
  - Repeated attacks by the player.
  - Close proximity to the player for extended periods.
  - Damage to allies or significant environmental destruction caused by the player.

- **Enemy Ai Update:** I added a fleeing mechanic to the enemy ai

## August 13, 2024
- **Implementing of enemy damage animation:** Simply adding the animation to the `self.animation` Dictionary.
- **Integrated attack handling:** So far no damage is being delt just want to make sure the sword hit box renders properly and the enemy damage animation aswell which isn't working that well but it's something.
- **Simple debug system:** So I made a debug system...well chatgpt recommended it and I copied what it said so now I can see where the hitbox is printed if the enemy gets hit.
- **added a new state:** this will handle the hit animation and damage[not yet implement the damage that is].
- **noteworthy problem:** Hit box inconsistency which needs to be fixed also the audio class.
- **Improved attacked Handling:** will attack player only if it's in a specific range...[heavily considering ray tracing at this point]
- **Ray Tracing:** simulated a ray tracing feature like in 3d games and I'm getting better results

## August 14,2024
- **Ray Tracing Modification:** so i used multiple rays to get a wider attack area one slightly above, in the middle and in slightly below the player. 
- **Push Back Modification:** made sure the enemy can only be pushed backed only if they get attacked.
- **Modified the attack trigger:** so originally onced attacked the enemy would stay in the damaged state so I made recieving damage a higher prioty and i made sure the `enemy.attacked` flag is reset each time.
- **Modified the Damage State Duration:** The Damage state would last a long long while so I used python Time module to set the state to sleep 0.2 milliseconds, there were inconsitencies due to the thread so we had to calculate it with deltaTime.
- **Enemy Overlap:** Used Chatgpt to create a simple collision system to prevent enemies from overlapping.

## August 15,2024
- **Improving Enemy Overlap:** Spent couple hours trying to improve the logic enemy's will push each other away if they're too close however they're stuck in one place, interfering with the original movement logic.
- **Moving The Enemy Overlap logic to the Base Enemy Class:** This worked well the enemies don't overlap and they push each other away if they're in the way, same was done for the player.
- **Implementation of a Collision Detection Class:** Moved all the logic in it's seperate class making for more consistency between player and enemy. [Shout out chatgpt for the assitance], however this is affecting the flee state due to the inherent logic.
- **Edited Attack Handling:** So basically how the fleeing mechanic works is if the player postion is less than the `enemy_rect` or if only one enemy is avaliable the enemy would flee. However the attack handling Knocks back the enemy so that would trigger the flee slowly making the enemy_rect larger. [still Want the push back thou]
- **Improving Attack Handling Again:** Set KnockBack to be random so it wouldn't interfere with the flee logic, rather than pushing enemy each time the button is clicked.
- **Playing With Particles:** Made a particle based class with the help of chatgpt ofc big help explained it well.
- **Edited the `flee` function:** When the state was trigger an error in the terminal would appear not affecting the gameloop however the error was that i was comparing an list and an integer with the > sign, also when fixing this the surface was locked so I had to unlock it with a conditional check in the render.

## August 19,2024
- **Enemy Death Handling:** Enemy has an integrated health system, they have a death state and they can finally die!!! however the enemy death animation isn't triggered properly, which may lead to some inconsistencies.
- **Trying to get Enemy Death Animation to work:** Get some help with my original death class for the enemy however it seems like he's break dancing than dying.
- **Improved death state:** Has a flag that checks if the animation is complete which is done in a while loop, tracks how long it has been in that state plays the death animation then filters out the enemy out the list safely removing them from the list.
- **Refining StateManagement:** To prevent memory leaks and thread overhead I looked into threadpooling.[Help from Chagpt]
- **Refining Audio:** Using thread pool to handle tasks like enqueuing sounds and playing them, ensuring that I don't have to create an excessive number of threads for these operations.[Help from Chatgpt]
- **Improved Error Handling For classes:** Add error handling and exception for audio and state manager class.
- **Enemy Death Anim:** Death Animation fix sorta.

## August 20, 2024

- **StateManager Improved:** removed the thread pooling due to the currency system so I used a flag system instead, I also set a default state if the state the enemy is looking for doesn't exist. I also removed the delays in the statemachine so everything will run smoother, improved the state hierarchy.
- **Damage State:** Enemy death animation is now visible however damage animation isn't due to certain changes in the in the statemanager.

