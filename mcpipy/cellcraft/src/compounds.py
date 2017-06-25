################
################ define features of Compounds()
################

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

from cellcraft.src.item import *
from cellcraft.src.protein import *

############## TODO
### get KEGG ids, function, relate with the protein if needed, generate grid independent or wihin complex and generate color/texture
# Define data structure of chemicals
class Compounds():
    def __init__(self, chemid, protid):
        # def function (substrate, ligand, effector, inhibitor)
        # def color (make a list of important compounds and specific colors in /data and also colors for each function)
        pass
