import math, sys, gzip, os, os.path, glob, re, urllib, wget
import xml.etree.ElementTree as ET
from datetime import datetime, timedelta
from pymongo import MongoClient
from collections import *
from grid import *
from Bio.PDB import *
from Bio.SeqUtils.CheckSum import seguid
from Bio import SeqIO
from Bio import *
from Bio.Alphabet import IUPAC
from Bio.Seq import Seq
from xml.dom import minidom
import numpy as np

# colors EC id:color id
col = {'1':'1', '2':'2', '3':'3', '4':'4', '5':'5', '6':'6', '7':'7'}
# testure path name:texture id
text = {'Metabolism':'76', 'Genetic Information Processing':'48', 'Environmental Information Processing':'7', 'Cellular Processes':'39', 'Organismal Systems':'67', 'Human Diseases':'3', 'Drug Development':'43'}

# Define features for input object protein
class protein():
    # define protein info
    def __init__(self, pdbin, chainId, GOs, EntrezIds, EnsemblIds, ECs, KOpathIDs, KPathways, dbname):
        self.pdb_id = pdbin
        self.chainId = chainId
        self.GOs = GOs
        self.EntrezIds = EntrezIds
        self.EnsemblIds = EnsemblIds
        self.ECs = ECs
        self.KOpathIDs = KOpathIDs
        self.KPathways = KPathways
        self.dbname = dbname

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

    # define weigth array with specific weigths for atoms that need special importance (active site...) when parsed in the grid
    def atom_weigth(self):
        # for the moment lets keep it as all the same weigth
        pass

    # get protein IDs
    def get_ids(self):
        # get uniprot Id from PDB
        tree1 = ET.ElementTree(file=urllib.request.urlopen('http://www.rcsb.org/pdb/rest/das/pdb_uniprot_mapping/alignment?query='+self.pdb_id))
        root = tree1.getroot()
        namespace = re.match('\{.*\}', root.tag).group()
        self.m = [[i.attrib['intObjectId'] for i in align.find(namespace+'block').findall(namespace+'segment')] for align in root.findall(namespace+'alignment')]
        a = 0
        while a < len(self.m):
            if self.m[a][0] == self.pdb_id+'.'+self.chainId:
                self.uniprotId = self.m[a][1]
                a = len(self.m)
            else:
                a += 1

        # get Ids from Uniprot
        tree2 = ET.ElementTree(file=urllib.request.urlopen('http://www.uniprot.org/uniprot/'+self.uniprotId+'.xml'))
        root2 = tree2.getroot()
        namespace2 = re.match('\{.*\}', root2.tag).group()
        self.ref = [[ref.attrib['type'] for ref in info.findall(namespace2+'dbReference')] for info in root2.findall(namespace2+'entry')]
        self.refid = [[ref.attrib['id'] for ref in info.findall(namespace2+'dbReference')] for info in root2.findall(namespace2+'entry')]
        b = 0
        while b < len(self.ref[0][:]):
            m = re.match("Ensembl.*", self.ref[0][b])
            # define KEGG Ids
            if self.ref[0][b] == 'KEGG':
                self.keggId = self.refid[0][b]
            # define GO terms
            elif self.ref[0][b] == 'GO':
                self.GOs.append(self.refid[0][b])
            # define gene Ids
            elif self.ref[0][b] == 'GeneID':
                self.EntrezIds.append(self.refid[0][b])
            elif self.ref[0][b] == 'EC':
                self.ECs.append('EC:'+self.refid[0][b])
            elif m != None:
                self.EnsemblIds.append(self.refid[0][b])
            b += 1

        # get Ids from KEGG
        tree3 = urllib.request.urlopen('http://rest.kegg.jp/get/'+self.keggId)
            b += 1       
        h = [line for line in tree3]
        u = 0
        KO = 0
        BR = 0
        pathprov = []
        path1 = ''
        while u < len(h):
            line = str(h[u], "utf-8")
            orgn = re.match("^ORGANISM.*", line)
            pathId = re.match("^PATHWAY.*", line)
            pathNa = re.match("^BRITE.*", line)
            fin = re.match(r'.*\[(BR:'+self.keggId[:3]+'.*\])\n', line)
            # get the name of the organism
            if orgn != None:
                self.Org = re.findall(self.keggId[:3]+' +(.*)\n', line)
            # get the KO pathway Identifiers 1
            elif pathId != None:
                self.KOpathIDs.append(re.findall('.*('+self.keggId[:3]+'\d).*', line))
                KO = 1
            # get the KEGG pathway 1
            elif pathNa != None:
                KO = 0
                BR = 1
            # fin of while
            elif BR == 1 and fin != None:
                BR = 0 
                u = len(h)
            # start repetition for KO pathway identifiers    
            elif KO == 1:
                self.KOpathIDs.append(re.findall('.*('+self.keggId[:3]+'\d....).*', line))
            # start repetition for KEGG pathway
            elif BR == 1:
                what = re.match("\S", line[14])
                main = re.match("\w", line[13])
                if main != None:
                    path1 = re.findall('(\S.*)\n', line)[0]
                elif main == None:
                    if what != None:
                        path2 = re.findall('(\S.*)\n', line)[0]
                        if path2 != 'Overview':
                            pathprov.append(path1+','+path2)
            u += 1
        # get the dictionary for KEGG Pathway out of pathprov
        Kpathwaylist = [i.split(',') for i in pathprov]         
        for patha, pathb in Kpathwaylist:
            self.KPathways[patha].append(pathb) 
        # if not EC Id, give default EC:0.0.0.0 for non enzymatic protein
        if len(self.ECs) <= 1 and len(self.ECs[0]) == 0:
            self.ECs[0] = 'EC:0.0.0.0'

    # define color and texture for each prot
    def prot_color(self):
        # define color by function
        myEC = self.ECs[0][3:4] 
        self.color = col[myEC]

        # define texture by pathway
        if len(self.KPathways) > 1:
            c = 0
            l = 0
            while l < len(self.KPathways):
                new = len(list(self.KPathways.values())[l])
                if new > c:
                    c = new
                    mypath = list(self.KPathways.keys())[l]
                l += 1
        else:
            mypath = list(self.KPathways.keys())[0]
        self.texture = text[mypath]

    # generate and insert json for the protein collection
    def genjson_tomongo(self):
        client = MongoClient()
        self.db = client[self.dbname]
        protein = self.db['protein']
        self.pid = self.db.protein.insert({
            'pdbid':self.pdb_id,
            'uniprotid':self.uniprotId,
            'organism':self.Org,
            'color':self.color,
            'keggid':self.keggId,
            'GOterms':self.GOs,
            'ECs':self.ECs,
            'gEntrez':self.EntrezIds,
            'gEnsembl':self.EnsemblIds,
            'KOPaths':self.KOpathIDs,
            'KPathways':self.KPathways,
            'texture':self.texture,
            'date':datetime.utcnow() + timedelta(hours=1)})
        #print(list(self.db.protein.find({'pdbid':self.pdb_id})))
        client.close()

    # define the ligands, inhibitors, effectors...
    def compounds_prot(self):
        # get KEEG_chemicals for that KEGG_id
        pass

    # Generate a modell of the protein '/home/celsa/Documents/Pompeu Fabra/SBI/steps.txt'
    def model_prot(self):
        # development in further steps when aa_seq_pdb != aa_seq 
        print("1. Get seq of the protein \n2. Find other seqs similar \n3. Find structures \n3.a. Build modell \n3.b.1. Predict secondary structure in gap \n3.b.2. Build modell by secondary structure prediction")

    # clean the working directory of files generated that not more useful
    #def clean_dir(self):
    #    patterns = [self.pdb_id+'_'+self.chainId+'.pdb$', '.*'+self.pdb_id+'.pdb', self.pdb_id+'.fa']
    #    mypath = "./"
    #    for root, dirs, files in os.walk(mypath):
    #        for i in patterns:
    #            if re.findall(i,files) != None:
    #                for file in filter(lambda x: re.findall(i, x), files):
    #                    os.remove(os.path.join(root, file))

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

