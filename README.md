       ######## The Cellcraft Project ########


### Setup your computer for using Cellcraft

#### Setup your python environment

** Linux Setup
```
curl -L https://raw.githubusercontent.com/pyenv/pyenv-installer/master/bin/pyenv-installer | bash
pyenv update
echo 'export PATH="$HOME/.pyenv/bin:$PATH"' >> ~/.bashrc
echo 'eval "$(pyenv init -)"' >> ~/.bashrc
echo 'eval "$(pyenv virtualenv-init -)"' >> ~/.bashrc
source ~/.bashrc
pyenv install 3.6.0

pyenv global 3.6.0
source ~/.bashrc
```

** Mac OX Setup
```
brew update
brew install pyenv
brew install pyenv-virtualenv
echo 'eval "$(pyenv init -)"' >> ~/.bash_profile
source ~/.bash_profile
pyenv install 3.6.0

pyenv global 3.6.0
source ~/.bash_profile
```

* To create and activate the python environment
```
pyenv virtualenv cellcraft
pyenv activate cellcraft
```

* For desactivaton of the python environment run:
```
pyenv deactivate
```

##### Packages to install manually:
* mc ()
* Biopython (http://biopython.org/wiki/Download)

##### Install rest of packages from requirements
```
pip install -r requirements.txt
```

#### Installation
- install forge minecraft server (version 1.8, may not work otherwise)
- install the RaspberryJamMod.jar (https://github.com/arpruss/raspberryjammod)
- Identify a folder called “mcpipy”, within the installation dictionary
- clone our repository “cellcraft” as a subfolder in mcpipy
- copy the cellcraft.py from the subfolder into the mcpipy folder (move cellcraft.py one level up)

#### Getting started
- start the server
- connect with client
- open the minecraft console
- try: py cellcraft pdb 3J9U 2 4 -15 load

#### Usage
  py cellcraft [pdb/cellpack] [PDBcode] <threshold> <blocksize> <horizontal_shift> [load/nolo]
- `py cellcraft` : mandatory
- `[pdb/cellpack]` : load pdb or cellpack structure (the later is not covered here)
- `[PDBcode]` : specify the PDB code (for pdb)
- `<threshold>` : minimum number of atoms found in grid cube to be filled
- `<blocksize>` : spacing of the grid in Angstroem
- `<horizontal_shift>` : horizontal shift of the structure in respect of the player position
- `[load/nolo]` :  load structure from database / take local copy
  (the latter is only possible if the same PDBid was processed before with the same threshold and blocksize)


#### Contact
info@thecellcraftproject.org
