"""Helpers para errores HTTP consistentes y legibles."""
from fastapi import HTTPException, status


def not_found(entity: str, entity_id: int) -> HTTPException:
    return HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail=f"{entity} with id={entity_id} not found",
    )


def conflict(message: str) -> HTTPException:
    return HTTPException(status_code=status.HTTP_409_CONFLICT, detail=message)
