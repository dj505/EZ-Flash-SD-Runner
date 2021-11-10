# EZ Flash SD Runner
Easily boot files from an EZ Flash Omega SD card in an emulator, and copy the save file back to the card afterwards.
This is a very basic and unoptimized project I made in my spare time - it'll be largely unsupported, and likely won't be updated much. Pull requests are okay, though.

# Instructions
1. Install VisualBoyAdvance
* Windows users:
  - Extract a copy of VBA so that VisualBoyAdvance.exe is present alongside the script
* Linux users:
  - The script attempts to run `VisualBoyAdvance-m`. For Arch users, this package is available via `pacman -s vbam-wx`. Feel free to modify this for use with another emulator or a different package, such as `vbam-sdl`.
* Mac users:
  - ¯\\\_(ツ)_/¯

2. Insert your EZ Flash Omega's SD card into your PC
3. Run `main.py`
4. Select your game
5. ???
6. Profit

After exiting the emulator, there will be a popup asking if you'd like to clear the copied ROM and save data.
This popup only refers to the local copies of the game ROM and save in the `rom` folder. At this point, the save data has already been copied back to your SD card, so answering "Yes" to this will not delete your save data - it just serves to prevent clutter.

# Requirements
Python 3
A copy of VisualBoyAdvance
