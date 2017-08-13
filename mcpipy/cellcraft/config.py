import os
import json
import logging


# cellcraft node
CELLCRAFT_NODE_URL="http://192.168.178.29:4534"


# path to cache where pickle files will be stored
PATH_RESOURCES='cellcraft/resources'
PATH_CACHE='cellcraft/resources/cache/'
PATH_TEST_CACHE='test/fixtures/cache/'

# path to fixtures
PATH_TO_FIXTURES="test/fixtures"

# path to cellpack structures after processing them
PATH_CELLPACK = 'cellcraft/resources/cellpack/'

# cellpack parameters
envelop_id = 22

# database name to store biological information and coordinates of structures
DB='cellcraft'
TEST_DB='test'

# fix maximum amount of structures saved on cache
MAXIMUM_NUM_STRUCTURES_CACHE = 8

# load block appear appearance json
def load_block_appearance():
    with open(os.path.join(PATH_RESOURCES, "block_appearance.json")) as appearance_json:
        block_appearance = json.load(appearance_json)
    return block_appearance


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
