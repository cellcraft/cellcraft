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
import protein
from src import item
#from src.item import *
#from src.envelop import *
#from src.lipid import *
#from src.nucleotide import *
#from src.compounds import *
#from src.usage import *
#from src.errorcheck import *


# create an instance with a prot/prot complex
pdbin = sys.argv[1]
print pdbin

mycomplex = complex(pdbin)
mycomplex.get_clean_pdb()
mycomplex.split_complex()
listchains = mycomplex.chains

print listchains
