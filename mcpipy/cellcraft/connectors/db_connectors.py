import logging
import urllib
import json
import requests
import re
import itertools
import xmltodict
import pandas as pd
from pymongo import MongoClient
from cellcraft.config import CELLCRAFT_NODE_URL


def get_item(_id):
    url = urllib.parse.urljoin(CELLCRAFT_NODE_URL, f'items/{_id}')
    response = requests.get(url)
    response_data = response.json()['data']
    return response_data


def get_items(**params):
    url = urllib.parse.urljoin(CELLCRAFT_NODE_URL, 'items')
    response = requests.get(url, params=params)
    response_data = response.json()['data']
    return response_data


def store_on_node(data_dict):
    url = urllib.parse.urljoin(CELLCRAFT_NODE_URL, 'items')
    response = requests.post(url, json={'data': data_dict})
    item_id = response.json()['data']['item_id']
    logging.info("Stored item with id {}.".format(item_id))
    return item_id


def insert_to_mongo(item_info_json, database):
    """

    :param item_info_json:
    :param database:
    :return:
    """
    try:
        client = MongoClient(host=['localhost:27017'], document_class=dict, tz_aware=True, connect=True)
        database = client[database]
        result = database.items.insert_one(item_info_json)
        logging.info("Inserted into database element {}.".format(result.inserted_id))
        client.close()

    except Exception as exp:
        logging.exception("Could not connect to the MongoDB and insert item.")


def protein_data_bank_connector(pdb_id):
    url = "http://www.rcsb.org/pdb/files/{}.pdb".format(pdb_id)
    result = urllib.request.urlopen(url)

    if result.getcode() != 200:
        raise ValueError("Can not connect with the Protein Data Bank")

    return result


def extract_uniprot_id_from_call(text):
    d = xmltodict.parse(text)
    d = json.dumps(d)
    d = json.loads(d)

    uniprot_id = d['dasalignment']['alignment'][1]['alignObject'][1]['@dbAccessionId']
    return uniprot_id


def uniprot_connector(uniprot_id):
    url = "http://www.uniprot.org/uniprot/{}.txt".format(uniprot_id)
    result = urllib.request.urlopen(url)

    if result.getcode() != 200:
        raise ValueError("Can not connect to UniProt")

    text = result.read().decode('utf8').replace("'", '"')
    return text


def extract_biological_info_from_uniprot(text):
    try:
        bio_uniprot = {}
        organism = [" ".join(x.split(" ")[3:]) for x in text.split("\n") if len(re.findall("^OS", x)) > 0][0]
        logging.info("Organism extracted from Uniprot.")
    except Exception as exp:
        logging.info("Could not find organism name in Uniprot.")
        organism = ''
    bio_uniprot["organism"] = organism

    uniprot_rows = [x.split(";") for x in text.split("\n") if len(re.findall("^DR", x)) > 0]
    uniprot_df = pd.DataFrame(uniprot_rows, columns=['id_name', 'id1', 'id2', 'id3', 'id4'])
    uniprot_df['id_name'] = [x[0].split("  ")[1] for x in uniprot_rows]

    try:
        ensembl_df = uniprot_df[uniprot_df['id_name'] == ' Ensembl']
        ensembl = extract_ids_from_dataframe_row_tolist(ensembl_df)
        logging.info("ENSMBL gene IDs extracted from Uniprot.")
    except Exception as exp:
        logging.info("Could not find ENSEMBL IDs in Uniprot.")
        ensembl = []
    bio_uniprot["ensembl"] = ensembl

    try:
        GeneID_df = uniprot_df[uniprot_df['id_name'] == ' GeneID']
        gene_id = extract_ids_from_dataframe_row_tolist(GeneID_df)
        logging.info("ENSMBL gene IDs extracted from Uniprot.")
    except Exception as exp:
        logging.info("Could not find Gene IDs in Uniprot.")
        gene_id = []
    bio_uniprot["gene_id"] = gene_id

    try:
        Pfam_df = uniprot_df[uniprot_df['id_name'] == ' Pfam']
        pfam_id = extract_ids_from_dataframe_first_column(Pfam_df)
        logging.info("Pfam IDs extracted from Uniprot.")
    except Exception as exp:
        logging.info("Could not find Pfam IDs in Uniprot.")
        pfam_id = []
    bio_uniprot["pfam"] = pfam_id

    try:
        go_df = uniprot_df[uniprot_df['id_name'] == ' GO']
        go_id = extract_ids_from_dataframe_first_column(go_df)
        logging.info("GO Terms extracted from Uniprot.")
    except Exception as exp:
        logging.info("Could not find GO Terms in Uniprot.")
        go_id = []
    bio_uniprot["go"] = go_id

    try:
        kegg_df = uniprot_df[uniprot_df['id_name'] == ' KEGG']
        kegg_id = extract_ids_from_dataframe_row_tolist(kegg_df)
        logging.info("KEGG IDs extracted from Uniprot.")
    except Exception as exp:
        logging.info("Could not find KEGG IDs in Uniprot.")
        kegg_id = []
    bio_uniprot["kegg"] = kegg_id

    try:
        ko_df = uniprot_df[uniprot_df['id_name'] == ' KO']
        ko_id = extract_ids_from_dataframe_row_tolist(ko_df)
        logging.info("KO IDs extracted from Uniprot.")
    except Exception as exp:
        logging.info("Could not find KO IDs in Uniprot.")
        ko_id = []
    bio_uniprot["ko"] = ko_id

    return bio_uniprot


def extract_ids_from_dataframe_row_tolist(df):
    list_ids = []
    for row in df.iterrows():
        ids = [row[1][x].split(" ")[1].split(".")[0].split("-")[0] for x in range(1, len(row[1])) if
               row[1][x] is not None]
        ids = [x for x in ids if x != '']
        list_ids.append(ids)
    list_ids = list(itertools.chain.from_iterable(list_ids))
    return list_ids

def extract_ids_from_dataframe_first_column(df):
    list_ids = []
    for row in df.iterrows():
        ids = [row[1][x].split(" ")[1].split(".")[0].split("-")[0] for x in range(1, len(row[1])) if
               row[1][x] is not None]
        ids = [x for x in ids if x != ''][0]
        list_ids.append(ids)
    return list_ids


def uniprot_id_call(pdb_id):
    url = "http://www.rcsb.org/pdb/rest/das/pdb_uniprot_mapping/alignment?query={}".format(pdb_id)
    result = urllib.request.urlopen(url)

    if result.getcode() != 200:
        raise ValueError("Can not connect to Uniprot")

    text = result.read().decode('utf8').replace("'", '"')
    return text


def kegg_connector(kegg_id):
    url = "http://rest.kegg.jp/get/{}".format(kegg_id)
    result = urllib.request.urlopen(url)

    if result.getcode() != 200:
        raise ValueError("Can not connect to KEGG database")

    text = result.read().decode('utf8').replace("'", '"')
    return text
