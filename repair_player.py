#! /usr/bin/python3

"""Compare and repair minecraft playerdata from a Bedrock Dedicated Server leveldb"""

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
parser.add_argument("old_world_path", help="file path to old world db folder")
parser.add_argument("new_world_path", help="file path to new world db folder")
parser.add_argument("number", help="integer found using find_player.py")
args = parser.parse_args()
args.number = int(args.number)

def parse_players(db_path):
    """Returns a list of tuples: (dbkey, binaryblob, parseddata)"""
    db = ldb.open(db_path)
    players = get_players(db)
    ldb.close(db)
    parsed_players = []
    for key, playerdata in players.items():
        player = nbt.decode(nbt.DataReader(playerdata))
        if not isinstance(player, nbt.TAG_Compound):
            raise Exception(f"Can't understand player of type {type(player)}")
        player_dict = {tag.name: tag.payload for tag in player.payload}
        parsed_players.append((key, playerdata, player_dict))
    return parsed_players

old_players = parse_players(args.old_world_path)
new_players = parse_players(args.new_world_path)

def print_players():
    def print_player(player):
        print(
            "\n".join([f'{k}: {v}' for k, v in player.items()])
        )
    print_player(old_players[args.number][2])
    print_player(new_players[args.number][2])

def inject_old_into_new():
    db = ldb.open(args.new_world_path)
    # insert old player's binary blob into new player's db key
    ldb.put(db, new_players[args.number][0], old_players[args.number][1])
    ldb.close(db)
    
print_players()
print("You must uncomment a line in the Python script to actually do work")

# Uncomment the line below
#inject_old_into_new()
