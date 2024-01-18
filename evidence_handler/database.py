from typing import Any, Final

from beanie import init_beanie
from beanie.odm.documents import Document
from motor.motor_asyncio import AsyncIOMotorClient

from evidence_handler.models.evidence import RawEvidence
from evidence_handler.settings import config

DOCUMENT_MODELS: Final[list[type[Document]]] = [
    RawEvidence,
]


async def init_db():
    client: Any = AsyncIOMotorClient(config.DB_CONNECTION_STRING)
    await init_beanie(
        database=client.get_database("evidence_handler"),
        document_models=DOCUMENT_MODELS,  # type: ignore
    )
