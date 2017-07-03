from mcpi.minecraft import Minecraft
from mcpi.block import Block


def minecraft_connector():
    """
    Connect to minecraft server.
    :return: Minecraft instance and the coordinates of the player
    """
    mc = Minecraft()
    pos = mc.player.getPos()
    return mc, pos


def add_numpy_array_to_minecraft(minecraft_conn, start_coordinates, bio_complex):
    """
    """
    bin_count_df, item_info = bio_complex

    for idx, row in bin_count_df.iterrows():
        coord = row[['x_coord', 'y_coord', 'z_coord']] + start_coordinates
        info = item_info[row['id']]
        texture = int(info['texture'])
        color = int(info['color'])
        minecraft_conn.setBlock(coord.tolist(), Block(texture, color))
