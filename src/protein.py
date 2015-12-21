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

class complex():
    def __init__(self, pdbin):
        self.pdb_id = pdbin
        # primarykey = pdb_id_uniprot_id
        # pdb_id
        # uniprot_id

    # get and clean the PDB file from database
    def get_clean_pdb(self):
        # Request pdb files from Protein Data bank
        PDB = 'http://www.rcsb.org/pdb/files/'+self.pdb_id+'.pdb'
        h = wget.download(PDB, bar=None)
        
	# get the polypeptide chains from pdb
	self.p = PDBParser()
	self.seq = self.p.get_structure(self.pdb_id, h)

	# clean the heteroatoms from pdb and save pdb as "clean_pdbid.pdb"
	io = PDBIO()
	io.set_structure(self.seq)
	io.save('clean_'+self.pdb_id+'.pdb', NonHetSelect())

    # if protein complex, define chains (apply everythin for each chain)
    def split_complex(self):
	# get list of polypeptide chains in pdb
	ppd = PPBuilder()
        chs = defaultdict(list)
        print "\n", self.pdb_id, "\n"
        fil = open(self.pdb_id+'.fa', 'w')
        for pp in ppd.build_peptides(self.seq):
            for model in pp:
                for chain in model:
                    c = chain.get_full_id()
                    ch = c[2]
            a = pp.get_sequence()
            chs[ch].append(a)
        self.chains = chs.keys()
        # for each chain generate a pdb and call class protein
	io = PDBIO()
	self.seq = self.p.get_structure(self.pdb_id, 'clean_'+self.pdb_id+'.pdb') 
	for i in self.chains:
            io.set_structure(self.seq)
	    io.save(self.pdb_id+'_'+i+'.pdb', ChainSelect(i))	  

    # define protein features of monomers protein class inheritance
    def monomer_feat(protein):
	pass
 	
# create an instance with a prot/prot complex
pdbin = sys.argv[1]
print pdbin

mycomplex = complex(pdbin)
mycomplex.get_clean_pdb()
mycomplex.split_complex()
listchains = mycomplex.chains

print listchains




