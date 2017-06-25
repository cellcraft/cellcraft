################
################ define features of CellcraftGrid()
################

import numpy as np


# transform pdb into bocks cellcraft
class CellcraftGrid():
    ############## TODO
    ### add weights in the future for each atom when defined the method in Protein() or Lipid()
    def __init__(self, threshold, blocksize): 
        self.blocksize = blocksize
        self.threshold = threshold
        self.coordinates = []
        self.pids = []

    def add_coordinates(self, coordinates, pid):
        self.coordinates.append(coordinates)
        self.pids.append(pid)

    def make_grid(self):
        amax = np.amax([np.amax(coor, axis=0) for coor in self.coordinates], axis=0)
        amin = np.amin([np.amin(coor, axis=0) for coor in self.coordinates], axis=0)
        self.x = np.arange(amin[0], amax[0]+self.blocksize, self.blocksize)
        self.y = np.arange(amin[1], amax[1]+self.blocksize, self.blocksize)
        self.z = np.arange(amin[2], amax[2]+self.blocksize, self.blocksize)
        self.values = np.zeros((self.x.shape[0]-1, self.y.shape[0]-1, self.z.shape[0]-1))

    # generate a 3D histogram for the coordinates
    def def_blocks(self):
        for coor, pid in zip(self.coordinates, self.pids):
            H, self.edges = np.histogramdd(coor, bins=(self.x, self.y, self.z))
            self.values[(H >= self.threshold)] = pid

    ############### TODO
    ### generate matrices with the different rotations in the feature (60 degrees each)
    def move_item(self, refrot, reftrans):
        pass


# calculate max-min
def cal_minmax(maxi, mini):
    return int(maxi)-int(mini)
