#! /usr/bin/python3

"""Print player data from a Minecraft Bedrock Dedicated Server leveldb"""

import argparse

from bedrock import (
    leveldb as ldb,
    nbt,
)


def get_players(db):
    return {
        key: value
        for key, value in ldb.iterate(db)
        if key.startswith(b"player_server_")
    }


parser = argparse.ArgumentParser(
    description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter
)
parser.add_argument("world_path", help="file path to world db folder")
args = parser.parse_args()

db = ldb.open(args.world_path)
players = get_players(db)
ldb.close(db)

parsed_players = []
for playerdata in players.values():
    player = nbt.decode(nbt.DataReader(playerdata))
    if not isinstance(player, nbt.TAG_Compound):
        raise Exception(f"Invalid player type {type(player)}")
    player_dict = {tag.name: tag.payload for tag in player.payload}
    parsed_players.append(player_dict)

print(
    "\n\n================\n\n".join([
            "\n".join([f'{k}: {v}' for k, v in player.items()])
            for player in parsed_players
            ])
)
