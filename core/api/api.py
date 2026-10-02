from dataclasses import dataclass
from fastapi import FastAPI
from gameReviewer import review as r
from chess import Board, Move

app = FastAPI()

@app.get("/health")
def health():
    return {"status": "ok"}


#Review Game
@dataclass
class reviewGameRequest:
    pgn: str
    dpeth: int = 18

@app.post("/review/game")
async def reviewGame(req : reviewGameRequest) -> r.GameReview:
    return r.analyiseGame(req.pgn)


#Review Move
@dataclass
class reviewMoveRequest:
    fen: str
    moveUCI: str
    dpeth: int = 18

@app.post("/review/move")
async def reviewMove(req : reviewMoveRequest) -> r.Result:
    board = Board(req.fen)
    move = Move.from_uci(req.moveUCI)
    return r.analyiseMove(board,move)