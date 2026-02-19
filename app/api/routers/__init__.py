from .voters import router as voters_router
from .candidates import router as candidates_router
from .votes import router as votes_router

__all__ = ["voters_router", "candidates_router", "votes_router"]
