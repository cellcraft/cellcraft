from mc import Minecraft
from pymongo import MongoClient


# connect to minecraft
def minecraft_connector():
    mc = Minecraft()
    pos = mc.player.getPos()
    return mc, pos


# create a DB/collection
def mongodb_connector():
    client = MongoClient()
    db = client['try']
    return db




def add_item(pdbin, uniprotid, color, Keggid, GOterms, ECs, gEntrez, gEnsembl, KOPaths, texture):
    client = MongoClient()
    db = client['try']
    collection = db['protein']
    _id = db.collection.insert({
        'pdbin': pdbin,
        'uniprotid': uniprotid,
        'color': color,
        'Keggid': Keggid,
        'GOterms': GOterms,
        'ECs': ECs,
        'gEntrez': gEntrez,
        'gEnsembl': gEnsembl,
        'KOPaths': KOPaths,
        'texture': texture,
        'date': DateTime.UtcNow.AddHours(1)})
    client.close()
    return _id


def add_collection():
    #    db.protein.find_one({'pdbid':pdbin})
    #    client.close()
    client = MongoClient()
    db = client['try']
    collection = db['protein']

    db.protein.insert({'name': 'myoglobin', 'pdb': '1myb'})
    db.collection.insert({
        'pdbin': pdbin,
        'uniprotid': uniprotid,
        'color': color,
        'Keggid': Keggid,
        'GOterms': GOterms,
        'ECs': ECs,
        'gEntrez': gEntrez,
        'gEnsembl': gEnsembl,
        'KOPaths': KOPaths,
        'texture': texture,
        'date': DateTime.UtcNow.AddHours(1)})

    db.protein.find_one({'pdbid': pdbin})

    client.close()
