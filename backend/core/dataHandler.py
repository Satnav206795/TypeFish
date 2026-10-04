from pathlib import Path
import json
from dataclasses import asdict
from backend.core.api import chesscom as cc
from fastapi import HTTPException
import threading


PLAYERS_PATH = Path(__file__).resolve().parent.parent / "data" / "players.json"
PLAYERS_PATH.parent.mkdir(parents=True, exist_ok=True) # Make if doesnt exsist

file_lock = threading.Lock()

def save(player: cc.ChessComPlayer, path=PLAYERS_PATH):
    with file_lock:
        try:
            with open(path, "r", encoding="utf-8") as f:
                players = json.load(f)
        except (FileNotFoundError, json.JSONDecodeError):
            players = {}

        players[player.username.lower()] = asdict(player)

        with open(path, "w", encoding="utf-8") as f:
            json.dump(players, f, indent=2)


def delete(username: str, path=PLAYERS_PATH) -> bool:
    with file_lock:
        try:
            with open(path, "r", encoding="utf-8") as f:
                players = json.load(f)
        except (FileNotFoundError, json.JSONDecodeError):
            return False

        if players.pop(username.lower(), None) is None:
            return False

        with open(path, "w", encoding="utf-8") as f:
            json.dump(players, f, indent=2)

    return True

def load(path=PLAYERS_PATH) -> dict[str, dict]:
    try:
        with open(path, "r", encoding="utf-8") as f:
            return json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        return {}

def constructPlayer(username : str) -> cc.ChessComPlayer:
    data = load().get(username.lower())
    if data is None:
        raise HTTPException(status_code=404, detail="Player not found")

    player = cc.ChessComPlayer(data["username"], data["user_agent"])
    return player

