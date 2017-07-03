
from cellcraft.config import PATH_TEST_CACHE
from cellcraft.builders.cache import get_complex, CellcraftGridStore
import logging

def test_get_complex():
    mode = "pdb"
    name_1 = "3RGK"
    name_2 = "1ejg"
    blocksize = 1
    threshold = 2
    usecache = True
    cgs = CellcraftGridStore(PATH_TEST_CACHE)
    check1 = cgs.check_if_in_cache(mode=mode, name=name_1, blocksize=blocksize, threshold=threshold)
    assert check1, f'{name_1} should be found in cache.'
    check2 = cgs.check_if_in_cache(mode=mode, name=name_2, blocksize=blocksize, threshold=threshold)
    assert not check2, f'{name_2} should not be found in cache.'

    # bio_complex = get_complex(mode, name_1, blocksize, threshold, usecache, PATH_TEST_CACHE)  
    # import ipdb; ipdb.set_trace()
    # assert bio_complex.name == "3RGK"
    logging.info('Passed test_get_complex.')

test_get_complex()