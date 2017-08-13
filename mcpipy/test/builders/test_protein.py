import pandas as pd
from cellcraft.builders.protein import define_items_color_texture_protein, store_location_biological_prot_data


def test_define_items_color_texture_protein():
    dict_chains = {"a": 1, "b": 2}
    d_appearance = define_items_color_texture_protein(dict_chains)
    assert len(d_appearance) == 2
    assert d_appearance[1]['color'] != d_appearance[2]['color']

def test_store_location_biological_prot_data():
    complex_coordinates = pd.Series([0.03, 0.45, 0.23])
    name = '1jsu'
    data_dict = store_location_biological_prot_data(complex_coordinates, name)