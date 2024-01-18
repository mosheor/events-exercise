import pymongo
from beanie import Document
from pydantic import BaseModel
from pymongo import IndexModel


class BulkCreateRawEvidence(BaseModel):
    evidence_id: int
    evidence_data: list[dict]


class BulkCreateRawEvidenceResponse(BaseModel):
    acknowledged: bool


class RawEvidence(Document):
    evidence_id: int
    evidence_data: dict

    class Settings:
        name = "raw_evidence"
        indexes = [
            IndexModel(
                [("evidence_id", pymongo.ASCENDING)],
                name="evidence_id_index",
                unique=False,
            ),
        ]
