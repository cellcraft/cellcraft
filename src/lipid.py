################
################ define features of Lipid() and Membrane() using Protein() and ProteinComplex() methods as a reference
################


import math, sys, gzip, os, os.path, glob, re, urllib, wget
import xml.etree.ElementTree as ET
from datetime import datetime, timedelta
from pymongo import MongoClient
from collections import *

from Bio.PDB import *
from Bio.SeqUtils.CheckSum import seguid
from Bio import SeqIO
from Bio import *
from Bio.Alphabet import IUPAC
from Bio.Seq import Seq
from xml.dom import minidom
import numpy as np

from cellcraft.src.item import *

path = ''

############# TODO
### add methods to define
        ## features of different lipids for posterior color/texture in Membrane()
        ## coordinates to send it to Membrane() and CellcraftGrid()
        ## generate lipid properties list for the .json (evaluate if in this case its better to generate one json per membrane instead of per lipid)
class Lipid():
    def __init__(self, unitcell_struc):
        pass
    
    # get coordinates
    def lip_coord(self):
        pass

    def lip_color(self):
        pass

    def genjson_lipid(self): #???
        pass
    

############# TODO
### add methods to define
        ## clean and split the membrane into different lipids and send them to Lipids()
        ## generate color/texture with the features of different lipids given in Lipids() based on the algorithm defined in ProteinComplex()
        ## generate the common grid for all the membrane
        ## generate lipid properties list for the .json (evaluate if in this case its better to generate one json per membrane instead of per lipid)
class Membrane():
    def __init__(self, pdbid):
        pass

    def clean_pdb(self):
        pass

    def split_lipids(self):
        pass

    def colors_textures(self):
        pass

    def genjson_membrane(self): #???
                pass

