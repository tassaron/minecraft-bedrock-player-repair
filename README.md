# Bedrock Player Repair Script

Take player data from one Bedrock Dedicated Server database and inject it into another database. This could allow you to repair a corrupted player in your Minecraft world without rolling back the entire world.

Thanks to cjwatson for [this script](https://github.com/cjwatson/minecraft-convert-local-player), which I used as a reference when creating this one.

## Instructions
1. [Install these bindings for Bedrock's leveldb format.](https://github.com/BluCodeGH/bedrock) (I recommend using a virtual env. You might have to compile stuff.)
1. Shut down the server and obtain a copy of your Minecraft world. You need the `db` folder
1. Run `find_player.py path/to/your/db` and try to figure out which player is the one you want to repair. Compare inventories or ender chests or something identifiable (sadly there are no usernames)
1. Remember the index of the player you want. So the first player is 0, second is 1, etc.
1. Run `repair_player.py path/to/old/db path/to/new/db INDEX`. The old db is one where your player wasn't corrupt, and INDEX is the index of your player as returned by `find_player.py`
1. Compare the two players printed by this script. The first player printed will REPLACE the second player printed.
1. If you're totally sure, uncomment the final line in `repair_player.py`

## Backstory
Once upon a time, I fell from a high place and died in the game of Minecraft. A totem of undying saved me, but a few seconds later my screen went grey. All I could see was the HUD and a general skybox/darkness colour. Soon after, my game crashed. I thought it could be because I was using the unofficial launcher for Linux, so I tried logging in from other devices. Everything crashed shortly after logging into the world. I tried teleporting my player using the server console; the player's position changed and it was clear that they did exist in the world. But still the game would crash if I actually tried to play.

Eventually I came to the conclusion that my only option was to write this Python script. To my surprise, it actually worked! My Ender Chest is saved thanks to Python :)

Later I found [this bug report](https://github.com/ChristopherHX/mcpelauncher-manifest/issues/278) on the launcher I was using, which seems to describe what happened. The player entity's rotation value becomes `NaN` and allegedly can be fixed by switching to third person. I haven't confirmed this yet.
