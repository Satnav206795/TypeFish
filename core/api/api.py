from dataclasses import dataclass
from fastapi import FastAPI, HTTPException
from core.gameReviewer import review as r
from chess import Board, Move
import threading, uvicorn
import time
from core import dataHandler as dh
from core.api import chesscom as cc


global players 
players = dh.load(dh.PLAYERS_PATH) 

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
    depth: int = 18
    maxTimePerMove: float = 0.3

@app.post("/review/game")
async def reviewGame(req : reviewGameRequest) -> r.GameReview:
    return r.analyiseGame(req.pgn,req.depth,req.maxTimePerMove)


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

@app.post("/chesscom/players/create")
async def createChesscomPlayer(req : createPlayerRequest) -> bool:
    player = cc.ChessComPlayer(req.username,appIdentifier)
    dh.save(player,dh.PLAYERS_PATH)
    players = dh.load(dh.PLAYERS_PATH)
    return True

@app.get("/chesscom/players/get")
async def getAllChesscomPlayers() -> dict[str,dict]:
    return players



@app.get("/chesscom/games/{username}/month/all") 
def getAllGames(username: str) -> list[str]:
    data = dh.load().get(username.lower())
    if data is None:
        raise HTTPException(status_code=404, detail="Player not found")

    player = cc.ChessComPlayer(data["username"], data["user_agent"])

    return player.get_all_months_played()