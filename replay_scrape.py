import datetime
import pathlib
import sc2reader.resources
import re

import pandas as pd

replays = pathlib.Path("/home/jordan/Documents/git/rts_project/Replays").glob("*.*")

files = [str(f) for f in replays if f.is_file()]

pack_info = {
    "player1": [],
    "player1_race": [],
    "player2": [],
    "player2_race": [],
    "winner": [],
    "map": [],
    "game_type": [],
    "ladder": [],
    "file": [],
    "game_version": [],
    "region": [],
    "game_length": [],
}


for f in files:
    replay = sc2reader.load_replay(f, load_level=2)
    if (
        (replay.game_type == "1v1")
        & ("Player 2" in str(replay.players))
        & ("A.I" not in str(replay.players))
    ):
        pack_info["player1"].append(re.sub(r"[\[\]\(\),]", "", str(replay.players).split()[3]))
        pack_info["player1_race"].append(re.sub(r"[\[\]\(\),]", "", str(replay.players).split()[4]))
        pack_info["player2"].append(re.sub(r"[\[\]\(\),]", "", str(replay.players).split()[8]))
        pack_info["player2_race"].append(re.sub(r"[\[\]\(\),]", "", str(replay.players).split()[9]))
        pack_info["winner"].append(str(replay.winner))
        pack_info["map"].append(str(replay.map_name))
        pack_info["game_type"].append(str(replay.game_type))
        pack_info["ladder"].append(str(replay.is_ladder))
        pack_info["game_version"].append(str(replay.base_build))
        pack_info["region"].append(str(replay.region))
        pack_info["game_length"].append(str(datetime.timedelta(seconds=replay.game_length.seconds)))
        pack_info["file"].append(f.split("/")[-1])

replay_dataframe = pd.DataFrame.from_dict(pack_info)

replay_dataframe['winner_race'] = replay_dataframe['winner'].apply(lambda x: 'None' if x == 'none' else str(x).split()[6].strip('()')) 

replay_dataframe.to_csv("pack_data.csv", index=None)
