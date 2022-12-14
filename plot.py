import matplotlib.patches as mpatches
from typing import Optional, List
import matplotlib.pyplot as plt
from matplotlib import cm
import pandas as pd
import numpy as np


df = pd.read_feather('plays.feather')


def generic_heat_plot(
        n: np.ndarray,
        white: Optional[str],
        pieces: Optional[List],
):
    """
    Make a generic heat plot of the board.
    :param n: 8x8 array
    :param white: the player
    :param pieces: the pieces
    :return: None
    """

    # Formatting
    width = 0.9
    cmap = cm.get_cmap('viridis')

    # Make figure objects
    figure: plt.Figure = plt.figure(
        dpi=300,
        figsize=(5, 5)
    )
    ax: plt.Axes = figure.add_subplot()

    # Normalize
    nn = n / n.max()

    for i, row in enumerate(nn):
        for j, val in enumerate(row):
            ax.add_patch(mpatches.Rectangle(
                (i - width / 2, j - width / 2),
                width,
                width,
                color=cmap(val)
            ))

    # Generate a label
    player_labels = {
        'True': 'white',
        'False': 'black',
        'None': 'both',
    }
    piece_label = 'all' if pieces is None else ', '.join(pieces)
    f_piece_label = 'all' if pieces is None else ''.join(pieces)
    player = player_labels[str(white)]
    label = f'Player: {player}, Pieces: {piece_label}'
    fname = f'{player}_{f_piece_label}'

    # Add label
    ax.text(
        -0.5,
        8.25,
        label,
        clip_on=False,
    )

    # Add white, black text
    for label, y_pos in zip(['white', 'black'], [-1.25, 7.75]):
        ax.text(
            3,
            y_pos,
            f'{label} side',
            clip_on=False,
        )

    # Format
    ax.set_xlim(-0.5, 7.5)
    ax.set_ylim(-0.5, 7.5)
    ax.set_aspect('equal')
    ax.set_xticks(range(8))
    ax.set_xticklabels(['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h'])
    ax.set_yticks(range(8))
    ax.set_yticklabels(range(1, 9))
    ax.tick_params(axis=u'both', which=u'both', length=0)
    for pos in ['top', 'right', 'bottom', 'left']:
        ax.spines[pos].set_visible(False)

    # Save
    figure.savefig(f'figures/{fname}.png')


def plot_heat(
        white: Optional[bool] = None,
        pieces: Optional[List] = None,
        fast: bool = False,
):

    # Down select
    idf = df.copy(deep=True)

    # Select player and pieces of interest
    if white is not None:
        idf = idf[idf['white'] == white]
    if pieces is not None:
        idf = idf[idf['piece'].isin(pieces)]

    # If fast, truncate
    if fast:
        idf = idf.head(100000)

    # Make a place to store counts
    count = np.zeros((8, 8), dtype=int)
    for i in range(8):
        for j in range(8):
            count[i, j] = sum((idf['posx'] == i) & (idf['posy'] == j))

    # Plot
    generic_heat_plot(
        n=count,
        white=white,
        pieces=pieces,
    )


def make_basic_plots():

    fast = True

    plot_heat(fast=fast, white=None, pieces=None)
    plot_heat(fast=fast, white=True, pieces=None)
    plot_heat(fast=fast, white=False, pieces=None)
    plot_heat(fast=fast, white=True, pieces=['B'])


if __name__ == '__main__':
    # make_basic_plots()
    print(df.dtypes)
