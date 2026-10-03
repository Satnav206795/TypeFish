from  core.api import chesscom as cc
from core.gameReviewer import review as rv

player = cc.ChessComPlayer("PLAYER","My Game Reviewer in Testing. Email me if needed: (EMAIL)")


data = player.get_games_in_month(player.get_all_months_played()[-1])

print(data[-1]["pgn"])

analisyed = rv.analyiseGame(data[-1]["pgn"],16,10)

print(analisyed)