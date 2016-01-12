import math, sys, gzip, os, os.path, glob, wget, urllib, sqlite3, datetime
from collections import *
from Bio.PDB import *
from Bio.SeqUtils.CheckSum import seguid
from Bio import SeqIO
from Bio import *
from Bio.Alphabet import IUPAC
from Bio.Seq import Seq
from xml.dom import minidom
import numpy as np

from mc import *

# import other methods of cellcraft
from src.cellpack import *
from .src.protein import *
from .src.item import *
from .src.envelope import *
from .src.lipid import *
from .src.nucleotide import *
from .src.compounds import *
from .src.usage import *
from .src.errorcheck import *

path = "./"


def minecraft_api(args):
    mc,pos = connect_mc()
    p0 = (int(pos.x),int(pos.y + 3),int(pos.z))
    if len(args)>3 or len(args)<3:
        print('Two arguments needed.')
    else:
        if args[1] == 'pdb':
            array,colordict = add_pdb(*args[2:5])
        if args[1] == 'cellpack':
            array,colordict = add_cellpack(*args[2:5])
        add_numpy_array(array,p0,blocktype=STAINED_HARDEND_CLAY_BLOCK,colordict)

def connect_mc():
    mc = Minecraft()
    pos = mc.player.getPos()
    return mc,pos

def add_numpy_array(array,p0,blocktype=STAINED_HARDEND_CLAY_BLOCK,colordict=defaultdict(lambda 0)):
    it = np.nditer(array, flags=['multi_index'],op_flags=['readonly'])
    while not it.finished:
        if it[0] > 0:
            x,y,z = it.multi_index
            mc.setBlock(x0+x,y0+y,z0+z,blocktype,colordict[it[0]])
        it.iternext()
