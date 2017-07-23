import json
import os
from pymongo import MongoClient
from cellcraft.config import DB, PATH_TO_FIXTURES
from cellcraft.connectors.db_connectors import insert_to_mongo, uniprot_connector, uniprot_id_call, \
    extract_uniprot_id_from_call, extract_biological_info_from_uniprot, store_on_node


def test_sent_to_api():
    with open(os.path.join(PATH_TO_FIXTURES, "item_info.json")) as item_json:
        item_info_json = json.load(item_json)
    store_on_node(item_info_json)
    


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


def test_uniprot_id_call():
    with open(os.path.join(PATH_TO_FIXTURES, "uniprot_id_call_response.txt"), "r") as text:
        uniprot_id = extract_uniprot_id_from_call(text.read())

    assert uniprot_id == 'P00514'


def test_uniprot_connector():
    with open(os.path.join(PATH_TO_FIXTURES, "uniprot_response.txt"), "r") as text:
        bio_uniprot = extract_biological_info_from_uniprot(text.read())

    assert bio_uniprot['pfam'][0] == 'PF00069'
    assert len(bio_uniprot) == 7
