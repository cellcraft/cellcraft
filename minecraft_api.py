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
import pickle


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
import time
path = "./"


def minecraft_api(args):
    mc,pos = connect_mc()
#    p0 = (123,123,23)
    if len(args)>7 or len(args)<7:
        print('Wrong number of arguments.')
    else:
        p0 = (int(pos.x),int(pos.y + int(args[5])),int(pos.z))
        if args[1] == 'pdb':
            if args[6] == 'load':
                array,colordict,texture = add_pdb(*args[2:5])
                pickle.dump((array,colordict,texture), open('_'.join(args[1:5])+".pkl", "wb" ) )
            else:
                array,colordict,texture = pickle.load( open( '_'.join(args[1:5])+".pkl", "rb" ) )
            swap = True
        if args[1] == 'cellpack':
            swap = False
            if args[6] == 'load':
                array,colordict,texture = add_cellpack(*args[2:5])
                pickle.dump((array,colordict,texture), open('_'.join(args[1:5])+".pkl", "wb" ) )
            else:
                array,colordict,texture = pickle.load( open( '_'.join(args[1:5])+".pkl", "rb" ) )
        add_numpy_array(mc,array,p0,colordict,texture,swap=swap)

def connect_mc():
    mc = Minecraft()
    pos = mc.player.getPos()
    return mc,pos

def add_numpy_array(mc,array,p0,colordict,texture,swap):
    it = np.nditer(array, flags=['multi_index'],op_flags=['readonly'])

    while not it.finished:
        if it[0] > 0:
            x,y,z = it.multi_index
            if swap:
                height = array.shape[2]
                mc.setBlock(p0[0]+x,p0[1]+(height-z),p0[2]+y,Block(texture[int(it[0])],colordict[int(it[0])]))
            else:
                mc.setBlock(p0[0]+x,p0[1]+y,p0[2]+z,Block(texture[int(it[0])],colordict[int(it[0])]))
        it.iternext()
