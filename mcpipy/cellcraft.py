import numpy as np
import argparse
import logging
from mcipy.block import Block
from cellcraft.connectors.connectors import minecraft_connector
from cellcraft.builders.items import get_complex


def main(args):
    """
    Request from Minecraft to get the desired structure.
    Usage: python cellcraft.py -m (pdb|cellpack) -i <PDBid> -t <threshold> -s <blocksize> -l (load|nolo)
    :param args:
    :return:
    """

    # if mode pdb get single biomolecule structure

    try:
        cmpx = get_complex(mode, name, size, threshold, usecache)
    except:
        logging.exception("Error loading structure.")
        raise

    try:
        mc, pos = minecraft_connector()
        p0 = (int(pos.x), int(pos.y + int(args.height)), int(pos.z))
    except:
        logging.exception("Error getting player position.")
        raise

    try:
        if mode == 'cellpack':
            swap = False
        elif mode == 'pdb':
            swap = True
        add_numpy_array(mc, cmpx.grid, p0, cmpx.color, cmpx.texture, swap=swap)
    except:
        logging.exception("Error putting structures.")
        raise


# TODO: define this method more clearly and maybe move it to builders
def add_numpy_array(mc, array, p0, colordict, texture, swap):
    it = np.nditer(array, flags=['multi_index'], op_flags=['readonly'])
    while not it.finished:
        if it[0] > 0:
            x, y, z = it.multi_index
            if swap:
                height = array.shape[2]
                mc.setBlock(p0[0] + x, p0[1] + (height - z), p0[2] + y,
                            Block(texture[int(it[0])], colordict[int(it[0])]))
            else:
                mc.setBlock(p0[0] + x, p0[1] + y, p0[2] + z, Block(texture[int(it[0])], colordict[int(it[0])]))
        it.iternext()


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description='python cellcraft.py -n name -m (pdb|cellpack) -t <threshold> -s <blocksize> [--no-cache]')

    parser.add_argument('-m', '--mode', type=str, default='pdb',
                        help='Mode of source data, pdb for single structures of cellpack for complete environment.')
    parser.add_argument('-n', '--name', type=str, default=None,
                        help='If mode "pdb" then specify the Protein Data Bank id to use')
    parser.add_argument('-t', '--threshold', type=int, default=5,
                        help='Threshold of amount of atoms to consider a cell in the grid.')
    parser.add_argument('-s', '--size', type=float, default=5.5, help='Size of each block in the grid.')
    parser.add_argument('-he', '--height', type=float, default=15,
                        help='Height of the starting position to build structure.')
    parser.add_argument('-C', '--no-cache', dest='usecache', action='store_false',
                        help='Do not load structure from local cache.')

    args = parser.parse_args()
    main(**args)
