from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from .routes import home_routes, uiEvent_routes, webhook_routes, websocket_routes
from .modules.agent_startup import initialize_schema_and_def

app = FastAPI()

# Set up CORS middleware
app.add_middleware(
    CORSMiddleware,
    #allow_origins=["*"],
    allow_origins=[
        "http://localhost:8000",
        "http://127.0.0.1:8000",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.mount("/static", StaticFiles(directory="static"), name="static")
app.include_router(uiEvent_routes.router, prefix="/ui-event")
app.include_router(webhook_routes.router, prefix="/webhook")
app.include_router(home_routes.router, prefix="")
app.include_router(websocket_routes.router)

@app.on_event("startup")
async def startup_event():
    await initialize_schema_and_def()