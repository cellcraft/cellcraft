import logging

from cellcraft.builders.cellpack import get_cellpack_complex


def get_complex_from_source(mode, name, theta, blocksize, threshold, usecache):
    if mode == 'cellpack':
        bio_complex = get_cellpack_complex(name, theta, blocksize, threshold)
        logging.info("The cellpack {} was correctly loaded from source.".format(name))
    elif mode == 'pdb':
        # bio_complex = get_pdb_complex(name, theta, blocksize, threshold)
        logging.info("The pdb {} was correctly loaded from source.".format(name))
    else:
        raise ValueError('Unknown mode: {}'.format(mode))
    return bio_complex