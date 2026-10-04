from saulochess import chess_review as cr
import os
import chess.engine
from backend.core.gameReviewer.base import Eval,Result,GameReview

STOCKFISH_PATH = os.path.abspath(
    os.path.join(os.path.dirname(__file__), "..", "..", "engines", "STOCKFISH.exe")
)

engine = chess.engine.SimpleEngine.popen_uci(STOCKFISH_PATH)
engine.configure({"Threads": 1, "Hash": 256}) # Increase threads for less repeatble results

def analyiseMove(board : chess.Board, move : chess.Move, depth : int, maxTimePerMove : float) -> Result:

    engine.configure({"Clear Hash": None})
    cr.STOCKFISH_CONFIG = {"depth": depth, "time": maxTimePerMove}

    board = board.copy()
    classifictaion, comment, bestUCI, _ = cr.review_move(
        board,move,"",engine=engine,
    )

    evalBefore, mateInBefore = cr.evaluate(board, engine,return_mate_n=True)
    board.push(move)
    evalAfter, mateInAfter = cr.evaluate(board, engine,return_mate_n=True)

    eBefore = Eval(evalBefore,None) if abs(evalBefore) != 10000 else Eval(None,mateInBefore)
    eAfter = Eval(evalAfter,None) if abs(evalAfter) != 10000 else Eval(None,mateInAfter)

    result = Result(
        classifictaion,comment,bestUCI,move.uci(),eBefore,eAfter
    )

    return result

def analyiseGame(pgn : str, depth : int, maxTimePerMove : float) -> GameReview:
    moves, _, _ = cr.parse_pgn(pgn)

    results = []
    board = chess.Board()

    for i in range(len(moves)):
        result = analyiseMove(board,moves[i],depth,maxTimePerMove)
        results.append(result)

        board.push(moves[i])

    return GameReview(results)
