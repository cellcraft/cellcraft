################
################ defining interface with minecraft
################

import numpy as np
import pickle

from mc import Block, Minecraft

# import other methods of cellcraft
from .src.cellpack import add_cellpack
from .src.protein import add_pdb
path = "./"


#mc.postToChat("Glass donut done")


def minecraft_api(args):
    '''
    Usage:
        py cellcraft (pdb|cellpack) <PDBid> <threshold> <blocksize> (load|nolo)
    '''
    mc, pos = connect_mc()
    if len(args) != 7:
        ValueError('Wrong number of arguments.')
    p0 = (int(pos.x),int(pos.y + int(args[5])),int(pos.z))
    if args[1] == 'pdb':
        if args[6] == 'load':
            array, colordict, texture = add_pdb(*args[2:5])
            pickle.dump((array, colordict, texture), open('_'.join(args[1:5])+".pkl", "wb" ) )
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
    return mc, pos


def add_numpy_array(mc, array, p0, colordict, texture, swap):
    it = np.nditer(array, flags=['multi_index'], op_flags=['readonly'])
    while not it.finished:
        if it[0] > 0:
            x, y, z = it.multi_index
            if swap:
                height = array.shape[2]
                mc.setBlock(
                    p0[0]+x, p0[1]+(height-z), p0[2]+y,
                    Block(texture[int(it[0])], colordict[int(it[0])]))
            else:
                mc.setBlock(
                    p0[0]+x, p0[1]+y, p0[2]+z,
                    Block(texture[int(it[0])], colordict[int(it[0])]))
        it.iternext()
