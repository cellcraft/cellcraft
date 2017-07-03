import json
import os
import re
import xmltodict
import pandas as pd
from collections import defaultdict
from pymongo import MongoClient
from cellcraft.config import DB, PATH_TO_FIXTURES
from cellcraft.connectors.db_connectors import insert_to_mongo, protein_data_bank_connector, kegg_connector, \
    uniprot_connector, uniprot_id_call


def test_insert_to_mongo():
    client = MongoClient(host=['localhost:27017'], document_class=dict, tz_aware=True, connect=True)
    db = "test"
    database = client[db]
    database.items.delete_many({})
    cursor = database.items.find()
    items = [element for element in cursor]
    assert len(items) == 0

    with open(os.path.join(PATH_TO_FIXTURES, "item_info.json")) as item_json:
        item_info_json = json.load(item_json)
    insert_to_mongo(item_info_json, "test")

    cursor = database.items.find()
    items = [element for element in cursor]
    assert len(items) > 0


def test_kegg_connector():
    kegg_id = "mmu:18747"
    result = kegg_connector(kegg_id)
    str_result = result.read().decode('utf8').replace("'", '"')
    organism = [" ".join(x.split(" ")[4:]) for x in str_result.split("\n") if len(re.findall("^ORGANISM", x)) > 0]
    uniprot_rows = [x.split(";") for x in str_result.split("\n") if len(re.findall("^DR", x)) > 0]
    uniprot_df = pd.DataFrame(uniprot_rows, columns=['id_name', 'id1', 'id2', 'id3', 'id4'])
    uniprot_df['id_name'] = [x[0].split("  ")[1] for x in uniprot_rows]
    assert len(str_result) > 0
    assert result.status == 200


def test_uniprot_connector():
    # TODO mock connection
    uniprot_id = "P05132"
    uniprot_df = uniprot_connector(uniprot_id)
    assert len(uniprot_df) > 0


def test_uniprot_id_call():
    # TODO mock connection
    pdb_id = "5JR7"
    result = uniprot_id_call(pdb_id)
    assert len(result) > 0
    assert result.status == 200
