import math, sys, gzip, os, os.path, glob, re, urllib, wget
import xml.etree.ElementTree as ET
from datetime import datetime, timedelta
from pymongo import MongoClient
from collections import *

from Bio.PDB import *
from Bio.SeqUtils.CheckSum import seguid
from Bio import SeqIO
from Bio import *
from Bio.Alphabet import IUPAC
from Bio.Seq import Seq
from xml.dom import minidom
import numpy as np

from cellcraft.src.item import *

path = ''

# colors EC id:color id
col = {'1':6, '2':1, '3':9, '4':2, '5':5, '6':4, '0':7}
# testure path name:texture id
text = defaultdict(list)
names = ['Metabolism', 'Genetic Information Processing', 'Human Diseases', 'Drug Development', 'Environmental Information Processing', 'Cellular Processes', 'Organismal Systems']
# texture 95 crystal, 159 full, 35 wool
textures = ['159', '35', '35', '35', '95', '95', '95']
for t,n in zip(textures,names):
    text[t].append(n)

# Define features for input object protein
class protein():
    # define protein info
    def __init__(self, pid, pdbin, chainId, GOs, EntrezIds, EnsemblIds, ECs, KOpathIDs, KPathways, dbname, GObioproc, GOmolefunt, GOcellcomp):
        self.pid = pid
        self.pdb_id = pdbin
        self.chainId = chainId
        self.GOs = GOs
        self.EntrezIds = EntrezIds
        self.EnsemblIds = EnsemblIds
        self.ECs = ECs
        self.KOpathIDs = KOpathIDs
        self.KPathways = KPathways
        self.dbname = dbname
        self.GObioproc = GObioproc
        self.GOmolefunt = GOmolefunt
        self.GOcellcomp = GOcellcomp

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
        if not hasattr(self, 'uniprotId'):
            if self.pdb_id == '4NCO':
                self.uniprotId = 'Q2N0S6'
            if self.pdb_id == '7HVP':
                self.uniprotId = 'P03369'

        # get Ids from Uniprot
        tree2 = ET.ElementTree(file=urllib.request.urlopen('http://www.uniprot.org/uniprot/'+self.uniprotId+'.xml'))
        root2 = tree2.getroot()
        namespace2 = re.match('\{.*\}', root2.tag).group()
        self.ref = [[ref.attrib['type'] for ref in info.findall(namespace2+'dbReference')] for info in root2.findall(namespace2+'entry')]
        self.refid = [[ref.attrib['id'] for ref in info.findall(namespace2+'dbReference')] for info in root2.findall(namespace2+'entry')]
        self.goval = [[[goname.attrib['value'] for goname in ref.findall(namespace2+'property')] for ref in info.findall(namespace2+'dbReference')] for info in root2.findall(namespace2+'entry')]
        b = 0
        while b < len(self.ref[0][:]):
            m = re.match("Ensembl.*", self.ref[0][b])
            # define KEGG Ids
            if self.ref[0][b] == 'KEGG':
                self.keggId = self.refid[0][b]
            # define GO terms
            elif self.ref[0][b] == 'GO':
                allcodes = []
                self.GOs.append(self.refid[0][b])
                # get the GO property = term value (C: cellular component, F: molecular fubction, P: biological processes)
                allcodes.append(self.goval[0][b])

                # print all the values that start with "P:"
                match1 = re.match('^P:.*', allcodes[0][0])
                match2 = re.match('^F:.*', allcodes[0][0])
                match3 = re.match('^C:.*', allcodes[0][0])
                if match1 != None:
                    self.GObioproc.append(allcodes[0][0][2:])
                # print all the values that start with "F:"
                elif match2 != None:
                    self.GOmolefunt.append(allcodes[0][0][2:])
                # print all the values that start with "C:"
                elif match3 != None:
                    self.GOcellcomp.append(allcodes[0][0][2:])



            # define gene Ids
            elif self.ref[0][b] == 'GeneID':
                self.EntrezIds.append(self.refid[0][b])
            elif self.ref[0][b] == 'EC':
                self.ECs.append('EC:'+self.refid[0][b])
            elif m != None:
                self.EnsemblIds.append(self.refid[0][b])
            b += 1

        # if not EC Id, give default EC:0.0.0.0 for non enzymatic protein
        if len(self.ECs) == 0:
            self.ECs.append('EC:0.0.0.0')

        # get Ids from KEGG
        while True:
            try:
                tree3 = urllib.request.urlopen('http://rest.kegg.jp/get/'+self.keggId)
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
                    fin = re.match(r'.*Enzymes \[(BR:'+self.keggId[:3]+'.*\])\n', line)
                    # get the name of the organism
                    if orgn != None:
                        self.Org = re.findall(self.keggId[:3]+' +(.*)\n', line)
                    # get the KO pathway Identifiers 1
                    elif pathId != None:
                        self.KOpathIDs.append(re.findall('.*('+self.keggId[:3]+'\d).*', line))
                        KO = 1
                    # fin of while
                    elif fin != None:
                        u = len(h)
                    # get the KEGG pathway 1
                    elif pathNa != None and fin != None:
                        KO = 0
                        BR = 1
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
                if not pathprov:
                    pathprov.append("Metabolism,Unknown")
                Kpathwaylist = [i.split(',') for i in pathprov]
                for patha, pathb in Kpathwaylist:
                    self.KPathways[patha].append(pathb)
                break
            # if there is not KEGG Id available give alternative values
            except (ValueError,RuntimeError, TypeError, NameError, AttributeError):
                self.keggId = 'Unknown'
                self.Org = 'Unknown'
                self.KOpathIDs.append('Unknown')
                self.KPathways['Metabolism'].append('Unknown')
                break


    # define color and texture for each prot
    def prot_color(self):
        # hack for 3J9U

        if self.pdb_id == '3J9U':
            cd = {'A':1,'B':5,'C':1,'D':5,'E':1,'F':5,'G':11,'H':11,'I':11,'J':11,'K':11,'L':11,'M':9,'N':9,
                  'O':4,'P':9,'Q':14,'R':4,'S':2,'T':4,'U':2,'V':4,'W':2,'X':4,'Y':2,'Z':4,'a':2,'b':4}
            print('_'+self.chainId+'_')
            self.color = cd[self.chainId]
        elif self.pdb_id == '2GLS':
            cd = {'A':1,'B':5,'C':1,'D':5,'E':1,'F':5,'G':11,'H':9,'I':11,'J':9,'K':11,'L':9}
            print('_'+self.chainId+'_')
            self.color = cd[self.chainId]
        else:
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
        rest = ([[texture for e in name if e == mypath] for texture, name in text.items()])
        nrest = [x for x in rest if x]
        self.texture = nrest[0][0]

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
    print('Get PDB.')
    Protcomplex = protein_complex(pdbin)
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


class protein_complex():
    def __init__(self, pdbin):
        self.pdb_id = pdbin

    # get pdb file from PDB database when not available
    def get_PDB(self):
        # Request pdb files from Protein Data bank
        PDB = 'http://www.rcsb.org/pdb/files/'+self.pdb_id+'.pdb'
        print(PDB)
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
        for pid,chain in enumerate(self.chains):
            GOs = []
            EntrezIds = []
            ENSEMBLids = []
            ECs = []
            KOpathIDs = []
            GObioproc = []
            GOmolefunt = []
            GOcellcomp = []
            KPathways = defaultdict(list)
            myprot = protein(pid,self.pdb_id, chain, GOs, EntrezIds, ENSEMBLids, ECs, KOpathIDs, KPathways,'try',GObioproc, GOmolefunt,GOcellcomp)
            # obtain IDs
            myprot.get_ids()
            myprot.prot_color()
            myprot.get_coord()
            self.proteins.append(myprot)

    def load_grid(self,threshold,blocksize):
        self.grid = cellcraft_grid(threshold,blocksize)
        for p in self.proteins:
            self.grid.add_coordinates(p.coord,p.pid)
        self.grid.make_grid()
        self.grid.def_blocks()
