import math, sys, gzip, os, glob, re, urllib
import wget
import xml.etree.ElementTree as ET
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


# Define features for input object protein

class protein():
    # define protein info
    def __init__(self,pdbin, chainId):
	self.pdb_id = pdbin
	self.chainId = chainId
	# define uniprot_id from PDB website
#	url_str = 'http://www.rcsb.org/pdb/rest/hmmer?structureId='+self.pdb_id
#	xml_str = urllib.urlopen(url_str).read()
#	xmldoc = minidom.parseString(xml_str)
	# primarykey = pdb_id_uniprot_id
        # pdb_id
	# uniprot_id
	# aa_seq
	# pfam_id
	# GO_id
	# GO_type
	# EC_id
	# KEGG_id
	# KEGG_pathway
	# prot_color (attribute a color to each KEGG pathway in /data)
	# gene_id
	# entrez_id
	# NT_seq
	pass

    # define color for each prot
    def prot_color(self):
	# get into data the codes
	pass

    # get coordinates out of pdb
    def get_coord(self):
	io = PDBIO()
	self.p = PDBParser()
	
	# self.seq is the sequence of aa for this chain
	self.seq = self.p.get_structure(self.pdb_id, 'clean_'+self.pdb_id+'.pdb')

	# save the pdb with this unique chain
        io.set_structure(self.seq)
        io.save(self.pdb_id+'_'+self.chainId+'.pdb', ChainSelect(self.chainId))
        self.chain = self.p.get_structure(self.pdb_id+'_'+self.chainId, self.pdb_id+'_'+self.chainId+'.pdb')

        # save coordinates in zeros.matrix of num_linesX3 dimension
        self.num_lines = sum(1 for line in open(self.pdb_id+'_'+self.chainId+'.pdb'))
        for line in open(self.pdb_id+'_'+self.chainId+'.pdb'):
            if line.find("ATOM") == -1:
                self.num_lines -=1
        self.coord = np.zeros((self.num_lines,3), dtype=np.float)
        for model in self.chain:
            for chain in model:
                count = 0
                for residue in chain:
                    for atom in residue:
                        cd = atom.get_coord()
                        self.coord[count][0] = cd[0]
                        self.coord[count][1] = cd[1]
                        self.coord[count][2] = cd[2]
                        count += 1

    # get protein IDs
    def get_ids(self):
	tree = ET.ElementTree(file=urllib.request.urlopen('http://www.rcsb.org/pdb/rest/das/pdb_uniprot_mapping/alignment?query='+self.pdb_id))
	root = tree.getroot()
	root.getchildren()
	self.uniprotId = root.getchildren()[0][1].attrib['intObjectId']

    # define weigth array with specific weigths for atoms that need special importance (active site...) when parsed in the grid
    def atom_weigth(self):
	# for the moment lets keep it as all the same weigth
	pass

    # define the ligands, inhibitors, effectors...
    def compounds_prot(self):
	# get KEEG_chemicals for that KEGG_id
	pass

    # Generate a modell of the protein '/home/celsa/Documents/Pompeu Fabra/SBI/steps.txt' 
    def model_prot(self):
        # development in further steps when aa_seq_pdb != aa_seq 
        print "1. Get seq of the protein \n2. Find other seqs similar \n3. Find structures \n3.a. Build modell \n3.b.1. Predict secondary structure in gap \n3.b.2. Build modell by secondary structure prediction"

    # generate the dataframe for user and server (json format)
    def gen_dataframe(self):
	# ids for user
	# all info in server
        pass

# protein pdb cleaner (BioPython)
class NonHetSelect(Select):
    def accept_residue(self, residue):
        return 1 if residue.id[0] == " " else 0

# select chain from pdb (BioPython)
class ChainSelect(Select):
    # create the chain name variable for Select class
    def __init__(self, chname):
	self.chname = chname
 
    def accept_chain(self, chain):
        if chain.get_id() == self.chname:
            return 1
        else:
            return 0

class protein_complex():
    def __init__(self, pdbin):
        self.pdb_id = pdbin
        # primarykey = pdb_id_uniprot_id
        # pdb_id
        # uniprot_id

    # get pdb file from PDB database when not available
    def get_PDB(self):
        # Request pdb files from Protein Data bank
        PDB = 'http://www.rcsb.org/pdb/files/'+self.pdb_id+'.pdb'
        h = wget.download(PDB, bar=None)

    # clean the PDB file from database
    def clean_pdb(self):
	# get the polypeptide chains from pdb
	self.p = PDBParser()
	self.seq = self.p.get_structure(self.pdb_id, self.pdb_id+".pdb")

	# clean the heteroatoms from pdb and save pdb as "clean_pdbid.pdb"
	io = PDBIO()
	io.set_structure(self.seq)
	io.save('clean_'+self.pdb_id+'.pdb', NonHetSelect())

    # if protein complex, define chains (apply everythin for each chain)
    def split_complex(self):
	# get list of polypeptide chains in pdb
	ppd = PPBuilder()
        chs = defaultdict(list)
        print("\n", self.pdb_id, "\n")
        fil = open(self.pdb_id+'.fa', 'w')
        for pp in ppd.build_peptides(self.seq):
            for model in pp:
                for chain in model:
                    c = chain.get_full_id()
                    ch = c[2]
            a = pp.get_sequence()
            chs[ch].append(a)
        self.chains = chs.keys()
