################
################ define features of Protein() and ProteinComplex()
################


import os
import os.path
import re
import urllib
import wget
import xml.etree.ElementTree as ET
from collections import *
from datetime import datetime, timedelta

import numpy as np
from Bio import *
from Bio.PDB import *
from pymongo import MongoClient

path = ''


############# TODO
### generate an algorithm that predicts color and texture of blocks taking into account a) biological features (GOterms) b) n_chains c) type of complex (prot complex, membrane, dna...) 
### it should be a method in ProteinComplex(), Membrane() and Dna() instead of particular of each item (Protein(),Lipid()...)

# colors EC id:color id
col = {'1':6, '2':1, '3':9, '4':2, '5':5, '6':4, '0':7}

# testure path name:texture id
text = defaultdict(list)
names = ['Metabolism', 'Genetic Information Processing', 'Human Diseases', 'Drug Development', 'Environmental Information Processing', 'Cellular Processes', 'Organismal Systems']

# texture 95 crystal, 159 full, 35 wool
textures = ['159', '35', '35', '35', '95', '95', '95']
for t,n in zip(textures,names):
    text[t].append(n)

##############


# Define features of each item in ProteinComplex and  
class Protein():
    # define potein biological info from scientific databases
    def __init__(self, pid, pdbin, chain_id, gos, entrez_ids, ensembl_ids, ECs, kopath_ids, kpathways, dbname, gobioproc, gomolefunt, gocellcomp):
        self.pid = pid
        self.pdbin = pdbin
        self.chain_id = chain_id
        self.gos = gos
        self.entrez_ids = entrez_ids
        self.ensembl_ids = ensembl_ids
        self.ecs = ecs
        self.kopath_ids = kopath_ids
        self.kpathways = kpathways
        self.dbname = dbname
        self.gobioproc = gobioproc
        self.gomolefunt = gomolefunt
        self.gocellcomp = gocellcomp

    # get coordinates out of pdb
    def get_coord(self):
        io = PDBIO()
        self.p = PDBParser()
        # sequence of aa 
        self.seq = self.p.get_structure(self.pdbin, 'clean_'+self.pdbin+'.pdb')

        # split pdb for different chains (items)
        io.set_structure(self.seq)
        io.save(self.pdbin+'_'+self.chain_id+'.pdb', ChainSelect(self.chain_id))
        self.chain = self.p.get_structure(self.pdbin+'_'+self.chain_id, self.pdbin+'_'+self.chain_id+'.pdb')

        # save coordinates in zeros.matrix of num_linesX3 dimension
        self.num_lines = sum(1 for line in open(self.pdbin+'_'+self.chain_id+'.pdb'))
        for line in open(self.pdbin+'_'+self.chain_id+'.pdb'):
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

    ############ TODO 
    ### define weigth array with specific weigths for atoms that need special importance (active site...) when parsed in the grid
    def atom_weigth(self):
        pass

    # get protein biological IDs from databases
    def get_ids(self):
        # get uniprot Id from PDB
        tree1 = ET.ElementTree(file=urllib.request.urlopen('http://www.rcsb.org/pdb/rest/das/pdb_uniprot_mapping/alignment?query='+self.pdbin))
        root = tree1.getroot()
        namespace = re.match('\{.*\}', root.tag).group()
        self.m = [[i.attrib['intObjectId'] for i in align.find(namespace+'block').findall(namespace+'segment')] for align in root.findall(namespace+'alignment')]
        a = 0
        while a < len(self.m):
            if self.m[a][0] == self.pdbin+'.'+self.chain_id:
                self.uniprot_id = self.m[a][1]
                a = len(self.m)
            else:
                a += 1

        ############## TODO
        ### exceptions from HIV cellpack model that will be removed when the code works fine
        if not hasattr(self, 'uniprotId'):
            if self.pdbin == '4NCO':
                self.uniprot_id = 'Q2N0S6'
            if self.pdbin == '7HVP':
                self.uniprot_id = 'P03369'

        # get IDs from Uniprot
        tree2 = ET.ElementTree(file=urllib.request.urlopen('http://www.uniprot.org/uniprot/'+self.uniprot_id+'.xml'))
        root2 = tree2.getroot()
        namespace2 = re.match('\{.*\}', root2.tag).group()
        self.ref = [[ref.attrib['type'] for ref in info.findall(namespace2+'dbReference')] for info in root2.findall(namespace2+'entry')]
        self.refid = [[ref.attrib['id'] for ref in info.findall(namespace2+'dbReference')] for info in root2.findall(namespace2+'entry')]
        self.goval = [[[goname.attrib['value'] for goname in ref.findall(namespace2+'property')] for ref in info.findall(namespace2+'dbReference')] for info in root2.findall(namespace2+'entry')]
        b = 0
        while b < len(self.ref[0][:]):
            m = re.match("Ensembl.*", self.ref[0][b])
            # define KEGG IDs
            if self.ref[0][b] == 'KEGG':
                self.kegg_id = self.refid[0][b]
            # define GO terms
            elif self.ref[0][b] == 'GO':
                allcodes = []
                self.gos.append(self.refid[0][b])
                # get the GO property = term value (C: cellular component, F: molecular fubction, P: biological processes)
                allcodes.append(self.goval[0][b])
                match1 = re.match('^P:.*', allcodes[0][0])
                match2 = re.match('^F:.*', allcodes[0][0])
                match3 = re.match('^C:.*', allcodes[0][0])
                if match1 != None:
                    self.gobioproc.append(allcodes[0][0][2:])
                elif match2 != None:
                    self.gomolefunt.append(allcodes[0][0][2:])
                elif match3 != None:
                    self.gocellcomp.append(allcodes[0][0][2:])

            # define gene IDs
            elif self.ref[0][b] == 'GeneID':
                self.entrez_ids.append(self.refid[0][b])
            elif self.ref[0][b] == 'EC':
                self.ecs.append('EC:'+self.refid[0][b])
            elif m != None:
                self.ensembl_ids.append(self.refid[0][b])
            b += 1

        # if not EC IDd, give default EC:0.0.0.0 for non enzymatic protein
        if len(self.ecs) == 0:
            self.ecs.append('EC:0.0.0.0')

        # get IDs from KEGG
        while True:
            try:
                tree3 = urllib.request.urlopen('http://rest.kegg.jp/get/'+self.kegg_id)
                h = [line for line in tree3]
                u = 0
                KO = 0
                BR = 0
                pathprov = []
                path1 = ''
                while u < len(h):
                    line = str(h[u], "utf-8")
                    orgn = re.match("^ORGANISM.*", line)
                    path_id = re.match("^PATHWAY.*", line)
                    path_na = re.match("^BRITE.*", line)
                    fin = re.match(r'.*Enzymes \[(BR:'+self.keggId[:3]+'.*\])\n', line)
                    # get the name of the organism
                    if orgn != None:
                        self.org = re.findall(self.kegg_id[:3]+' +(.*)\n', line)
                    # get the KO pathway Identifiers 1
                    elif path_id != None:
                        self.kopath_ids.append(re.findall('.*('+self.kegg_id[:3]+'\d).*', line))
                        KO = 1
                    elif fin != None:
                        u = len(h)
                    # get the KEGG pathway 1
                    elif path_na != None and fin != None:
                        KO = 0
                        BR = 1
                    elif KO == 1:
                        self.kopath_ids.append(re.findall('.*('+self.kegg_id[:3]+'\d....).*', line))
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
                if not pathprov:
                    pathprov.append("Metabolism,Unknown")
                kpathwaylist = [i.split(',') for i in pathprov]
                for patha, pathb in kpathwaylist:
                    self.kpathways[patha].append(pathb)
                break

            # if there is not KEGG Id available give alternative values
            except (ValueError,RuntimeError, TypeError, NameError, AttributeError):
                self.kegg_id = 'Unknown'
                self.org = 'Unknown'
                self.kopath_ids.append('Unknown')
                self.kpathways['Metabolism'].append('Unknown')
                break


    # define color and texture for each prot
    def prot_color(self):

        ############## TODO
        ### implement a method that gives features to the method for ProteinComplex() in order to find colors and textures for all chains in comples as explained at the beginning of the file
        if self.pdbin == '3J9U':
            cd = {'A':1,'B':5,'C':1,'D':5,'E':1,'F':5,'G':11,'H':11,'I':11,'J':11,'K':11,'L':11,'M':9,'N':9,
                  'O':4,'P':9,'Q':14,'R':4,'S':2,'T':4,'U':2,'V':4,'W':2,'X':4,'Y':2,'Z':4,'a':2,'b':4}
            print('_'+self.chain_id+'_')
            self.color = cd[self.chain_id]
        elif self.pdbin == '2GLS':
            cd = {'A':1,'B':5,'C':1,'D':5,'E':1,'F':5,'G':11,'H':9,'I':11,'J':9,'K':11,'L':9}
            print('_'+self.chain_id+'_')
            self.color = cd[self.chain_id]
        else:
            # define color by function (this will give features but not color directly)
            myEC = self.ecs[0][3:4]
            self.color = col[myEC]

        # define texture by pathway (this will give features but not texture directly)
        if len(self.kpathways) > 1:
            c = 0
            l = 0
            while l < len(self.kpathways):
                new = len(list(self.kpathways.values())[l])
                if new > c:
                    c = new
                    mypath = list(self.kpathways.keys())[l]
                l += 1
        else:
            mypath = list(self.kpathways.keys())[0]
        rest = ([[texture for e in name if e == mypath] for texture, name in text.items()])
        nrest = [x for x in rest if x]
        self.texture = nrest[0][0]

    ################ TODO
    ### define first the data structure we will use, the color and texture methods 
    ### define where to store it and utilities
    # generate and insert json for the protein collection
    def genjson_tomongo(self):
        client = MongoClient()
        self.db = client[self.dbname]
        protein = self.db['protein']
        self.pid = self.db.protein.insert({
            'pdbid':self.pdbin,
            'uniprotid':self.uniprot_id,
            'organism':self.org,
            'color':self.color,
            'keggid':self.kegg_id,
            'GOterms':self.gos,
            'ECs':self.ecs,
            'gEntrez':self.entrez_ids,
            'gEnsembl':self.ensembl_ids,
            'KOPaths':self.kopath_ids,
            'KPathways':self.kpathways,
            'texture':self.texture,
            'date':datetime.utcnow() + timedelta(hours=1)})
        #print(list(self.db.protein.find({'pdbid':self.pdb_id})))
        client.close()

    ################# TODO
    ### get the compounds ids for the Compounds() class that needs to be defined
    # define the compounds included in the pdb file
    def compounds_prot(self):
        # get KEEG_chemicals for that KEGG_id
        pass

    ################# TODO
    ### give the option in the feature to generate a model in the case the protein has gaps in the pdb
    # Generate a modell of the protein '/home/celsa/Documents/Pompeu Fabra/SBI/steps.txt'
    def model_prot(self):
        # input aa_seq from uniprot and aa_seq from chain in pdb file 
        print("1. Get seq of the protein \n2. Find other seqs similar \n3. Find structures \n3.a. Build modell \n3.b.1. Predict secondary structure in gap \n3.b.2. Build modell by secondary structure prediction")


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

