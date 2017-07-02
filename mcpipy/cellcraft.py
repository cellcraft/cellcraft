import numpy as np
import pickle
import argparse
import logging
from mcpi.block import Block
from cellcraft.connectors.db_connectors import
from cellcraft.connectors.minecraft_server import minecraft_connector
from cellcraft.builders.cellpack import add_cellpack
from cellcraft.builders.protein import add_pdb


def main(args):
    """
    Request from Minecraft to get the desired structure.
    Usage: python cellcraft.py -m (pdb|cellpack) -i <PDBid> -t <threshold> -s <blocksize> -l (load|nolo)
    :param args:
    :return:
    """

    # if mode pdb get single biomolecule structure
    array = []
    if args.mode == 'pdb':

        # if loading mode "load", require call from sources
        if args.loadmode == 'load':
            try:
                # call the source
                array, colordict, texture = add_pdb(*[args.input, args.threshold, args.size])
                pickle.dump((array, colordict, texture), open("cellcraft/cache/" + '_'.join(
                    [args.mode, args.input, str(args.threshold), str(args.size)]) + ".pkl", "wb"))
                logging.info("The structure {} was correctly loaded from source and pickled.".format(args.input))

            except Exception as exp:
                logging.exception(
                    "It was not possible to connect to the structure source API. Try later or load pickle structures.")

        elif args.loadmode == 'nolo':
            try:
                # try to load structure from local pickel
                print('_'.join([args.mode, args.input, str(args.threshold), str(args.size)]) + ".pkl")
                array, colordict, texture = pickle.load(
                    open("cellcraft/cache/" + '_'.join(
                        [args.mode, args.input, str(args.threshold), str(args.size)]) + ".pkl", "rb"))
                logging.info("The structure {} was correctly loaded from pickle.".format(args.input))

            except Exception as exp:
                swap = True
                logging.exception("The required estructure is not pickeled yet. You may have to load it from source.")

        else:
            raise ValueError(
                "Unknown loading mode: {}. The possible options are 'load' or 'nolo'.".format(args.loadmode))

    # if mode pdb get complete system structure
    elif args.mode == 'cellpack':
        swap = False

        # if loading mode require call from sources
        if args.loadmode == 'load':
            try:
                array, colordict, texture = add_cellpack(*args[args.input, args.threshold, args.size])
                pickle.dump((array, colordict, texture),
                            open("cellcraft/cache/" + '_'.join(
                                [args.mode, args.input, str(args.threshold), str(args.size)]) + ".pkl",
                                 "wb"))
                logging.info("The structure {} was correctly loaded from source and pickled.".format(args.input))

            except Exception as exp:
                logging.exception(
                    "It was not possible to connect to the structure source API. Try later or load pickle structures.")
        elif args.loadmode == 'nolo':
            try:
                array, colordict, texture = pickle.load(
                    open("cellcraft/cache/" + '_'.join([args.mode, args.input, args.threshold, args.size]) + ".pkl",
                         "rb"))
                logging.info("The structure {} was correctly loaded from pickle.".format(args.input))

            except Exception as exp:
                logging.exception("The required estructure is not pickeled yet. You may have to load it from source.")
        else:
            logging.info("Please, specify the load mode desired.")

    if len(array) > 0:
        mc, pos = minecraft_connector()
        p0 = (int(pos.x), int(pos.y + int(args.height)), int(pos.z))
        add_numpy_array(mc, array, p0, colordict, texture, swap=swap)

        # save structure in mongo database



# TODO: define this method more clearly and maybe move it to helpers
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
        description='python cellcraft.py -m (pdb|cellpack) -i <PDBid> -t <threshold> -s <blocksize> -h <height> -l (load|nolo)')

    parser.add_argument('-m', '--mode', type=str, default='pdb',
                        help='Mode of source data, pdb for single structures of cellpack for complete environment.')
    parser.add_argument('-i', '--input', type=str, default=None,
                        help='If mode "pdb" then specify the Protein Data Bank id to use')
    parser.add_argument('-t', '--threshold', type=int, default=5,
                        help='Threshold of amount of atoms to consider a cell in the grid.')
    parser.add_argument('-s', '--size', type=float, default=5.5, help='Size of each block in the grid.')
    parser.add_argument('-he', '--height', type=float, default=15,
                        help='Height of the starting position to build structure.')
    parser.add_argument('-l', '--loadmode', type=str, default='load',
                        help='Load mode for structures. Default load from source but if used before could be loaded from pickle structure.')

    args = parser.parse_args()
    main(args)
