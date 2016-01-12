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
from .src.cellpack import *
from .src.protein import *
from .src.item import *
from .src.envelope import *
from .src.lipid import *
from .src.nucleotide import *
from .src.compounds import *
from .src.usage import *
from .src.errorcheck import *

path = "./"

palette = (WOOL_WHITE,HARDENED_CLAY_STAINED_WHITE,WOOL_PINK,WOOL_MAGENTA,WOOL_PURPLE,HARDENED_CLAY_STAINED_LIGHT_BLUE,HARDENED_CLAY_STAINED_CYAN,HARDENED_CLAY_STAINED_PURPLE,HARDENED_CLAY_STAINED_LIGHT_GRAY,HARDENED_CLAY_STAINED_MAGENTA,HARDENED_CLAY_STAINED_PINK,HARDENED_CLAY_STAINED_RED,WOOL_RED,REDSTONE_BLOCK,HARDENED_CLAY_STAINED_ORANGE,WOOL_ORANGE,HARDENED_CLAY_STAINED_YELLOW,WOOL_YELLOW,WOOL_LIME,HARDENED_CLAY_STAINED_LIME,HARDENED_CLAY_STAINED_GREEN,WOOL_GREEN,HARDENED_CLAY_STAINED_GRAY,WOOL_BROWN,HARDENED_CLAY_STAINED_BROWN,WOOL_GRAY,HARDENED_CLAY_STAINED_BLUE,WOOL_BLUE,WOOL_CYAN,WOOL_LIGHT_BLUE,WOOL_LIGHT_GRAY)


def minecraft_api(args):
    mc,pos = connect_mc()
    p0 = (int(pos.x),int(pos.y + 3),int(pos.z))
#    p0 = (123,123,23)
    if len(args)>5 or len(args)<5:
        print('Two arguments needed.')
    else:
        if args[1] == 'pdb':
            array,colordict,texture = add_pdb(*args[2:5])
        if args[1] == 'cellpack':
            array,colordict,texture = add_cellpack(*args[2:5])
        add_numpy_array(mc,array,p0,colordict,texture)

def connect_mc():
    mc = Minecraft()
    pos = mc.player.getPos()
    return mc,pos

def add_numpy_array(mc,array,p0,colordict,texture):
    it = np.nditer(array, flags=['multi_index'],op_flags=['readonly'])
    while not it.finished:
        if it[0] > 0:
            x,y,z = it.multi_index
            mc.setBlock(p0[0]+x,p0[1]+y,p0[2]+z,Block(texture[int(it[0])],colordict[int(it[0])]))
        it.iternext()
