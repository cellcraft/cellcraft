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


url_str = 'http://www.rcsb.org/pdb/rest/hmmer?structureId=3V8X'
xml_str = urllib.urlopen(url_str).read()
xmldoc = minidom.parseString(xml_str)

pfamhit_values = xmldoc.getElementsByTagName('pfamHit')
print pfamhit_values
print pfamhit_values[4].firstChild.nodeValue
