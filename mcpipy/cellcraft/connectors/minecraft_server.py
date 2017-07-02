from mcpi.minecraft import Minecraft


def minecraft_connector():
    """
    Connect to minecraft server.
    :return: Minecraft instance and the coordinates of the player
    """
    mc = Minecraft()
    pos = mc.player.getPos()
    return mc, pos
