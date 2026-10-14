import datetime
import os
from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles

from app.db import init_db
from app.routes.auth import router as auth_router
from app.routes.accounts import router as accounts_router
from app.routes.transfers import router as transfers_router
from app.routes.cards import router as cards_router
from app.routes.onboarding import router as onboarding_router
from app.routes.dashboard import router as dashboard_router


@asynccontextmanager
async def lifespan(app: FastAPI):
    init_db()
    yield


app = FastAPI(
    title="Enterprise Digital Banking Platform",
    description="Unified financial core platform for omnichannel digital banking touchpoints",
    version="1.0.0",
    lifespan=lifespan
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/health")
def health_check():
    return {
        "status": "ok",
        "service": "enterprise-digital-banking",
        "timestamp": datetime.datetime.utcnow().isoformat()
    }


# Include API Routers under /api/v1
app.include_router(auth_router, prefix="/api/v1")
app.include_router(accounts_router, prefix="/api/v1")
app.include_router(transfers_router, prefix="/api/v1")
app.include_router(cards_router, prefix="/api/v1")
app.include_router(onboarding_router, prefix="/api/v1")
app.include_router(dashboard_router, prefix="/api/v1")

# Mount Static Files
public_dir = os.path.join(os.path.dirname(__file__), "..", "public")
if os.path.exists(public_dir):
    pages_dir = os.path.join(public_dir, "pages")
    if os.path.exists(pages_dir):
        app.mount("/pages", StaticFiles(directory=pages_dir), name="pages")
    app.mount("/", StaticFiles(directory=public_dir, html=True), name="public")
