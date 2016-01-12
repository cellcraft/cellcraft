import re, sys, os
from pymongo import MongoClient

# create a DB/collection

def connect_to_db():
    client = MongoClient()
    db = client['try']
    return db

# insert element into DB

# find element in DB

# print from DB

def add_item(pdbin,uniprotid,color,Keggid,GOterms,ECs,gEntrez,gEnsembl,KOPaths,texture):
    client = MongoClient()
    db = client['try']
    collection = db['protein']
    _id = db.collection.insert({
            'pdbin':pdbin,
            'uniprotid':uniprotid,
            'color':color,
            'Keggid':Keggid,
            'GOterms':GOterms,
            'ECs':ECs,
            'gEntrez':gEntrez,
            'gEnsembl':gEnsembl,
            'KOPaths':KOPaths,
            'texture':texture,
            'date':DateTime.UtcNow.AddHours(1)})
    client.close()
    return _id

def add_collection():




#    db.protein.find_one({'pdbid':pdbin})
#    client.close()
client = MongoClient()
db = client['try']
collection = db['protein']

db.protein.insert({'name':'myoglobin','pdb':'1myb'})
db.collection.insert({
        'pdbin':pdbin,
        'uniprotid':uniprotid,
        'color':color,
        'Keggid':Keggid,
        'GOterms':GOterms,
        'ECs':ECs,
        'gEntrez':gEntrez,
        'gEnsembl':gEnsembl,
        'KOPaths':KOPaths,
        'texture':texture,
        'date':DateTime.UtcNow.AddHours(1)})

db.protein.find_one({'pdbid':pdbin})

client.close()
