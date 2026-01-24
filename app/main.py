from __future__ import annotations

from fastapi import FastAPI, HTTPException, Query
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from starlette.requests import Request

from app.bot_state import BotState
from app.config import settings
from app.questrade_client import QuestradeClient

app = FastAPI(title=settings.app_name)
app.mount("/static", StaticFiles(directory="app/static"), name="static")

templates = Jinja2Templates(directory="app/templates")
client = QuestradeClient()
state = BotState()


@app.get("/", response_class=HTMLResponse)
async def index(request: Request) -> HTMLResponse:
    return templates.TemplateResponse(
        "index.html",
        {
            "request": request,
            "app_name": settings.app_name,
            "environment": settings.environment,
        },
    )


@app.get("/api/status")
async def status() -> dict[str, object]:
    return {
        "running": state.running,
        "mode": state.mode,
        "strategy": state.strategy,
        "last_action": state.last_action,
        "environment": settings.environment,
    }


@app.post("/api/bot/start")
async def start_bot() -> dict[str, str]:
    if state.running:
        return {"status": "already-running"}
    state.running = True
    state.last_action = "Started bot"
    state.log("Bot started in paper mode.")
    return {"status": "started"}


@app.post("/api/bot/stop")
async def stop_bot() -> dict[str, str]:
    if not state.running:
        return {"status": "already-stopped"}
    state.running = False
    state.last_action = "Stopped bot"
    state.log("Bot stopped.")
    return {"status": "stopped"}


@app.get("/api/bot/logs")
async def bot_logs() -> dict[str, list[str]]:
    return {"logs": list(state.logs)}


@app.get("/api/accounts")
async def accounts() -> dict[str, object]:
    try:
        accounts_data = client.get_accounts()
    except Exception as exc:
        raise HTTPException(status_code=502, detail=str(exc)) from exc
    return {"accounts": accounts_data}


@app.get("/api/quotes")
async def quotes(symbols: str = Query(..., description="Comma-separated list")) -> dict[str, object]:
    symbol_list = [symbol.strip() for symbol in symbols.split(",") if symbol.strip()]
    if not symbol_list:
        raise HTTPException(status_code=400, detail="No symbols provided.")
    try:
        quotes_data = client.get_quotes(symbol_list)
    except Exception as exc:
        raise HTTPException(status_code=502, detail=str(exc)) from exc
    return {"quotes": quotes_data}


@app.post("/api/orders")
async def create_order(payload: dict[str, object]) -> dict[str, object]:
    account_id = payload.get("account_id")
    if not account_id:
        raise HTTPException(status_code=400, detail="Missing account_id.")
    try:
        result = client.place_order(str(account_id), payload)
    except Exception as exc:
        raise HTTPException(status_code=502, detail=str(exc)) from exc
    state.last_action = f"Placed order for {account_id}"
    state.log(f"Order submitted for account {account_id}.")
    return result
