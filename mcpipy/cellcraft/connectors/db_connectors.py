import logging
import urllib
import json
import re
import xmltodict
import pandas as pd
from pymongo import MongoClient
from cellcraft.config import DB, DB_HOST, DB_PORT


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


def uniprot_id_call(pdb_id):
    url = "http://www.rcsb.org/pdb/rest/das/pdb_uniprot_mapping/alignment?query={}".format(pdb_id)
    result = urllib.request.urlopen(url)

    if result.getcode() != 200:
        raise ValueError("Can not connect with the Protein Data Bank")

    str_result = result.read().decode('utf8').replace("'", '"')
    dict_result = xmltodict.parse(str_result)
    dict_result = json.dumps(dict_result)
    dict_result = json.loads(dict_result)
    uniprot_id = dict_result['dasalignment']['alignment'][1]['alignObject'][1]['@dbAccessionId']

    return uniprot_id


def uniprot_connector(uniprot_id):
    url = "http://www.uniprot.org/uniprot/{}.txt".format(uniprot_id)
    result = urllib.request.urlopen(url)

    if result.getcode() != 200:
        raise ValueError("Can not connect with the Protein Data Bank")

    str_result = result.read().decode('utf8').replace("'", '"')
    uniprot_rows = [x.split(";") for x in str_result.split("\n") if len(re.findall("^DR", x)) > 0]
    uniprot_df = pd.DataFrame(uniprot_rows, columns=['id_name', 'id1', 'id2', 'id3', 'id4'])
    uniprot_df['id_name'] = [x[0].split("  ")[1] for x in uniprot_rows]

    return uniprot_df


def kegg_connector(kegg_id):
    url = "http://rest.kegg.jp/get/{}".format(kegg_id)
    result = urllib.request.urlopen(url)

    if result.getcode() != 200:
        raise ValueError("Can not connect with the Protein Data Bank")

    return result