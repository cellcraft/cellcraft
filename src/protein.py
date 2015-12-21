import math, sys, gzip, os, glob
import wget
from collections import *
from Bio.PDB import *
from Bio.SeqUtils.CheckSum import seguid
from Bio import SeqIO
from Bio import *
from Bio.Alphabet import IUPAC
from Bio.Seq import Seq



# Define features for input object protein

class protein():
    # define protein info
    def __init__(self,pdbin):
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
    def prot_color():
	# get into data the codes
	pass

    # obtain aa sequence
    def get_aa_seq(self):
	# query from uniprot_id -> seq in website aa_seq

        # get seq from pdb file with possible gaps and mutations aa_seq_pdb
        p = PDBParser() 
        aa_seq_pdb = p.get_structure(pdbin, './PDB/pdb'+pdbin+'.ent')
        io = PDBIO()
        io.set_structure(aa_seq_pdb)
        io.save('./PDB/'+pdbin+'.pdb')
        print 'This is the sequence of '+pdbin+':\n', aa_seq_pdb
        return aa_seq_pdb 

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


class complex():
    def __init__(self, pdbin):
        self.pdb_id = pdbin
        # primarykey = pdb_id_uniprot_id
        # pdb_id
        # uniprot_id
        pass

    # select only aa in the pdb file
    def accept_residue(residue):
        return 1 if residue.id[0] == " " else 0

    # get and clean the PDB file from database
    def get_clean_pdb(self):
        # Request pdb files from Protein Data bank
        PDB = 'http://www.rcsb.org/pdb/files/'+self.pdb_id+'.pdb'
        h = wget.download(PDB, bar=None)
        
	# get chains	

	# parse find polypeptide chains
	p = PDBParser()
	seq = p.get_structure(self.pdb_id, h)
	ppd = PPBuilder()
	chs = defaultdict(list)
        print "\n", self.pdb_id, "\n"
        fil = open(self.pdb_id+'.fa', 'w')
        for pp in ppd.build_peptides(seq):
            for model in pp:
                for chain in model:
                    c = chain.get_full_id()
                    ch = c[2]
            a = pp.get_sequence()
            chs[ch].append(a)
	# get list of polypeptide chains in pdb
	self.chains = chs.keys()

	# for each chain in chains get a cleaned pdb

	io = PDBIO()
        io.set_structure(seq)
#        io.save(h, self.accept_residue())

    # if protein complex, define chains (apply everythin for each chain)
    def prot_complex(self):
        # for each chain call class protein and get all the variables
        pass

# create an instance with a prot/prot complex
pdbin = sys.argv[1]
print pdbin

mycomplex = complex(pdbin)
mycomplex.get_clean_pdb()
listchains = mycomplex.chains

print listchains




