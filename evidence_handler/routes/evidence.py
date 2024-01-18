from typing import Annotated

from fastapi import APIRouter, Path

import evidence_handler.dao.evidence as dao
from evidence_handler.models.evidence import BulkCreateRawEvidenceResponse, RawEvidence
from evidence_handler.routes.utils import get_serializer

router = APIRouter(prefix="/evidence/{id}")
EvidenceId: str = Path(..., min_length=1)


@router.post(
    "/{id}",
    response_description="Create new evidences",
    description="Create new evidences",
)
async def create_evidences(id: Annotated[str, EvidenceId], evidences: list[dict]) -> BulkCreateRawEvidenceResponse:
    """
    :param evidences:
    :param id:
    :return: BulkCreateRawEvidenceResponse
    """

    # I use bulk_create here because it's more reasonable than creating each evidence separately - do it in a one DB hit
    result = await dao.bulk_create([RawEvidence(evidence_id=id, evidence_data=evidence) for evidence in evidences])
    return BulkCreateRawEvidenceResponse(
        acknowledged=result.acknowledged,
    )


@router.get("/", response_description="List Evidences for evidence_id")
async def list_evidences(id: int) -> list[dict]:
    if (raw_evidences := await dao.list_(evidence_id=id)) is not None:
        raw_data = [raw_evidence.evidence_data for raw_evidence in raw_evidences]
        serializer = get_serializer(id)
        if serializer is not None:
            return [serializer.to_representation(evidence_data) for evidence_data in raw_data]
        return raw_data
