import xml.etree.ElementTree as ET
import re
import numpy as np
import pandas as pd
from cellcraft.src.item import *

default_dir = 'x3d/'

def add_cellpack(x3d_file,threshold,blocksize):
    Protcomplex = protein_complex_x3d(x3d_file)
    Protcomplex.parse_file()
    Protcomplex.load_grid(int(threshold),int(blocksize))
    return Protcomplex.grid.values,Protcomplex.colordict,Protcomplex.texture

class protein_complex_x3d():
    def __init__(self, x3d_file):
        self.x3d_file = x3d_file
        self.surfaces = []
        self.pids = []
        self.colors = []
        self.colordict = {}
        self.texture = {}

    def load_grid(self,threshold,blocksize):
        self.grid = cellcraft_grid(threshold,blocksize)
        for pid,surface in zip(self.pids,self.surfaces):
            self.grid.add_coordinates(surface,pid)
        self.grid.make_grid()
        self.grid.def_blocks()

    def parse_file(self):
        df = pd.read_csv(default_dir+self.x3d_file+'.csv')
        df.pdbid = df.pdbid.str.replace('\'', '')
        tree = ET.parse(default_dir+self.x3d_file+'.x3d')
        root = tree.getroot()
        transforms = root.find('Scene').find('Group').getchildren()
        pdb_pat = re.compile('\d...')
        i = 0
        for transform in transforms:
            MetadataString  = transform.find('MetadataString')
            if not MetadataString == None:
                MetadataString = MetadataString.attrib['value'].split('_')
                row = df.iloc[i]

                self.pids.append(i)
                self.colordict[i] = int(row.color)
                self.texture[i] = int(row.texture)

                name = MetadataString[1]
                match = pdb_pat.match(MetadataString[2])
                if match:
                    pdb = match.group(0)
                else:
                    pdb = None

                shapes = transform.findall('Shape')
                all_points = []
                for shape in shapes[::int(row.take_every)]:
#                for shape in shapes:
                    points = np.array(shape.find('IndexedTriangleSet').find('Coordinate').attrib['point'].split(),dtype=float)
                    all_points.append(points.reshape((-1,3)))
                if i == 22:
                    mean = all_points[0].mean(axis=0)
                    radius = np.sqrt(((all_points[0] - mean)**2).mean())
                    vecs = np.random.normal(size=(100000,3))
                    mags = np.linalg.norm(vecs, axis=-1)

                    more_points = (vecs / mags[..., np.newaxis] * radius)+mean
                    all_points.append(more_points)

                self.surfaces.append(np.concatenate(all_points))
                i += 1
