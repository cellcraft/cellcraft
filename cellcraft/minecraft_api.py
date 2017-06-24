import numpy as np
import pickle
import argparse
from mc import Block
from connectors.database import connect_mc
from builders.cellpack import add_cellpack
from builders.protein import add_pdb


def main(args):
    """
    Request from Minecraft to get the desired structure.
    Usage: python minecraft_api.py -m (pdb|cellpack) -i <PDBid> -t <threshold> -s <blocksize> -l (load|nolo)
    :param args:
    :return:
    """

    # TODO: Give arguments names to each of the methods correctly. Make the code easier to understand in each step
    mc, pos = connect_mc()
    if len(args) != 7:
        ValueError('Wrong number of arguments.')
    p0 = (int(pos.x), int(pos.y + int(args[5])), int(pos.z))
    if args[1] == 'pdb':
        if args[6] == 'load':
            array, colordict, texture = add_pdb(*args[2:5])
            pickle.dump((array, colordict, texture), open('_'.join(args[1:5]) + ".pkl", "wb"))
        else:
            array, colordict, texture = pickle.load(open('_'.join(args[1:5]) + ".pkl", "rb"))
        swap = True
    if args[1] == 'cellpack':
        swap = False
        if args[6] == 'load':
            array, colordict, texture = add_cellpack(*args[2:5])
            pickle.dump((array, colordict, texture), open('_'.join(args[1:5]) + ".pkl", "wb"))
        else:
            array, colordict, texture = pickle.load(open('_'.join(args[1:5]) + ".pkl", "rb"))
    add_numpy_array(mc, array, p0, colordict, texture, swap=swap)


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
        description='python minecraft_api.py -m (pdb|cellpack) -i <PDBid> -t <threshold> -s <blocksize> -l (load|nolo)')

    parser.add_argument('-m', '--mode', type=str, default='pdb',
                        help='Mode of source data, pdb for single structures of cellpack for complete environment.')
    parser.add_argument('-i', '--input', type=str, default=None,
                        help='If mode "pdb" then specify the Protein Data Bank id to use')
    parser.add_argument('-t', '--threshold', type=int, default=5,
                        help='Threshold of amount of atoms to consider a cell in the grid.')
    parser.add_argument('-s', '--size', type=float, default=5.5, help='Size of each block in the grid.')
    parser.add_argument('-l', '--loadmode', type=str, default='load',
                        help='Load mode for structures. Default load from source but if used before could be loaded from pickle structure.')

    args = parser.parse_args()
    main(args)
