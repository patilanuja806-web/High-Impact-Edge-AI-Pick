from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from fastapi.middleware.cors import CORSMiddleware
from backend.app.api.v1 import (
    endpoints_ingest,
    endpoints_trajectory,
    endpoints_traffic,
    endpoints_watchlist
)
from backend.app.api.websocket import ws_manager

app = FastAPI(title="NetraGati ANPR & Trajectory Analytics API", version="1.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(endpoints_ingest.router, prefix="/api/v1/ingest", tags=["Ingest"])
app.include_router(endpoints_trajectory.router, prefix="/api/v1/trajectory", tags=["Trajectory"])
app.include_router(endpoints_traffic.router, prefix="/api/v1/traffic", tags=["Traffic Analytics"])
app.include_router(endpoints_watchlist.router, prefix="/api/v1/watchlist", tags=["Watchlist"])

@app.websocket("/ws/live")
async def websocket_endpoint(websocket: WebSocket):
    await ws_manager.connect(websocket)
    try:
        while True:
            await websocket.receive_text()
    except WebSocketDisconnect:
        ws_manager.disconnect(websocket)

@app.get("/health")
def health_check():
    return {"status": "HEALTHY", "system": "NetraGati Core"}
