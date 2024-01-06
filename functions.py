import pandas as pd

df = pd.read_csv("pack_data.csv")


def get_matches(player_name):
    player_info = []
    for _, row in df.iterrows():
        if row["player1"] == player_name:
            player_info.append(
                {
                    "player": player_name,
                    "player_race": row["player1_race"],
                    "opponent": row["player2"],
                    "opponent_race": row["player2_race"],
                    "decision": "win" if row["winner_name"] == player_name else "loss",
                }
            )
        elif row["player2"] == player_name:
            player_info.append(
                {
                    "player": player_name,
                    "player_race": row["player2_race"],
                    "opponent": row["player1"],
                    "opponent_race": row["player1_race"],
                    "decision": "win" if row["winner_name"] == player_name else "loss",
                }
            )
    return player_info


# def winrate(name, race=None):
#    player_subset = df[(df['player1'] == name) | (df['player2'] == name)]
#    win_games = player_subset[player_subset['winner_name'] == name]
#    winrate = len(win_games) / len(player_subset)
#    return "{:.2%}".format(winrate)
#
def winrate(name, race=None):
    player_matches = get_matches(name)
    if race is not None:
        race_letter = race[0].upper()
        race_match = [game for game in player_matches if game["player_race"] == race]
        race_wins = [game for game in race_match if game["decision"] == "win"]
        overall_race_wr = len(race_wins) / len(race_match)
        zerg_wr = winrate_vs_opponent(race_match, "Zerg")
        terran_wr = winrate_vs_opponent(race_match, "Terran")
        protoss_wr = winrate_vs_opponent(race_match, "Protoss")
        print(f"{race_letter}vZ winrate: {zerg_wr:.2%}")
        print(f"{race_letter}vT winrate: {terran_wr:.2%}")
        print(f"{race_letter}vP winrate: {protoss_wr:.2%}")
        print(f"Overall {race} winrate: {overall_race_wr:.2%}")
    else:
        wins = [game for game in player_matches if game["decision"] == "win"]
        winrate = len(wins) / len(player_matches)
        return "Overall winrate is {:.2%}".format(winrate)


def winrate_vs_opponent(race_matches, opponent_race):
    games_vs_opponent = [game for game in race_matches if game["opponent_race"] == opponent_race]
    wins_vs_opponent = [game for game in games_vs_opponent if game["decision"] == "win"]
    return len(wins_vs_opponent) / len(games_vs_opponent)