def add_pdb(pdbin,threshold,blocksize):
    Protcomplex = protein_complex(pdbin)
    if os.path.isfile(path+pdbin+".pdb"):
        pass
    else:
        Protcomplex.get_PDB()
    Protcomplex.clean_pdb()
    Protcomplex.split_complex()
    Protcomplex.load_chain_info()
    Protcomplex.load_grid(threshold,blocksize)
    return Protcomplex.grid.values,{p.pid:i for i,p in enumerate(Protcomplex.proteins)}


class protein_complex():
    def __init__(self, pdbin):
        self.pdb_id = pdbin

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
        fil = open(self.pdb_id+'.fa', 'w')
        for pp in ppd.build_peptides(self.seq):
            for model in pp:
                for chain in model:
                    c = chain.get_full_id()
                    ch = c[2]
            a = pp.get_sequence()
            chs[ch].append(a)
        self.chains = chs.keys()

    def load_chain_info(self):
        self.proteins = []
        for i in self.chains:
            GOs = []
            EntrezIds = []
            ENSEMBLids = []
            ECs = []
            KOpathIDs = []
            KPathways = defaultdict(list)
            myprot = protein(pdbin, chain, GOs, EntrezIds, ENSEMBLids, ECs, KOpathIDs, KPathways,'try')
            # obtain IDs
            myprot.get_ids()
            myprot.prot_color()
            myprot.genjson_tomongo()
            self.proteins.append(myprot)

    def load_grid(self,threshold,blocksize):
        self.grid = cellcraft_grid(threshold,blocksize)
        for protein in self.proteins:
            self.grid.add_coordinates(protein.get_coord(),protein.pid)
        self.grid.make_grid()
        self.grid.def_blocks()
