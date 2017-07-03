from pymongo import MongoClient
import os
import urllib
import ssl


# create a DB/collection
class MongoDB():
    def __init__(self, host=['localhost:27017']):
        self.host = host

    def add_item(self, data):
        client = MongoClient(host=self.host)
        db = client['item']
        _id = db.item.insert(data)
        client.close()
        return _id

    def get_item(self, item_id):
        client = MongoClient(host=self.host)
        db = client['item']
        item = db.protein.find_one({'item_id': item_id})
        client.close()
        return item


def insert_structure_into_mongodb():
    mdb = MongoDB()


# def open_filestream(filename):
#     with open(filename, 'r') as fn:
#         return fn


def save_file(obj, filename):
    with open(filename, 'w') as fn:
        fn.write(obj)


class PDBStore():
    def __init__(self, pdb_store='cellcraft/pdb/'):
        self.pdb_store = pdb_store

    def get_pdb(self, pdb_id):
        pdb_id = pdb_id.lower()
        local_pdb = os.path.join(self.pdb_store, pdb_id + '.pdb')
        if not os.path.isfile(local_pdb):
            pdb_s = protein_data_bank_connector(pdb_id, local_pdb)
            save_file(pdb_s, local_pdb)
        return local_pdb

    def get_path(self, pdb_id, version):
        return os.path.join(self.pdb_store, '{}_{}.pdb'.format(pdb_id, version))


def protein_data_bank_connector(pdb_id, path):
    context = ssl._create_unverified_context()
    link = 'https://www.rcsb.org/pdb/files/' + pdb_id + '.pdb'
    return urllib.request.urlopen(link, context=context).read().decode('utf-8')


def kegg_connector(kegg_id):
    link = 'http://rest.kegg.jp/get/' + kegg_id
    return urllib.request.urlopen(link)


def uniprot_connector(pdb_id):
    link = 'http://www.rcsb.org/pdb/rest/das/pdb_uniprot_mapping/alignment?query=' + pdb_id
    return urllib.request.urlopen(link)

