import re, sys, os
from pymongo import MongoClient

# create a DB/collection

# insert element into DB

# find element in DB

# print from DB

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

