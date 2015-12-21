

class item_cellcraft():
    def __init__(self, threshold, blocksize):
	# define threshold
	# get name of item
	# define blocksize
	pass

    # rotate item if needed to center 
    def move_item(self, refrot, reftrans):
	# transport item to ref position
	# get the rotated structures of item for given refs
	pass

    # define the volume that item will need 
    def vol_prot(self):
        # calculate the vol each needs
        pass

    # parse item throuh the grid
    def def_blocks(self):
        # generate a 3d grid for my coordinates
        # get volumen of my item to know boundaries according to blocksize units defined
        # use a 3d histogram (numpy 3d bin)
        # define empty or full by threshold
        pass

    # translate grid into cellcraft format
    def def_cellcraftinput(self):
        pass

    # define the item in cellpack format
    def def_cellpackinput(self):
	pass

    # define the moment the data is requested    
    def date_time(self):
        # date and time of the data generation




