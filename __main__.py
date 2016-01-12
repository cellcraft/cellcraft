import math, sys, gzip, os, os.path, glob, wget, urllib, sqlite3, datetime
from collections import *
from pymongo import MongoClient
from Bio.PDB import *
from Bio.SeqUtils.CheckSum import seguid
from Bio import SeqIO
from Bio import *
from Bio.Alphabet import IUPAC
from Bio.Seq import Seq
from xml.dom import minidom
import numpy as np

# import other methods of cellcraft
from src.protein import *
from src.item import *
from src.envelope import *
from src.lipid import *
from src.nucleotide import *
from src.compounds import *
from src.usage import *
from src.errorcheck import *

path = "./"
dbname = 'try'
inpformat = sys.argv[1]
clean = True

# generate item protein
if inpformat == "-pdbprot":
    # create an instance with a prot/prot complex
    pdbin = sys.argv[2]
    myProtcomplex = protein_complex(pdbin)
    if os.path.isfile(path+pdbin+".pdb"):
        pass
    else:
        myProtcomplex.get_PDB()
    myProtcomplex.clean_pdb()
    myProtcomplex.split_complex()
    listchains = myProtcomplex.chains

    # for each protein in PDB
    for i in listchains:
        GOs = []
        EntrezIds = []
        ENSEMBLids = []
        ECs = []
        KOpathIDs = []
        KPathways = defaultdict(list)
        myprot = protein(pdbin, i, GOs, EntrezIds, ENSEMBLids, ECs, KOpathIDs, KPathways, dbname)

        # obtain matrix of coordenates
#        myprot.get_coord()
#        mymatrix = myprot.coord
#        numatoms = myprot.num_lines

#        # obtain grid
#        mygrid = item_cellcraft(mymatrix,1,1)
#        mygrid.vol_prot()
#        mygrid.def_blocks()
#        output = mygrid.H

        # obtain IDs
        myprot.get_ids()
        pdbid = myprot.pdb_id
        uniprotid = myprot.uniprotId
        keggid = myprot.keggId
        GOterms = myprot.GOs
        ECs = myprot.ECs
        Org = myprot.Org
        gEntrez = myprot.EntrezIds
        gEnsembl = myprot.EnsemblIds
        KOpaths = myprot.KOpathIDs
        KPaths = myprot.KPathways
        print(uniprotid)
        print("GOterms",GOterms)
        print("ECs",ECs)
        print("Organism",Org)
        print("KOpaths",KOpaths)
        print("Keggpaths",KPaths)

        # get color and texture
        myprot.prot_color()
        color = myprot.color
        text = myprot.texture
        print(pdbid,',',color,',',text,',',KPaths,',',ECs)
 
        # insert a json collection for each protein
        #myprot.genjson_tomongo()  
        #db = myprot.db 
        
        # clean if desired the not useful generated files
        #myprot.clean_dir()

    # create an instance with a lipid/membrane
    #myLipmembrane = membrane(pdbin)
    #myLipmembrane.clean_pdb()
    #myLipmembrane.split_lipids()
    #listlips = myLipmembrane.listlip

    # for each lipid in PDB
    #for i in listlips:
         # obtain matrix of coordenates

         # obtain grid

elif inpformat == "-autopack":
    print("Here new protokol to get matrix with coordenates")

elif inpformat == '-memb':
    print("Here new protokol for lipid membrane")

elif inpformat == '-nucleot':
    print("Here new protokol for nucleotides")
