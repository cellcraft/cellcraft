# The Cellcraft Project


### Setup your computer for using Cellcraft
#### Start a Docker Image and create a MongoDB where to store the biological information of your minecraft world (Run only once!!)

* Install Docker in your computer: https://docs.docker.com/docker-for-mac/install/
* You can also install Kinematic as an interface for the docker image

* Create an instance Mongo database
```
docker pull mongo:latest
```

* For accessing the mongo shell
```
docker run --name mongo -d mongo --net=host # run -p 27017:27017 --name mongo -d mongo

docker exec -it mongo /bin/bash
db = db.getSiblingDB('admin');
db.createUser({ user: 'admin', pwd: 'admin', roles: [ { role: "userAdminAnyDatabase", db: "admin" } ] });
db = db.getSiblingDB('cellcraft');
db.createUser({ user: "cellcraft", pwd: "cellcraft", roles: [{role: "readWrite", db: "cellcraft"}]});
db = db.getSiblingDB('test');
db.createUser({ user: "test", pwd: "test", roles: [{role: "readWrite", db: "test"}]});
```

* Check if user and was correctly created
```
docker exec -it mongo bash
mongo cellcraft -u cellcraft -p cellcraft
```

* To backup the database into "cellcraft-backup" folder (backup the database regularly)
```
docker exec -it mongo bash
mongodump --db cellcraft --out cellcraft/mongo_storage/data/cellcraft-backup
```


#### Setup your python environment

* Install pyenv and run setup the cellcraft pyenv
```
brew install pyenv-virtualenv
echo 'eval "$(pyenv init -)"' >> ~/.bash_profile
source ~/.bash_profile
pyenv install 3.6.2
pyenv global 3.6.2
source ~/.bash_profile

pyenv virtualenv 3.6.2 cellcraft
pyenv activate cellcraft
```

##### Install python packages from requirements
```
pip install -r requirements.txt
```

### Setup the Mincraft server and connect it to cellcraft
#### Installation of Minecraft Client
- Download Minecraft server
- Run client once with correct version (1.12)
- Download forge installer (version 1.12) from http://files.minecraftforge.net/ (Notice that you need to have the Java Developer Kit installed)
- Run forge installer and install client into minecraft folder (no change needed)

#### Installation of Minecraft Server with RaspberryJamMod
- Download forge installer (version 1.12) from http://files.minecraftforge.net/ (same then above)
- Run forge installer and install server into the root directory of the repo
- Download from https://github.com/arpruss/raspberryjammod/releases the mods.zip
- Unzip the mods.zip and copy the mods folder content into the mods folder in the root directory of the repo
- Run the forge-1.12-14.21.0.2359-universal.jar once
- Edit the eula.txt and change false to true
- Start the server running forge-1.12-14.21.0.2359-universal.jar again

#### Starting the server with cellcraft
- Start the server in the root folder of the repo with your python environment correctly setup and start the server
```
java -jar forge-1.12-14.21.0.2359-universal.jar
```

### Now you are ready to start! Join the server
- start the client
- choose Multiplayer
- choose Direct Connect
- add 0.0.0.0 as server adress and join server
- type: /py cellcraft -m pdb -n 3J9U -t 2 -s 4 -he -15 -C



#### Contact
info@thecellcraftproject.org
