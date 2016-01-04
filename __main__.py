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
from src.protein import *
from src.item import *
from src.envelope import *
from src.lipid import *
from src.nucleotide import *
from src.compounds import *
from src.usage import *
from src.errorcheck import *


# create an instance with a prot/prot complex
pdbin = sys.argv[1]
print pdbin

mycomplex = complex(pdbin)
mycomplex.get_clean_pdb()
mycomplex.split_complex()
listchains = mycomplex.chains

print listchains

# for each protein in PDB
for i in listchains:
    # obtain matrix of coordenates
    myprot = protein(pdbin,i)
    myprot.get_coord()
    mymatrix = myprot.coord
    numatoms = myprot.num_lines
    print mymatrix
    print numatoms

    # obtain grid
    

