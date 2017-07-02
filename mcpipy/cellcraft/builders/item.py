################
################ define features of CellcraftGrid()
################

import numpy as np
import os
from collections import OrderedDict
import pickle
from cellcraft.builders.protein import ProteinComplex
from cellcraft.builders.cellpack import ProteinComplexX3d
import logging


class CellcraftGridStore():
    def __init__(self, cache_dir='cache/'):
        self.cache_dir = cache_dir

    def check(self, **keys):
        key = self.create_key(**keys)
        fn = self.get_path(key)
        os.path.isfile(fn)

    def get(self, **keys):
        key = self.create_key(**keys)
        return self._get(key)

    def _get(self, key):
        fn = self.get_path(key)
        with open(fn, 'r') as f:
            pickle.load(f)

    def put(self, obj, **keys):
        key = self.create_key(**keys)
        return self._put(obj, key)

    def _put(self, obj, key):
        fn = self.get_path(key)
        with open(fn, 'w') as f:
            pickle.dumbs(obj, f)

    def create_key(self, **keys):
        keys = OrderedDict(sorted(keys.items(), key=lambda t: t[0]))
        key = '__'.join(['{}_{}'.format(k, v) for k, v in keys.items()])
        return key

    def get_path(self, key):
        return self.cache_dir + key + '.pkl'


cgs = CellcraftGridStore()


def get_complex(self, mode, name, blocksize, threshold, usecache):
    # check for complex in cache
    cached = cgs.check(mode=mode, name=name, blocksize=blocksize, threshold=threshold)
    if cached and usecache:
        cmpx = cgs.get(mode=mode, name=name, blocksize=blocksize, threshold=threshold)
        logging.info("The structure {} was correctly loaded from store.".format(name))     
    else:
        if mode == 'cellpack':
            cmpx = ProteinComplexX3d(name, blocksize, threshold)
            logging.info("The cellpack {} was correctly loaded from source.".format(name))    
        elif mode == 'pdb':
            cmpx = ProteinComplex(name, blocksize, threshold)
            logging.info("The pdb {} was correctly loaded from source.".format(name))    
        else:
            raise ValueError('Unknown mode: {}'.format(mode))
        cgs.put(cmpx, mode=mode, name=name, blocksize=blocksize, threshold=threshold)
        logging.info("The structure {} was correctly stored.".format(name))    
    return cmpx


class Complex():
    def __init__():
        pass

    def create_grid_from_items(self, blocksize, threshold):
        """
        :param item:        dict with 
        :param blocksize:
        :param threshold: 
        :return:
        """
        all_coor = [i.coordinates for i in self.items]
        grid = self.init_grid(all_coor, blocksize)
        shape = [len(d) - 1 for d in grid]
        return self.create_grid(grid, shape, threshold)

    def init_grid(self, coordinates, blocksize):
        amax = np.amax([np.amax(coor, axis=0) for coor in coordinates], axis=0)
        amin = np.amin([np.amin(coor, axis=0) for coor in coordinates], axis=0)
        x = np.arange(amin[0], amax[0] + blocksize, blocksize)
        y = np.arange(amin[1], amax[1] + blocksize, blocksize)
        z = np.arange(amin[2], amax[2] + blocksize, blocksize)
        return x, y, z

    def create_grid(self, grid, shape, threshold):
        values = np.zeros(shape)
        for item in self.items:
            H, _ = np.histogramdd(item.coordinates, bins=grid)
            values[H >= threshold] = item.id
        return values
