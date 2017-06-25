from mcpipy.mcpi.minecraft import Minecraft

# connect to minecraft server
def minecraft_connector():
    mc = Minecraft()
    pos = mc.player.getPos()
    return mc, pos