# ♟️ TypeFish

**A self-hostable chess game analyser.** Review your games move by move with Stockfish, pull your games straight from Chess.com, and run it however you like: as a bare API, as an API plus web UI, or as a native desktop app.

> **Project status:** early development. The backend API works today. The web UI, native apps and Docker image are planned and are marked as such below.

---

## Features

- **Full game review.** Paste a PGN and get every move classified with a comment, the engine's best move, and before/after evaluations (centipawns or mate-in-N).
- **Single move review.** Analyse one position and move from a FEN and a UCI move.
- **Chess.com integration.** Save players, list the months they've played, and fetch all games for any month.
- **Configurable depth.** Trade speed for accuracy with search depth and per-move time limits.
- **Open API.** Everything is a plain HTTP/JSON endpoint (FastAPI), with auto-generated docs at `/docs`.
- **Self-hostable.** Your games and analysis stay on your machine.

## Ways to run it

| Mode | What you get | Status |
|---|---|---|
| **API only** | Headless FastAPI server, bring your own client | ✅ Available |
| **API + Web UI** | API and browser interface served together | 🚧 Planned |
| **Native app** (Windows, Linux, macOS) | Desktop app that runs the API and UI together | 🚧 Planned |
| **Docker** | Self-hosted container, API only or API + Web UI | 🚧 Planned |

---

## Quick start (API only)

### Requirements

- Python 3.10+
- A [Stockfish](https://stockfishchess.org/download/) binary

### Install

```bash
git clone https://github.com/Satnav206795/TypeFish.git
cd TypeFish
pip install -r requirements.txt
```

### Add Stockfish

TypeFish currently looks for the engine at:

```
backend/engines/STOCKFISH.exe
```

Download Stockfish for your OS, put it in `backend/engines/`, and name it `STOCKFISH.exe` (on Linux/macOS, keep the name or change `STOCKFISH_PATH` in `backend/core/gameReviewer/review.py`). Make sure the file is executable on Linux/macOS (`chmod +x`).

### Run

From the repository root:

```bash
python -m backend.variants.windows.main
```

The API starts on **http://127.0.0.1:23764**. Check it with:

```bash
curl http://127.0.0.1:23764/health
# {"status":"ok"}
```

Interactive API docs are at http://127.0.0.1:23764/docs.

---

## API reference

### Health

| Method | Endpoint | Description |
|---|---|---|
| `GET` | `/health` | Returns `{"status": "ok"}` |

### Reviewing

| Method | Endpoint | Body | Description |
|---|---|---|---|
| `POST` | `/review/game` | `{"pgn": "...", "depth": 18, "maxTimePerMove": 0.3}` | Review every move in a PGN |
| `POST` | `/review/move` | `{"fen": "...", "moveUCI": "e2e4"}` | Review a single move from a position |

`depth` defaults to `18` and `maxTimePerMove` (seconds) to `0.3`.

### Chess.com players and games

| Method | Endpoint | Description |
|---|---|---|
| `POST` | `/chesscom/players/create` | Save a Chess.com player. Body: `{"username": "..."}` |
| `POST` | `/chesscom/players/delete` | Remove a saved player. Body: `{"username": "..."}` |
| `GET` | `/chesscom/players/get` | List all saved players |
| `GET` | `/chesscom/games/{username}/month/all` | List the months a player has games for |
| `GET` | `/chesscom/games/{username}/month/{year}/{month}` | Get all games in a given month |

Players must be created before their games can be fetched. Errors return standard HTTP codes: `404` (player not found), `409` (player already saved), `502` (Chess.com unreachable).

### Example

```bash
curl -X POST http://127.0.0.1:23764/review/game \
  -H "Content-Type: application/json" \
  -d '{"pgn": "1. e4 e5 2. Nf3 Nc6 3. Bb5 a6", "depth": 16, "maxTimePerMove": 0.2}'
```

---

## Web UI 🚧 *(planned)*

A browser interface for importing games, running reviews and browsing your Chess.com history. When released, you'll be able to choose whether to host **just the API** or **the API and web UI together**.

## Native app 🚧 *(planned)*

A desktop app for **Windows, Linux and macOS** that bundles the API and web UI and runs both locally with one click. No terminal or manual setup needed.

## Docker 🚧 *(planned)*

Self-host TypeFish with Docker, either as an API-only container or with the web UI included. The intended setup is a single image with Stockfish bundled and a mounted volume so your saved players persist. Instructions will be added here once the image is published.

---

## Configuration and data

- **Saved players** are stored in `backend/data/players.json`, created automatically on first run. For Docker, this directory is what you'll mount as a volume.
- **Host and port** are set in the `start_api(host, port)` call in the entry point. The default entry point uses `127.0.0.1:23764`. Use `0.0.0.0` to accept connections from other machines.
- **CORS** is currently open to all origins so a web UI on another port can talk to the API. Restrict this before exposing TypeFish to the internet.
- **Engine settings** (threads, hash size) live in `backend/core/gameReviewer/review.py`. It defaults to 1 thread and 256 MB hash for repeatable results; raise threads for more speed.

> ⚠️ TypeFish has no authentication. If you self-host it on a public network, put it behind a reverse proxy with auth or a VPN.

## Project structure

```
TypeFish/
├── backend/
│   ├── core/
│   │   ├── api/                # FastAPI app and Chess.com client
│   │   ├── gameReviewer/       # Stockfish-powered move/game review
│   │   └── dataHandler.py      # Saved player storage
│   ├── engines/                # Put your Stockfish binary here
│   └── variants/
│       ├── windows/            # Local entry point
│       └── docker/             # Container entry point (WIP)
├── requirements.txt
└── README.md
```

## Roadmap

- [x] Game and move review API
- [x] Chess.com player and game fetching
- [ ] Web UI
- [ ] API-only and API + UI hosting modes
- [ ] Docker image with bundled Stockfish
- [ ] Native apps for Windows, Linux and macOS
- [ ] Lichess support
- [ ] Authentication for self-hosted deployments

## Credits

- [Stockfish](https://stockfishchess.org/) for the engine
- [python-chess](https://github.com/niklasf/python-chess) for board and PGN handling
- [saulochess](https://pypi.org/project/saulochess/) for move classification
- [FastAPI](https://fastapi.tiangolo.com/) for the API
- [Chess.com Published-Data API](https://www.chess.com/news/view/published-data-api) for game data

## License

Released under the [GPL-3.0 license](LICENSE).