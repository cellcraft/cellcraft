import math, sys, gzip, os, glob
import wget
from collections import *
from Bio.PDB import *
from Bio.SeqUtils.CheckSum import seguid
from Bio import SeqIO
from Bio import *
from Bio.Alphabet import IUPAC
from Bio.Seq import Seq
from xml.dom import minidom
import urllib
import numpy as np


# transform pdb into bocks cellcraft
class cellcraft_grid():
    def __init__(self,threshold,blocksize): # add weigth in future
        self.blocksize = blocksize
        self.threshold = threshold
        self.coordinates = []
        self.pids = []

    def add_coordinates(self,coordinates,pid):
        self.coordinates.append(coordinates)
        self.pids.append(pid)

    def make_grid(self):
        amax = np.amax([np.amax(coor,axis=0) for coor in self.coordinates],axis=0)
        amin = np.amin([np.amin(coor,axis=0) for coor in self.coordinates],axis=0)
        self.x = np.arange(amin[0],amax[0]+self.blocksize,self.blocksize)
        self.y = np.arange(amin[1],amax[1]+self.blocksize,self.blocksize)
        self.z = np.arange(amin[2],amax[2]+self.blocksize,self.blocksize)
        self.values = np.zeros((self.x.shape[0]-1,self.y.shape[0]-1,self.z.shape[0]-1))

    # parse item throuh the grid -> give: grid cell unit (A), dimensions (A) X,Y,Z
    def def_blocks(self):
        for coor,pid in zip(self.coordinates,self.pids):
            # generate a 3D histogram
            H, self.edges = np.histogramdd(coor, bins=(self.x, self.y, self.z))
            self.values[(H >= self.threshold)] = pid

    # rotate item if needed to center ->  new dimensions, needed????????
    def move_item(self, refrot, reftrans):
        # transport item to ref position
        # get the rotated structures of item for given refs
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
        pass

# calculate max-min
def cal_minmax(maxi, mini):
    return int(maxi)-int(mini)
