import numpy as np
import argparse
import logging
from cellcraft.connectors.minecraft_server import minecraft_connector, add_numpy_array_to_minecraft
from cellcraft.builders.cache import get_complex
from cellcraft.builders.protein import store_location_biological_prot_data


def main(args):
    """
    Request from Minecraft to get the desired structure.
    Usage: python cellcraft.py -n name -m (pdb|cellpack) -th [int int int] -t <threshold> -s <blocksize> [--no-cache]
    :param args:
    :return:
    """

    try:
        # Extract the grid, colors and biological information from given structure
        bio_complex = get_complex(args.mode, args.name, args.theta, args.size, args.threshold, args.usecache)
        logging.info("The structure {} was successfully loaded.".format(args.name))
    except Exception as exp:
        logging.exception("Error loading structure.")
        raise

    try:
        minecraft_conn, minecraft_player_coordinates = minecraft_connector()
        complex_coordinates = np.array(
            [int(minecraft_player_coordinates.x),
             int(minecraft_player_coordinates.y) + int(args.height),
             int(minecraft_player_coordinates.z)])
        logging.info("The coordinates of the player {} where successfully obtained.".format(complex_coordinates))
    except Exception as exp:
        logging.exception("Error extracting player position coordinates.")
        raise

    try:
        add_numpy_array_to_minecraft(minecraft_conn, complex_coordinates, bio_complex)
        logging.info("Structure successfully transformed into blocks and loaded into Minecraft.")
    except Exception as exp:
        logging.exception("Error throwing structures into the minecraft server.")
        raise

    if args.mode is "pdb":
        try:
            data_dict = store_location_biological_prot_data(complex_coordinates, args.name)
            logging.info("Data correctly stored in server: {}".format(data_dict))
        except Exception as exp:
            logging.exception("Error while sending data to server.")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description='python cellcraft.py -n name -m (pdb|cellpack) -th [int int int] -t <threshold> -s <blocksize> [--no-cache]')

    parser.add_argument('-m', '--mode', type=str, default='pdb',
                        help='Mode of source data, pdb for single structures of cellpack for complete environment.')
    parser.add_argument('-n', '--name', type=str, default=None,
                        help='If mode "pdb" then specify the Protein Data Bank id to use')
    parser.add_argument('-th', '--theta', type=int, nargs=3, default=[0, 0, 0],
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
