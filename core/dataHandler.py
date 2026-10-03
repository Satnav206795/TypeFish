from pathlib import Path
import json
from dataclasses import asdict
from core.api import chesscom as cc


PLAYERS_PATH = Path(__file__).resolve().parent.parent / "data" / "players.json"
PLAYERS_PATH.parent.mkdir(parents=True, exist_ok=True) # Make if doesnt exsist


def save(player : cc.ChessComPlayer, path=PLAYERS_PATH):
    try:
        with open(path, "r", encoding="utf-8") as f:
            players = json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        players = {}

    players[player.username.lower()] = asdict(player)

    with open(path, "w", encoding="utf-8") as f:
        json.dump(players, f, indent=2)

def load(path=PLAYERS_PATH) -> dict[str, dict]:
    try:
        with open(path, "r", encoding="utf-8") as f:
            return json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        return {}