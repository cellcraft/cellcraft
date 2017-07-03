import numpy as np
import argparse
import logging
from mcpi.block import Block
#from cellcraft.connectors.minecraft_server import minecraft_connector
from cellcraft.builders.item import get_complex


def main(args):
    """
    Request from Minecraft to get the desired structure.
    Usage: python cellcraft.py -m (pdb|cellpack) -i <PDBid> -t <threshold> -s <blocksize> -l (load|nolo)
    :param args:
    :return:
    """

    try:
        # Extract the grid, colors and biological information from given structure
        bio_complex = get_complex(args.mode, args.name, args.size, args.threshold, args.usecache)
    except:
        logging.exception("Error loading structure.")
        raise
    import ipdb; ipdb.set_trace()

    try:
        minecraft_conn, minecraft_player_coordinates = minecraft_connector()
        complex_coordinates = (
            int(minecraft_player_coordinates.x), int(minecraft_player_coordinates.y + int(args.height)),
            int(minecraft_player_coordinates.z))
    except:
        logging.exception("Error getting player position.")
        raise

    try:
        if args.mode == 'cellpack':
            swap = False
        elif args.mode == 'pdb':
            swap = True
        add_numpy_array(minecraft_conn, bio_complex.grid, complex_coordinates, bio_complex.color, bio_complex.texture,
                        swap=swap)
    except:
        logging.exception("Error putting structures.")
        raise


# TODO: define this method more clearly and maybe move it to builders
def add_numpy_array(minecraft_conn, complex_grid, complex_coordinates, colors, texture, swap):
    """

    :param minecraft_conn:
    :param complex_grid:
    :param complex_coordinates:
    :param colors: dict with colors ids
    :param texture:
    :param swap:
    :return:
    """
    iterator = np.nditer(complex_grid, flags=['multi_index'], op_flags=['readonly'])
    while not iterator.finished:
        if iterator[0] > 0:
            x, y, z = iterator.multi_index
            if swap:
                height = complex_grid.shape[2]
                minecraft_conn.setBlock(complex_coordinates[0] + x, complex_coordinates[1] + (height - z),
                                        complex_coordinates[2] + y,
                                        Block(texture[int(iterator[0])], colors[int(iterator[0])]))
            else:
                minecraft_conn.setBlock(complex_coordinates[0] + x, complex_coordinates[1] + y,
                                        complex_coordinates[2] + z,
                                        Block(texture[int(iterator[0])], colors[int(iterator[0])]))
        iterator.iternext()


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
    main(args)
