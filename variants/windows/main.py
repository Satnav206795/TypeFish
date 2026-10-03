from core.api import chesscom as cc
from core.gameReviewer import review as rv
from core.api import api as api

player = cc.ChessComPlayer("PLAYER","My Game Reviewer in Testing. Email me if needed: (EMAIL)")


api.start_api(23764)
print("Started")

