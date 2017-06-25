       ######## The Cellcraft Project ########

## Needed packages

- check requirements.txt

## Installation
### Installation of Minecraft Client
- download client
- run client once with correct version (1.12)
- download forge installer (version 1.12) from http://files.minecraftforge.net/
- run forge installer and install client into minecraft folder (no change needed)

### Installation of Minecraft Server with RaspberryJamMod
- download forge installer (version 1.12) from http://files.minecraftforge.net/ (same then above)
- create a minecraft_server folder
- run forge installer and install server into the minecraft_server folder
- download from https://github.com/arpruss/raspberryjammod/releases the mods.zip
- unzip the mods.zip and copy the mods folder into the minecraft_server folder
- create a "mcpipy" in the minecraft_server folder
- run the forge-1.12-14.21.0.2359-universal.jar once
- edit the eula.txt and change false to true
- start the server running forge-1.12-14.21.0.2359-universal.jar again

### Testing of RaspberryJamMod
- download from https://github.com/arpruss/raspberryjammod/releases the python-scripts.zip
- unpack and copy the content of mcpipy into the mcpipy in the minecraft_server
- run forge-1.12-14.21.0.2359-universal.jar
- start the client
- choose Multiplayer
- choose Direct Connect
- add 0.0.0.0 as server adress and join server
- type: /py donut

### Starting the server with cellcraft
- copy the mcpi folder from the python-scripts.zip to the mcpipy folder
- clone cellcraft into the mcpi folder
- copy the cellpack.py from the cellcraft folder to the mcpipy folder
- enter the virtual enviroment
- start the server with cellcraft java -jar forge-1.12-14.21.0.2359-universal.jar

### Join the server
- start the client
- choose Multiplayer
- choose Direct Connect
- add 0.0.0.0 as server adress and join server
- type: /py cellcraft pdb 3J9U 2 4 -15 load

## Usage
  py cellcraft [pdb/cellpack] [PDBcode] <threshold> <blocksize> <horizontal_shift> [load/nolo]
- `py cellcraft` : mandatory
- `[pdb/cellpack]` : load pdb or cellpack structure (the later is not covered here)
- `[PDBcode]` : specify the PDB code (for pdb)
- `<threshold>` : minimum number of atoms found in grid cube to be filled
- `<blocksize>` : spacing of the grid in Angstroem
- `<horizontal_shift>` : horizontal shift of the structure in respect of the player position
- `[load/nolo]` :  load structure from database / take local copy
  (the latter is only possible if the same PDBid was processed before with the same threshold and blocksize)


## Contact
info@thecellcraftproject.org
