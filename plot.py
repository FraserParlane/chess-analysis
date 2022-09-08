from typing import Optional, List
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import pandas as pd
import numpy as np


df = pd.read_feather('plays.feather')


def generic_heat_plot(
        n: np.ndarray,
):
    """
    Make a generic heat plot of the board.
    :param n: 8x8 array
    :return: None
    """

    # Make figure objects
    figure: plt.Figure = plt.figure()
    ax: plt.Axes = figure.add_subplot()




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
        print('fast!')
        idf = idf.head(100000)

    # Make a place to store counts
    count = np.zeros((8, 8), dtype=int)
    for i in range(8):
        for j in range(8):
            count[i, j] = sum((idf['posx'] == i) & (idf['posy'] == j))

    # Plot
    generic_heat_plot(
        n=count,
    )


if __name__ == '__main__':
    plot_heat(
        fast=True,
        white=True,
        pieces=['P']
    )


