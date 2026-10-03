from dataclasses import dataclass
from fastapi import FastAPI, HTTPException
from core.gameReviewer import review as r
from chess import Board, Move
import threading, uvicorn
import time
from core import dataHandler as dh
from core.api import chesscom as cc
from fastapi.middleware.cors import CORSMiddleware
import requests

global players 
players = dh.load(dh.PLAYERS_PATH) 

app = FastAPI()
appIdentifier = "TypeFish (https://github.com/Satnav206795/TypeFish)"

@app.get("/health")
def health():
    return {"status": "ok"}


def start_api(host="127.0.0.1", port=8000):
    config = uvicorn.Config(app, host=host,port=port)
    server = uvicorn.Server(config)

    app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
    )

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
class PlayerRequest:
    username: str

@app.post("/chesscom/players/create")
def createChesscomPlayer(req: PlayerRequest) -> bool:
    if req.username.lower() in dh.load(dh.PLAYERS_PATH):
        raise HTTPException(status_code=409, detail="Player already exists")

    try:
        exists = cc.chesscom_user_exists(req.username, appIdentifier)
    except requests.RequestException:
        raise HTTPException(status_code=502, detail="Could not reach chess.com")

    if not exists:
        raise HTTPException(status_code=404, detail="Chess.com user not found")

    player = cc.ChessComPlayer(req.username, appIdentifier)
    dh.save(player, dh.PLAYERS_PATH)
    return True

@app.post("/chesscom/players/delete")
def deleteChesscomPlayer(req: PlayerRequest) -> bool:
    if not dh.delete(req.username, dh.PLAYERS_PATH):
        raise HTTPException(status_code=404, detail="Player not found")
    return True

@app.get("/chesscom/players/get")
async def getAllChesscomPlayers() -> dict[str,dict]:
    players = dh.load(dh.PLAYERS_PATH)
    return players

@app.get("/chesscom/games/{username}/month/all") 
def getAllGames(username : str) -> list[str]:
    player = dh.constructPlayer(username)

    months = player.get_all_months_played()
    for i in range(len(months)):
        months[i] = months[i].removeprefix(f"https://api.chess.com/pub/player/{username}/games/")

    return months

@app.get("/chesscom/games/{username}/month/{year}/{month}") 
def getAllGamesInMonth(username : str, year : int, month : int) -> list[dict]:
    player = dh.constructPlayer(username)
    games = player.get_games_in_month(year,month)
    return games