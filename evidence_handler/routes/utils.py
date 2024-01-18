import logging

from beanie import PydanticObjectId
from bson.errors import InvalidId
from fastapi import HTTPException
from starlette import status

from evidence_handler.core.serializer import Serializer
from evidence_handler.scripts.utils import load_config

logger = logging.getLogger(__name__)

parsing_configurations = load_config()


async def validated_document_id(document_id: str) -> PydanticObjectId:
    """
    Validate document_id is a valid PydanticObjectId
    :param document_id: string representing document_id
    :raises HTTPException: if invalid document_id
    :return: PydanticObjectId
    """
    try:
        _document_id = PydanticObjectId(document_id)
    except InvalidId as exc:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Not found.") from exc
    return _document_id


def get_serializer(evidence_id: int) -> Serializer | None:
    """
    Get the serializer for a given evidence id
    """
    parsing_config = parsing_configurations.get(evidence_id, None)

    if not parsing_config:
        logger.warning(
            f"No parsing configuration found for evidence_id {evidence_id}. Returning evidence data without parsing."
        )

    return parsing_config
