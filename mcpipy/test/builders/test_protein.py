from cellcraft.builders.protein import define_items_color_texture_protein, get_pdb_complex


def test_define_items_color_texture_protein():
    dict_chains = {"a": 1, "b": 2}
    d_appearance = define_items_color_texture_protein(dict_chains)
    assert len(d_appearance) == 2
    assert d_appearance[1]['color'] != d_appearance[2]['color']


def test_get_pdb_complex():
    name= "1exr"
    theta = 2
    blocksize = 4
    threshold = 5
    pdb_file = get_pdb_complex(name, theta, blocksize, threshold)
