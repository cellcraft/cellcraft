#!/usr/bin/python
# -*- coding: utf-8 -*-


import math, sys, wget, gzip
from os import *
from sys import *
from Bio.PDB import *


### Variables
pdbeg = '1p38'
PDB = 'ftp://ftp.wwpdb.org/pub/pdb/data/structures/all/pdb/pdb'+pdbeg+'.ent.gz'



### SOME TOOLS

# get and clean a pdb file
def get_clean_pdb(pdbin):
    # Request pdb files from Protein Data bank
    pdbl = PDBList(pdb='./pdb/')
    pd = pdbl.retrieve_pdb_file(pdbin)
    return pd

# locate pdb 

# create shape of unit

# generate ids (connect with the database)



### HELP/usage

if argv[0] == "- h":
  # coments/usage
  print '''
  Usage: get_prot [PDB ID]... [??]...
  Will download the pdb requested structure from the oficial Protein Data Bank.

  Mandatory arguments to long options are mandatory for short options too.

    -c, --stdout      write on standard output, keep original files unchanged
    -d, --??
    -h, --help        give this help
    -q, --quiet       suppress all warnings

  With no FILE, or when FILE is -, read standard input.


  ''' 
  exit(0)


 # Incorrect pdb id givenmolecules
elif len(argv[1]) < 4:
  # coments/usage
  print '''
  PDB id should contain 4 characters (e.g. 1p38).
  Please, try again as following:
  python get_prot.py '1p38 4cfm'
  ''' 
  exit(0)

else:

  # generate array, possible to request several structures at the same time
  mypdbs = sys.argv[1].split()
  
  # check if all the ids given contain 4 characters
  for i in mypdbs:
      if len(i) < 4:
         print '''
         PDB id should contain 4 characters (e.g. 1p38).
         Please, try again as following:
         python get_prot.py '1p38 4cfm'
         ''' % (argv[0], argv[0])
         exit(0)
      elif len(i) > 4:
         print '''
         PDB id should contain 4 characters (e.g. 1p38).
         Please, try again as following:
         python get_prot.py '1p38 4cfm'
         ''' % (argv[0], argv[0])
         exit(0)

  #### Generate a unit for each pdb file
  for struc in mypdbs:

      # Request pdb files from Protein Data bank
      nf = get_clean_pdb(i) 
      print nf      