# call from minecraft_api.py  
def add_pdb(pdbin,threshold,blocksize):
    print('Get PDB.')
    Protcomplex = ProteinComplex(pdbin)
    if os.path.isfile(pdbin+".pdb"):
        pass
    else:
        Protcomplex.get_PDB()
    print('Clean PDB.')
    Protcomplex.clean_pdb()
    print('Split Complex.')
    Protcomplex.split_complex()
    print('Load additional Info.')
    Protcomplex.load_chain_info()
    print('Make Grid.')
    Protcomplex.load_grid(int(threshold),int(blocksize))
    texture = {p.pid:p.texture for p in Protcomplex.proteins}
    color = {p.pid:p.color for p in Protcomplex.proteins}
    return Protcomplex.grid.values,color,texture

# split the protein complex and define features
class ProteinComplex():
    def __init__(self, pdbin):
        self.pdbin = pdbin

    # get pdb file from PDB database when not available in working directory
    def get_pdb(self):
        self.pdbin = self.pdbin.lower()
        pdb = 'http://www.rcsb.org/pdb/files/'+self.pdbin+'.pdb'
        print(pdb)
        h = wget.download(pdb, bar=None)

    # clean the pdb file from database
    def clean_pdb(self):
        # get only the chains from pdb
        self.p = PDBParser()
        self.seq = self.p.get_structure(self.pdbin, self.pdbin+".pdb")
        # clean the heteroatoms from pdb and save pdb as "clean_pdbid.pdb"
        io = PDBIO()
        io.set_structure(self.seq)
        io.save('clean_'+self.pdbin+'.pdb', NonHetSelect())

    # if several chains in the pdb file, split them
    def split_complex(self):
        # get list of chains in pdb
        ppd = PPBuilder()
        chs = defaultdict(list)
        fil = open(self.pdbin+'.fa', 'w')
        for pp in ppd.build_peptides(self.seq):
            for model in pp:
                for chain in model:
                    c = chain.get_full_id()
                    ch = c[2]
            a = pp.get_sequence()
            chs[ch].append(a)
        self.chains = chs.keys()

    # load data for each chain going through Protein()
    def load_chain_info(self):
        self.proteins = []
        for pid,chain in enumerate(self.chains):
            gos = []
            entrez_ids = []
            ensembl_ids = []
            ecs = []
            kopath_ids = []
            gobioproc = []
            gomolefunt = []
            gocellcomp = []
            kpathways = defaultdict(list)
            myprot = Protein(pid,self.pdbin, chain, gos, entrez_ids, ensembl_ids, ecs, kopath_ids, kpathways,'try',gobioproc, gomolefunt,gocellcomp)
            myprot.get_ids()
            myprot.prot_color()
            myprot.get_coord()
            self.proteins.append(myprot)

    # generate the common grid for the whole complex through CellcraftGrid() in item.py
    def load_grid(self,threshold,blocksize):
        self.grid = CellcraftGrid(threshold,blocksize)
        for p in self.proteins:
            self.grid.add_coordinates(p.coord,p.pid)
        self.grid.make_grid()
        self.grid.def_blocks()
