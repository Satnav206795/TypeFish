from dataclasses import dataclass
from fastapi import FastAPI
from core.gameReviewer import review as r
from chess import Board, Move
import threading, uvicorn
import time
from core import dataHandler as dh
from core.api import chesscom as cc

app = FastAPI()
appIdentifier = "TypeFish (https://github.com/Satnav206795/TypeFish)"

@app.get("/health")
def health():
    return {"status": "ok"}


def start_api(port=8000):
    config = uvicorn.Config(app, port=port)
    server = uvicorn.Server(config)

    t = threading.Thread(target=server.run, daemon=True)
    t.start()

    while not server.started: 
        time.sleep(0.05)

    return server


# --- Reviewing --- #

#Review Game
@dataclass(frozen=True)
class reviewGameRequest:
    pgn: str
    dpeth: int = 18

@app.post("/review/game")
async def reviewGame(req : reviewGameRequest) -> r.GameReview:
    return r.analyiseGame(req.pgn)


#Review Move
@dataclass(frozen=True)
class reviewMoveRequest:
    fen: str
    moveUCI: str
    dpeth: int = 18

@app.post("/review/move")
async def reviewMove(req : reviewMoveRequest) -> r.Result:
    board = Board(req.fen)
    move = Move.from_uci(req.moveUCI)
    return r.analyiseMove(board,move)

#Players
@dataclass(frozen=True)
class createPlayerRequest:
    username: str

@app.post("/players/create/chesscom")
async def createPlayer(req : createPlayerRequest) -> bool:
    player = cc.ChessComPlayer(req.username,appIdentifier)
    dh.save(player,dh.PLAYERS_PATH)
    return True