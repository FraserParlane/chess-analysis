from datetime import datetime
from typing import Tuple
from tqdm import tqdm
import pandas as pd
import berserk
import json

# Create a lichess session
with open('lichess.token') as t:
    token = t.read()
session = berserk.TokenSession(token)
client = berserk.Client(session)


def get_top_players(n: int = 200):
    """
    Get a list of the top players whose games should be scraped.  The maximum
    number of players in the leaderboard is 200.
    :param n: number of leaders to get
    :return: None
    """

    leaders = client.users.get_leaderboard('classical', count=n)
    with open('leaders.json', 'w') as f:
        json.dump(leaders, f)


def get_top_player_games(n: int = int(1E4)):
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
        while True:
            try:
                games = client.games.export_by_player(
                    username=username,
                    since=date_start,
                    until=date_stop,
                    max=n,
                )
                break

            except:
                print(f'{username} failed.')
                pass

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


def clean_data():
    """
    Clean the game data.
    :return: None
    """

    # Read in the feather file
    df = pd.read_feather('games.feather')

    # Remove duplicates
    df = df.drop_duplicates(subset=['id'])
    print(len(df))

    # Reset index
    df.reset_index(inplace=True)

    # Save
    df.to_feather('games-clean.feather')


def process_data():
    """
    Process the play data
    :return: None
    """

    # Read in the data
    df = pd.read_feather('games-clean.feather')

    # Create a place to store the resulting moves
    rows = []

    # Iter through the rows
    for i, row in tqdm(df.iterrows(), total=len(df)):

        # Skip if no moves played
        if row['moves'] == '':
            continue

        # Process the moves
        moves = row.moves.split(' ')

        # For each move
        for j, move in enumerate(moves):

            # Get special moves
            white = True if j % 2 == 0 else False
            check = True if move.endswith('+') else False
            mate = True if move.endswith('#') else False
            q_castle = True if 'O-O' in move else False
            k_castle = True if 'O-O-O' in move else False
            kill = True if 'x' in move else False
            promote = True if '=Q' in move else False

            # Deal with Castling first
            if q_castle or k_castle:
                castle_base = dict(
                    white=white,
                    kill=False,
                    check=False,
                    mate=False,
                )
                castle_base['posy'] = 0 if white else 7
                if q_castle:
                    r = castle_base | dict(piece='K', posx=6)
                    rows.append(r)
                    r = castle_base | dict(piece='R', posx=5)
                    rows.append(r)
                else:
                    r = castle_base | dict(piece='K', posx=2)
                    rows.append(r)
                    r = castle_base | dict(piece='R', posx=3)
                    rows.append(r)
                continue

            # Get posx, posy
            pos = move_to_pos(
                move=move,
                white=white,
                promote=promote,
                check=check,
                mate=mate,
            )

            # Record position
            posx, posy = pos_to_coord(pos)

            # Get piece
            piece = move_to_piece(move)
            r = dict(
                white=white,
                piece=piece,
                posx=posx,
                posy=posy,
                kill=kill,
                check=check,
                mate=mate,
            )
            rows.append(r)

    # Save
    df = pd.DataFrame(rows)
    df.to_feather('plays.feather')


def add_row(
        df: pd.DataFrame,
        d: dict,
) -> pd.DataFrame:
    """
    Add a dictionary to a dataframe
    :param df:
    :param d:
    :return:
    """

    comb = pd.concat(
        [df,
         pd.DataFrame(
             d,
             index=[0],
         )],
        ignore_index=True,
    )
    return comb


def move_to_piece(
        move: str,
) -> str:
    """
    Extract a piece from a move.
    :param move: move string
    :return: piece
    """
    if move[0] not in ['Q', 'K', 'B', 'N', 'R']:
        return 'P'
    else:
        return move[0]


def move_to_pos(
        move: str,
        promote: bool,
        white: bool,
        check: bool,
        mate: bool,
) -> str:
    """
    extract the position (i.e. 'd2') from a move (i.e. 'Nfd2').
    :param move: move
    :param promote: has a pawn been promoted
    :param white: is white turn
    :param check: Is check
    :param mate: Is mate
    :return: pos
    """

    # If not a castling or
    if '=' in move and (check or mate):
        return move[-5:-3]
    elif '=' in move:
        return move[-4:-2]
    elif check or mate:
        return move[-3:-1]
    else:
        return move[-2:]


def pos_to_coord(
        pos: str,
) -> Tuple[int, int]:
    """
    Convert a string ('a2') into a coordinate [0, 1].
    :param pos: Position.
    :return: List of int.
    """
    coord = (
        ord(pos[0]) - 97,
        int(pos[1]) - 1,
    )
    return coord


if __name__ == '__main__':
    get_top_players()
    get_top_player_games()
    format_games_into_pandas()
    clean_data()
    process_data()
