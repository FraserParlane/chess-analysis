from datetime import datetime

import pandas as pd
from tqdm import tqdm
import berserk
import json

# Create a lichess session
with open('lichess.token') as t:
    token = t.read()
session = berserk.TokenSession(token)
client = berserk.Client(session)


def get_top_players(n: int = 10):
    """
    Get a list of the top players whose games should be scraped.
    :param n: number of leaders to get
    :return: None
    """

    leaders = client.users.get_leaderboard('classical', count=n)
    with open('leaders.json', 'w') as f:
        json.dump(leaders, f)


def get_top_player_games(n: int = 10):
    """
    Get the games of the top players.
    :param n: The max number of games for each player.
    :return: None
    """

    # Read in the leaders, get usernames
    with open('leaders.json', 'r') as f:
        leaders = json.load(f)
    usernames = [l['username'] for l in leaders]

    # Define time range for game scraping
    date_start = berserk.utils.to_millis(datetime(1900, 12, 8))
    date_stop = berserk.utils.to_millis(datetime(2050, 12, 9))

    # Create an empty file
    fname = 'games.json'
    with open(fname, 'w') as f:
        f.write('[]')

    # Loop through the players
    for username in tqdm(usernames):

        # Get games
        games = client.games.export_by_player(
            username,
            since=date_start,
            until=date_stop,
            max=n,
        )
        games = list(games)

        # Store
        with open(fname, 'r') as f:
            previous = json.load(f)
        store = previous + games
        with open(fname, 'w') as f:
            f.write(json.dumps(store, default=str))


def format_games_into_pandas():
    """
    Format the games into a pandas dataframe
    :return: None
    """

    # Read in raw data
    df = pd.read_json('games.json')

    # Save
    df.to_feather('games.feather')


if __name__ == '__main__':
    get_top_players()
    get_top_player_games()
    format_games_into_pandas()
