################
################ define features of Nucleotide() and NucleotChain() using Protein() and ProteinComplex() methods as a reference
################


from Bio import *
from Bio.PDB import *

path = ''

############# TODO
### add methods to define
        ## features of different nucleotides (U,C,G,T,A) for posterior color/texture in NucleotChain()
        ## coordinates to send it to NucleotChain() and CellcraftGrid()
class Nucleotide():
    def __init__(self, unitcell_struc):
        pass

    # get coordinates
    def nucleot_coord(self):
        pass

    def nucleot_color(self):
        pass


############# TODO
### add methods to define
        ## clean and split the polinucleotide chain into different nucleotides and send them to Nucleotide()
        ## generate color/texture with the features of different genes or nucleotides given in Nucleotide() and define own algorithm
        ## generate the common grid for all the chain or double chain
        ## generate chain properties list for the .json 
class NucleotChain():
    def __init__(self, pdbid):
        pass

    def clean_pdb(self):
        pass

    def split_nucleot(self): ## ???
        pass

    # give options to define color/texture by nucleotide or by gene
    def colors_textures(self):
        pass

    def genjson_nucleot(self):
        pass
