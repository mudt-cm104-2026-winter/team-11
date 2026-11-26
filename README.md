# PyPython

## What this is

PyPython is a Snake game for the browser, written in Python. The snake looks like a real python. There are two game modes: in **Classic** mode, hitting a wall ends the game; in **Teleport** mode, the snake comes out on the opposite side instead. Four kinds of food are worth 10, 30, 50 and 100 points, and each game mode has its own top 10 list with one best score per player.

It is for anyone who wants a quick game with a high score list.

**Where we are:** the server part (players, scores and the top 10) is built first and lives in this repository. The game screens are planned in the epic "Game Engine and Browser Interface" and are not in the repository yet. Until then, the start page is still the example page from the template.

## How to run it

You need Python 3.10 or newer.

```bash
python3 -m venv .venv
source .venv/bin/activate          # Windows: .venv\Scripts\activate
pip install -r requirements.txt
uvicorn app.main:app --reload
```

Then open http://127.0.0.1:8000 in your browser. Stop it with `Ctrl+C`.

The example page keeps its entries in memory: after a restart the list is empty again. Players and scores for the game are stored in the SQLite file `pypython.db`, which is created on the first start and is never committed to the repository.

## Team

| GitHub | Role |
|---|---|
| StBuerak | Backend: database, API and tests |
| dru-pixel | Page and login |
| solana3 | Documentation |

## How we work

- Every piece of work starts as an issue on our board. Issues are grouped in three epics, and each issue is a sub-issue of one of them.
- One branch per issue, named after it, for example `issue-9-api-endpoints`.
- Nobody pushes to `main`. Every change is a pull request that says what changed and why, and closes its issue with `closes #n`.
- Every pull request needs one approval from another team member. The reviewer reads the **Files changed** tab, comments on lines, and uses **Request changes** when something must be fixed. The author fixes it, and then the reviewer approves.
- The author merges after the approval. Every pull request adds one line to `CHANGELOG.md`.
- If two branches change the same line, the author of the second pull request merges `main` into their branch on their own laptop (`git fetch`, `git merge origin/main`), fixes the conflict and pushes.
- Commit messages say what changed, in small steps.

## Sources

- 2026-11-25: course sheets "Team Project and Assessment 1" and "Assessment 1: ten steps to stage-1", used for the Git process, the board and the README sections.

## Use of AI

- 2026-11-11: Claude (Anthropic), used to develope the first version of the Snake game in Python (rules, pixel-art look, login, leaderboard), checked by running and playing it
- 2026-11-12: Claude, used to improve the game (one score per player on the leaderboard, ranking effects, spacing of the food list), checked by running and playing it
- 2026-11-23: Claude, used to turn the game into a web app whose game code runs in the browser, with a backend for players and scores, checked by running it in the browser
- 2026-11-24: Claude, used to explain how to run it and to keep the backend in Python, checked by running it
- 2026-11-25: Claude, used to adapt the backend (`app/storage.py`, `app/main.py`) and tests to our FastAPI template, to split the game into small pieces (`app/static/game/`) and to plan the issues, epics and pull requests, checked by a teammate's review of each pull request
- 2026-11-26: Claude, used to explain the Git and GitHub steps and to draft pull request examples when needed, CHANGELOG lines, review comments and the first draft of this README, checked by doing the steps ourselves and reading the result on github.com

Claude did not push, merge, review or approve anything. The branches, pull requests, reviews and merges were made by the team.
