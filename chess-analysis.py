import berserk
import json

# Create a lichess session
with open('lichess.token') as f:
    token = f.read()
session = berserk.TokenSession(token)
client = berserk.Client(session)


def get_top_players(n: int = 10):
    """
    Get a list of the top players whose games should be scraped.
    :param n: number of leaders to get
    :return: None
    """

    leaders = client.users.get_leaderboard('classical', count=10)
    with open('leaders.json', 'w') as f:
        json.dump(leaders, f)


if __name__ == '__main__':
    get_top_players()
