import logging
from contextlib import asynccontextmanager

from fastapi import FastAPI
from starlette.responses import RedirectResponse

from evidence_handler.database import init_db
from evidence_handler.routes.evidence import router as evidences_router


@asynccontextmanager
async def lifespan(app_: "FastAPI"):
    await init_db()
    yield


app = FastAPI(lifespan=lifespan)

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app.include_router(evidences_router, tags=["evidences"], prefix="/api/v1")


@app.get("/health")
async def health():
    return {"status": "ok"}


@app.get("/", include_in_schema=False)
async def redirect_docs():
    return RedirectResponse("/docs")
