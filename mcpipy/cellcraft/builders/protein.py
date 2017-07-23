import logging
import numpy as np
from biopandas.pdb import PandasPdb
from cellcraft.builders.grid import create_bins_from_coordinates
from cellcraft.connectors.db_connectors import uniprot_id_call, extract_biological_info_from_uniprot, store_on_node
from cellcraft.config import load_block_appearance


def get_pdb_complex(name, theta, blocksize, threshold):
    coor_df, chain_block = get_pdb_from_source(name)
    bin_count_df = create_bins_from_coordinates(
        coor_df, theta, blocksize, threshold, id_column='chain_id')
    return bin_count_df, chain_block


def get_pdb_from_source(name):
    protein_pdb = PandasPdb().fetch_pdb(name)
    prot_df = protein_pdb.df['ATOM'].ix[:, ['chain_id', 'x_coord', 'y_coord', 'z_coord']]
    prot_df['chain_id'], dict_chains = string_to_int(prot_df['chain_id'])
    chain_block = define_items_color_texture_protein(dict_chains)
    return prot_df, chain_block


def string_to_int(list_str):
    d = {s: i for i, s in enumerate(list_str.unique())}
    list_chains_int = list_str.map(d)
    return list_chains_int, d


def define_items_color_texture_protein(dict_chains):
    block_appearance = load_block_appearance()
    np.random.shuffle(block_appearance["light_color_names"])
    np.random.shuffle(block_appearance["dark_color_names"])
    d_appearance = {}
    odd = 0
    even = 0
    for i, chain in enumerate(dict_chains.values()):
        if i % 2 == 0:
            color = block_appearance["light_color_names"][even]
            if even == len(block_appearance["light_color_names"]) - 1:
                even = 0
            else:
                even += 1
        else:
            color = block_appearance["dark_color_names"][odd]
            if odd == len(block_appearance["dark_color_names"]) - 1:
                odd = 0
            else:
                odd += 1
        d_appearance[chain] = {
            'texture': block_appearance["textures"]["wool"],
            'color': block_appearance["colors"][color]["id"]
        }
    return d_appearance


def store_location_biological_prot_data(complex_coordinates, name):
    uniprot_id = uniprot_id_call(name)
    bio_uniprot_data = extract_biological_info_from_uniprot(uniprot_id)

    logging.info("Requested data for coordinates {}: {}".format(complex_coordinates, bio_uniprot_data))
    data_dict = {
        "location": complex_coordinates.tolist(),
        "pdb_id": name,
        "uniprot_id": uniprot_id,
        "organism": bio_uniprot_data["organism"],
        "genes_ensembl": bio_uniprot_data["ensembl"],
        "genes_entrez": bio_uniprot_data["gene_id"],
        "pfam_id": bio_uniprot_data["pfam"],
        "go_terms": bio_uniprot_data["go"],
        "kegg_ids": bio_uniprot_data["kegg"],
        "ko_ids": bio_uniprot_data["ko"]
    }
    store_on_node(data_dict)
    return data_dict