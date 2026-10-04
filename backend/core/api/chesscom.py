import requests
from dataclasses import dataclass, field


@dataclass
class ChessComPlayer:
    type: str = field(default="chesscom", init=False)
    username: str
    user_agent: str
    base_url: str = field(default="https://api.chess.com/pub", init=False)
    headers: dict = field(init=False, repr=False)

    def __post_init__(self):
        self.username = self.username.lower()
        self.headers = {"User-Agent": self.user_agent}


    def get_all_months_played(self) -> list[str] | None:
        url = f"{self.base_url}/player/{self.username}/games/archives"
        r = requests.get(url, headers=self.headers, timeout=10)
        if not r.ok:
            return None
        return r.json()["archives"]

    def get_games_in_month(self,year : int, month : int):
        url = constuctMonthArchiveUrl(self.username,year,month)
        r = requests.get(url,headers=self.headers)
        if not r.ok:
            return None
        return r.json()["games"]

def constuctMonthArchiveUrl(username : str, year : int, month : int):
    return f"https://api.chess.com/pub/player/{username}/games/{year}/{month}"

import requests

def chesscom_user_exists(username: str, user_agent: str) -> bool:
    r = requests.get(
        f"https://api.chess.com/pub/player/{username.lower()}",
        headers={"User-Agent": user_agent},
        timeout=10,
    )
    if r.status_code == 200:
        return True
    if r.status_code == 404:
        return False
    r.raise_for_status() 