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
    if len(args)>3 or len(args)<3:
        print('Two arguments needed.')
    else:
        if args[1] == 'pdb':
            add_pdb(args[2])



def add_numpy_array(array):
    mc = Minecraft()
    playerPos = mc.player.getPos()
    x0 = int(playerPos.x)
    y0 = int(playerPos.y + 3)
    z0 = int(playerPos.z)
    block_type = GLOWSTONE_BLOCK
    it = np.nditer(array, flags=['multi_index'],op_flags=['readonly'])
    while not it.finished:
        if it[0] == 1:
            x,y,z = it.multi_index
            mc.setBlock(x0+x,y0+y,z0+z,block_type)
        it.iternext()

#    vec = np.vectorize(api_set_block,set([3,4,5,6]))
    print(array)
    print(x0,y0,z0)
    #vec(array,x0,y0,z0,block_type)


def add_pdb(pdbin):
    # create an instance with a prot/prot complex
    myProtcomplex = protein_complex(pdbin)
    myProtcomplex.get_PDB()
    myProtcomplex.clean_pdb()
    myProtcomplex.split_complex()
    listchains = myProtcomplex.chains
    # for each protein in PDB
    for chain in listchains:
        GOs = []
        EntrezIds = []
        ENSEMBLids = []
        ECs = []
        KOpathIDs = []
        KPathways = defaultdict(list)
        myprot = protein(pdbin, chain, GOs, EntrezIds, ENSEMBLids, ECs, KOpathIDs, KPathways,'try')

        # obtain matrix of coordenates
        myprot.get_coord()
        mymatrix = myprot.coord
        numatoms = myprot.num_lines

        # obtain grid
        mygrid = item_cellcraft(mymatrix,1,1)
        mygrid.vol_prot()
        mygrid.def_blocks()
        output = mygrid.H

        # obtain IDs
        myprot.get_ids()
        uniprotid = myprot.uniprotId
        keggid = str(myprot.keggId)
        GOterms = myprot.GOs
        ECs = myprot.ECs
        gEntrez = myprot.EntrezIds
        gEnsembl = myprot.EnsemblIds
        KOpaths = myprot.KOpathIDs
        KPaths = myprot.KPathways
        output[output > 0] = 1
        add_numpy_array(output)
        return 'Done!!!!'
