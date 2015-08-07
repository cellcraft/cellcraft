#!/usr/bin/python
# -*- coding: utf-8 -*-


import math, sys, wget, gzip, os, glob
from collections import *
from Bio.PDB import *
from Bio.SeqUtils.CheckSum import seguid
from Bio import SeqIO
from Bio import *
from Bio.Alphabet import IUPAC
from Bio.Seq import Seq


### Variables
pdbin = '1p38'
aa_list = ['ALA','ARG','ASN','ASP','ASX','CYS','CYM','CYX','GLN','GLU','GLX','GLY','HIS','HIE','HIP','HID','ILE','LEU','LYS','MET','PHE','PRO','SER','THR','TRP','TYR','UNK','VAL']

### SOME TOOLS

# get and clean a pdb file
def get_clean_pdb(pdbin):
    # Request pdb files from Protein Data bank
    PDB = 'ftp://ftp.wwpdb.org/pub/pdb/data/structures/all/pdb/pdb'+pdbin+'.ent.gz'
    wget.download(PDB)
    gzip.open('pdb'+pdbin+'.ent.gz', 'rb')

   
    # Get secuence of polipeptides and print it to let the people know what are they uploading
    p = PDBParser()
    seq = p.get_structure(pdbin, './PDB/pdb'+pdbin+'.ent')
    io = PDBIO()
    io.set_structure(seq)
    io.save('./PDB/'+pdbin+'.pdb')
    print 'This is the sequence of '+pdbin+':\n', seq
    return seq

def model_prot(pdbin):
    # Generate a modell of the protein to fill gaps '/home/celsa/Documents/Pompeu Fabra/SBI/steps.txt'
    # This can be done by users once the game is working so develop later 
    print "1. Get seq of the protein \n2. Find other seqs similar \n3. Find structures \n3.a. Build modell \n3.b.1. Predict secondary structure in gap \n3.b.2. Build modell by secondary structure prediction"
    return pdbin

# locate pdb 

# create shape of unit

# generate ids (connect with the database)



### HELP/usage

if sys.argv[0] == "- h":
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
elif len(sys.argv[1]) < 4:
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
         ''' % (sys.argv[0], sys.argv[0])
         exit(0)
      elif len(i) > 4:
         print '''
         PDB id should contain 4 characters (e.g. 1p38).
         Please, try again as following:
         python get_prot.py '1p38 4c6d'
         ''' % (sys.argv[0], sys.argv[0])
         exit(0)

  # Check if already downloaded, replace
  for b in mypdbs:
      if glob.glob(b+'.pdb'): 
          os.remove(b+'.pdb') 
      if glob.glob(b+'.fa'):
          os.remove(b+'.fa')

  #### Generate a unit for each pdb file
  for b in mypdbs:
      
      ## Request pdb files from Protein Data bank
      PDB = 'http://www.rcsb.org/pdb/files/'+b+'.pdb'
      h = wget.download(PDB, bar=None)

      ## Get secuence of polipeptides and print it to let the people know what are they uploading
      p = PDBParser()
      seq = p.get_structure(b, h)

      ## Clean the structure and leave only the protein
      class NonHetSelect(Select):
          def accept_residue(self, residue):
                  return 1 if residue.id[0] == " " else 0
      io = PDBIO()
      io.set_structure(seq)
      io.save(h, NonHetSelect())

      ## Get the sequence/s of the protein/s
      ppd = PPBuilder()
      chains = defaultdict(list)
      print "\n", b, "\n"
      fil = open(b+'.fa', 'w')
      for pp in ppd.build_peptides(seq):
          for model in pp:
              for chain in model:
                  c = chain.get_full_id()
                  ch = c[2]
          a = pp.get_sequence()
          chains[ch].append(a)
          #print "This is/are the seq/s of ", b, "\n", pp.get_sequence(), "\n"

      ## Concatenate sequences if are from a fragmented chain
      concatenated = Seq("", IUPAC.protein)
      print "This is/are the seq/s of ", b, "\n"
      for c, s in chains.iteritems():
         if len(s) > 1:
             for i in s:
                     concatenated += i
             s = concatenated
         chains[c] = s
         print c, [chains[c]]   
      
      ## Identify if monomer or oligomer
      if len(chains) == 1:
          idx = '00'
          print "\nProtein is a monomer\n"
      else:
          idx = '01'
          print "\nProtein is a polimer\n"

      ## Identify repeated chains
      if idx == '01':
          print "\nLet's check if monomers are equal:\n"      



      # Modell gaps 






