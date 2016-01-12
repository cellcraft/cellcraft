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
import scipy


class grid():
    def __init__(self,amin,amax,blocksize):
        self.x = np.arange(amin[0],amax[0]+blocksize,blocksize)
        self.y = np.arange(amin[0],amax[0]+blocksize,blocksize)
        self.z = np.arange(amin[0],amax[0]+blocksize,blocksize)
        self.values = np.zeros((self.x.shape[0],self.y.shape[0],self.z.shape[0]))
