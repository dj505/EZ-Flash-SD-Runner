# EZ Flash SD Runner
Easily boot files from an EZ Flash Omega SD card in an emulator, and copy the save file back to the card afterwards.
This is a very basic and unoptimized project I made in my spare time - it'll be largely unsupported, and likely won't be updated much. Pull requests are okay, though.

This should support the original kernel's save file directory, as well as the slightly different directory used by custom kernels such as Simple by Sterophonick.

# Instructions
1. Grab an emulator (mGBA or VisualBoyAdvance recommended)
2. Extract the emulator somewhere easily accessible, ideally in a directory alongside main.py
3. Rename `example_settings.ini` to `setings.ini`, and point `emulator_path` to the emulator's executable
  - eg. `emulator_path=mgba/mGBA.exe`
  - for Mac/Linux users, if you've installed an emulator via a package manager, the package name *should* work, maybe
4. Insert your EZ Flash Omega's SD card into your PC
5. Run `main.py`
6. Select your game
7. ???
8. Profit

After exiting the emulator, there will be a popup asking if you'd like to clear the copied ROM and save data.
This popup only refers to the local copies of the game ROM and save in the `rom` folder. At this point, the save data has already been copied back to your SD card, so answering "Yes" to this will not delete your save data - it just serves to prevent clutter.

# Requirements
* Python 3
* An emulator (VisualBoyAdvance and mGBA work well)
