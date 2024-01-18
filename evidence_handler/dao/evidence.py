from pymongo.results import InsertManyResult

from evidence_handler.models.evidence import RawEvidence


async def list_(evidence_id: int) -> list[RawEvidence]:
    """
    list all evidences for a given evidence_id
    :param evidence_id: int
    :return: list[RawEvidence]
    """
    return await RawEvidence.find(RawEvidence.evidence_id == evidence_id).to_list()


async def bulk_create(evidences: list[RawEvidence]) -> InsertManyResult:
    """
    Bulk create evidences
    :param evidences: list of RawEvidence
    :return: InsertManyResult - the result of the insert_many operation
    """
    return await RawEvidence.insert_many(evidences)
