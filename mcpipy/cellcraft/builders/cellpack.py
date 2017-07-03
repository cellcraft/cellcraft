"""
define features of ProteinComplexX3d(), input from CellPack
"""

import xml.etree.ElementTree as ET

import numpy as np
import pandas as pd
from cellcraft.builders.grid import create_bins_from_coordinates
# import math

default_dir = 'cellcraft/cellpack/'


def get_cellpack_complex(name, theta, blocksize, threshold):
    coor_df, item_info = get_cellpack_items(name)
    bin_count_df = create_bins_from_coordinates(
        coor_df, theta, blocksize, threshold, id_column='id')
    return bin_count_df, item_info


def get_cellpack_items(x3d_file):
    df = pd.read_csv(default_dir + x3d_file + '.csv')
    df.pdbid = df.pdbid.str.replace('\'', '')
    tree = ET.parse(default_dir + x3d_file + '.x3d')
    root = tree.getroot()
    transforms = root.find('Scene').find('Group').getchildren()
    # pdb_pat = re.compile('\d...')
    i = 0
    item_coordinates = []
    item_info = {}
    for transform in transforms:
        MetadataString = transform.find('MetadataString')
        if not MetadataString == None:
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

            item_df = pd.DataFrame(
                np.concatenate(all_points), columns=['x_coord', 'y_coord', 'z_coord'])
            item_df['id'] = i

            item_coordinates.append(item_df)

            item_info[i] = {
                'color': int(row.color),
                'texture': int(row.texture),
                'pdbid': row['pdbid']
            }

            i += 1
    return pd.concat(item_coordinates), item_info
