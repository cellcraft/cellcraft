"""
define features of CellcraftGrid()
"""
import os
from collections import OrderedDict
import pickle
from cellcraft.config import PATH_CACHE
from cellcraft.builders.cellpack import get_cellpack_complex
from cellcraft.builders.protein import get_pdb_complex
import logging


class CellcraftGridStore():
    def __init__(self, cache_dir=PATH_CACHE):
        self.cache_dir = cache_dir

    def check_if_in_cache(self, **keys):
        file_name = self.create_file_name(**keys)
        path = self.get_path_to_cache(file_name)
        return os.path.isfile(path)

    def get_from_cache(self, **keys):
        file_name = self.create_file_name(**keys)
        return self._get_from_cache(file_name)

    def _get_from_cache(self, file_name):
        path = self.get_path_to_cache(file_name)
        with open(path, 'rb') as f:
            return pickle.load(f)

    def put_on_cache(self, obj, **keys):
        file_name = self.create_file_name(**keys)
        return self._put_on_cache(obj, file_name)

    def _put_on_cache(self, obj, file_name):
        path = self.get_path_to_cache(file_name)
        with open(path, 'wb') as f:
            pickle.dump(obj, f)

    def create_file_name(self, **keys):
        keys = OrderedDict(sorted(keys.items(), key=lambda t: t[0]))
        file_name = '__'.join(['{}_{}'.format(k, parse_list_to_string(v)) for k, v in keys.items()])
        return file_name

    def get_path_to_cache(self, file_name):
        return self.cache_dir + file_name + '.pkl'


def get_complex_from_source(mode, name, theta, blocksize, threshold):
    if mode == 'cellpack':
        try:
            bio_complex = get_cellpack_complex(name, theta, blocksize, threshold)
            logging.info("The cellpack {} was correctly loaded from source.".format(name))
        except Exception as exp:
            logging.exception("The cellpack {} can not be loaded from source.".format(name))
    elif mode == 'pdb':
        try:
            bio_complex = get_pdb_complex(name, theta, blocksize, threshold)
            logging.info("The pdb {} was correctly loaded from source.".format(name))
        except Exception as exp:
            logging.exception("The pdb {} can not be loaded from source.".format(name))
    else:
        raise ValueError('Unknown mode: {}'.format(mode))
    return bio_complex


def get_complex(mode, name, theta, blocksize, threshold, usecache, path=PATH_CACHE):
    # check for complex in cache
    cgs = CellcraftGridStore(path)
    cached = cgs.check_if_in_cache(
        mode=mode, name=name, theta=theta, blocksize=blocksize, threshold=threshold)
    if cached and usecache:
        bio_complex = cgs.get_from_cache(
            mode=mode, name=name, theta=theta, blocksize=blocksize, threshold=threshold)
        logging.info("The structure {} was correctly loaded from store.".format(name))
    else:
        bio_complex = get_complex_from_source(mode, name, theta, blocksize, threshold)
        cgs.put_on_cache(
            bio_complex, mode=mode, name=name, theta=theta, blocksize=blocksize, 
            threshold=threshold)
        logging.info("The structure {} was correctly stored.".format(name))
    return bio_complex


def parse_list_to_string(list_elements):
    if isinstance(list_elements, list):
        string = "_".join(str(x) for x in list_elements)
    else:
        string = list_elements
    return string