# Questrade Gekko-Style Trading Bot (Python)

A Python trading bot inspired by the structure and UI of the Gekko trading bot. It ships with a FastAPI backend, a Gekko-like control panel, and a Questrade API client ready for paper trading or live execution.

## GitHub Setup

1. Create a new GitHub repository (e.g., `questrade-gekko-bot`).
2. Push this project to GitHub:

```bash
git remote add origin https://github.com/<your-username>/questrade-gekko-bot.git
git branch -M main
git push -u origin main
```

3. Add repository secrets or environment variables for `QUESTRADE_REFRESH_TOKEN` if using GitHub Actions or Codespaces.

## Features

- Gekko-inspired single-page UI (dashboard, market pulse, strategy, logs).
- FastAPI backend with bot control endpoints.
- Questrade API integration for accounts, quotes, and order placement.
- Docker + Gitpod ready.

## Quick Start (Local)

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
cp .env.example .env
uvicorn app.main:app --reload
```

Open <http://localhost:8000>.

## Docker

```bash
docker build -t questrade-bot .
docker run --rm -p 8000:8000 --env-file .env questrade-bot
```

## Gitpod

Create a Gitpod workspace and the app will start automatically. The preview opens on port 8000.

## Environment Variables

| Variable | Description |
| --- | --- |
| `QUESTRADE_REFRESH_TOKEN` | Questrade refresh token. Required for live API calls. |
| `QUESTRADE_PRACTICE` | `true` for practice mode. |
| `QUESTRADE_TIMEOUT` | Request timeout in seconds. |
| `BOT_ENV` | Environment label shown in the UI. |

## API Endpoints

- `GET /api/status` - Bot status.
- `POST /api/bot/start` - Start the bot.
- `POST /api/bot/stop` - Stop the bot.
- `GET /api/bot/logs` - Fetch recent logs.
- `GET /api/accounts` - Fetch accounts from Questrade.
- `GET /api/quotes?symbols=AAPL,MSFT` - Fetch quotes.
- `POST /api/orders` - Submit an order payload to Questrade.

## Notes

This template provides a clean foundation for adding strategies, scheduling, and persistent state. Make sure you store secrets securely when running in production.
