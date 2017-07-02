from mcpi.vpython_minecraft import Minecraft
from cellcraft.connectors.db_connectors import MongoDB
import urllib



def test_connect_Minecraft():
    mnc = Minecraft()
    assert mnc


def test_connect_MongoDB():
    connect = MongoDB()



def protein_data_bank_connector(pdb_id):
    url = 'http://www.rcsb.org/pdb/files/' + pdb_id + '.pdb'
    return urllib.request.urlopen(url)


def kegg_connector(kegg_id):
    url = 'http://rest.kegg.jp/get/' + kegg_id
    return urllib.request.urlopen(url)


def uniprot_connector(pdb_id):
    link = 'http://www.rcsb.org/pdb/rest/das/pdb_uniprot_mapping/alignment?query=' + pdb_id
    return urllib.request.urlopen(link)