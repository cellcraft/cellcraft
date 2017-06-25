from mcpipy.mcpi.vpython_minecraft import Minecraft
from unittest.mock import Mock, patch
import json

def test_minecraft_connector():
    # with patch('mcpipy.mcpi.vpython_minecraft.Minecraft') as ws_return_mock, \
    #        open(PATH_FIXTURES + 'response_gmaps_reverse_geocode.json', 'r') as mock_file:
    #    minecraft_server_mock = Mock()
    #    minecraft_server_mock.reverse_geocode.return_value = json.load(mock_file)
    #    ws_return_mock.return_value = minecraft_server_mock

    mc = Minecraft()