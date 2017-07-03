import os
from collections import defaultdict
import logging

############# TODO
### generate an algorithm that predicts color and texture of blocks taking into account a) biological features (GOterms) b) n_chains c) type of complex (prot complex, membrane, dna...)
### it should be a method in ProteinComplex(), Membrane() and Dna() instead of particular of each item (Protein(),Lipid()...)



# Setup for correct assignment of colors to example proteins

# colors EC id:color id
col = {'1': 6, '2': 1, '3': 9, '4': 2, '5': 5, '6': 4, '0': 7}

# testure path name:texture id
text = defaultdict(list)
names = ['Metabolism', 'Genetic Information Processing', 'Human Diseases', 'Drug Development',
         'Environmental Information Processing', 'Cellular Processes', 'Organismal Systems']

# texture 95 crystal, 159 full, 35 wool
textures = ['159', '35', '35', '35', '95', '95', '95']
for t, n in zip(textures, names):
    text[t].append(n)

# path to cache where pickle files will be stored
PATH_CACHE='cellcraft/cache/'
PATH_TEST_CACHE='test/fixtures/cache/'

# database name to store biological information and coordinates of structures
DB='cellcraft'
TEST_DB='test'


# path to fixtures
PATH_TO_FIXTURES="test/fixtures"

current_env = os.environ.get('app_env')
root_logger = logging.getLogger()

current_env = 'test'

if current_env == 'cellcraft':
    DB_HOST = '127.0.0.1'
    DB_PORT = 27017
    root_logger.setLevel(logging.INFO)


elif current_env == 'test':
    DB_HOST = '127.0.0.1'
    DB_PORT = 27017
    root_logger.setLevel(logging.DEBUG)

else:
    logging.warning('Please configure a environment using now default dev environment for config')
    root_logger.setLevel(logging.DEBUG)
