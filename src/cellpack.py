import xml.etree.ElementTree as ET
import re
import numpy as np

default_dir = 'cellcraft/x3d/'

class protein_complex():
    def __init__(self, x3d_file):
        self.x3d_file = x3d_file

    def parse_file(self):
        tree = ET.parse(default_dir+self.x3d_file)
        root = tree.getroot()
        transforms = root.find('Scene').find('Group').getchildren()
        pdb_pat = re.compile('\d...')
        for transform in transforms:
            MetadataString  = transform.find('MetadataString')
            if MetadataString == None:
                continue
            if not MetadataString == None:
                MetadataString = MetadataString.attrib['value'].split('_')
                name = MetadataString[1]
                match = pdb_pat.match(MetadataString[2])
                if match:
                    pdb = match.group(0)
                else:
                    pdb = None
                shapes = transform.findall('Shape')
                for shape in shapes:
                    points = np.array(shape.find('IndexedTriangleSet').find('Coordinate').attrib['point'].split())
                    points = points.reshape((-1,3))
                    print(points)

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
