################
################ define features of ProteinComplexX3d(), input from CellPack
################


import re
import xml.etree.ElementTree as ET

import numpy as np
import pandas as pd
from cellcraft.builders.complex_structure import ComplexStructure

default_dir = 'x3d/'


class SimpleProtein():
    def __init__(coordinates, color, texture, id):
        self.coordinates = coordinates
        self.color = color
        self.texture = texture
        self.id = id


class ProteinComplexX3d(ComplexStructure):
    def __init__(self, name, threshold, blocksize):
        self.x3d_file = name
        self.parse_file()
        self.textures = {p.pid: p.texture for p in self.items}
        self.colors = {p.pid: p.color for p in self.items}
        self.grid = self.create_grid_from_items(blocksize, threshold)

    ################ TODO
    ### generate a method to parse each element of the cellpack in the .csv through Protein/Lipid class in order to get biological info for the .json

    def parse_file(self):
        df = pd.read_csv(default_dir + self.x3d_file + '.csv')
        df.pdbid = df.pdbid.str.replace('\'', '')
        tree = ET.parse(default_dir + self.x3d_file + '.x3d')
        root = tree.getroot()
        transforms = root.find('Scene').find('Group').getchildren()
        # pdb_pat = re.compile('\d...')
        i = 0
        self.items = []
        for transform in transforms:
            MetadataString = transform.find('MetadataString')
            if MetadataString:
                # MetadataString = MetadataString.attrib['value'].split('_')
                row = df.iloc[i]

                # name = MetadataString[1]
                # match = pdb_pat.match(MetadataString[2])
                # if match:
                #     pdb = match.group(0)
                # else:
                #     pdb = None

                shapes = transform.findall('Shape')
                all_points = []
                for shape in shapes[::int(row.take_every)]:
                    points = np.array(
                        shape.find('IndexedTriangleSet').find('Coordinate').attrib['point'].split(),
                        dtype=float)
                    all_points.append(points.reshape((-1, 3)))
                if i == 22:
                    mean = all_points[0].mean(axis=0)
                    radius = np.sqrt(((all_points[0] - mean) ** 2).mean())
                    vecs = np.random.normal(size=(100000, 3))
                    mags = np.linalg.norm(vecs, axis=-1)

                    more_points = (vecs / mags[..., np.newaxis] * radius) + mean
                    all_points.append(more_points)
                self.items.apend(SimpleProtein(
                    coordinates=np.concatenate(all_points),
                    color=int(row.color),
                    texture=int(row.texture),
                    id=i
                ))
                i += 1
