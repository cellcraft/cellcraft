import logging
import urllib
from pymongo import MongoClient
from cellcraft.config import DB, DB_HOST, DB_PORT


def insert_to_mongo(item_info_json, database=DB):
    """

    :param item_info_json:
    :param database:
    :return:
    """
    try:
        client = MongoClient()
        database = client[database]
        result = database.restaurants.insert_one(item_info_json)
        logging.info("Inserted into database element {}.".format(result.id))
        client.close()

    except Exception as exp:
        logging.exception("Could not connect to the MongoDB and insert item.")


def protein_data_bank_connector(pdb_id):
    url = "http://www.rcsb.org/pdb/files/{pdb_id}.pdb".format(pdb_id)
    result = urllib.request.urlopen(url)

    if result.getcode() != 200:
        raise ValueError("Can not connect with the Protein Data Bank")

    return result


def kegg_connector(kegg_id):
    url = "http://rest.kegg.jp/get/{kegg_id}".format(kegg_id)
    result = urllib.request.urlopen(url)

    if result.getcode() != 200:
        raise ValueError("Can not connect with the Protein Data Bank")

    return result


def uniprot_connector(pdb_id):
    url = "http://www.rcsb.org/pdb/rest/das/pdb_uniprot_mapping/alignment?query={pdb_id}".format(pdb_id)
    result = urllib.request.urlopen(url)

    if result.getcode() != 200:
        raise ValueError("Can not connect with the Protein Data Bank")

    return result
