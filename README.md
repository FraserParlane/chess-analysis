# Chess moves—a statistical analysis

Which are the most frequently used tiles on a chess board? Which tile is black most likely to move a pawn onto? What tile are both players most likely to lose a piece on? This repo provides an analysis of >1 million chess moves to answer these quetions and more.

<img src="figures/both_all.png" style="padding-left: 20%; padding-right: 20%;">

# Data source

[Lichess](https://lichess.org/) is a free and open-source chess server with an [API](https://lichess.org/api) that provides access to all games played on the site. I used the [Berserk](https://pypi.org/project/berserk-downstream/) Python wrapper to download the top **X** games from the top **Y** players on Lichess, resulting in **Z** total chess moves.

# To use
1. Create a Lichess account and [create a token](https://lichess.org/account/oauth/token). Save this token as `lichess.token` within the repository.
2. `process.py` fetches and cleans the data from Lichess. Modify the number of top players to 