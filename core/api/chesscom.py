import requests
from dataclasses import dataclass, field


@dataclass
class ChessComPlayer:
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

    def get_games_in_month(self,archiveURL):
        url = archiveURL
        r = requests.get(url,headers=self.headers)
        if not r.ok:
            return None
        return r.json()["games"]
