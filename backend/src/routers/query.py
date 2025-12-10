import time

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from src.auth.schemas import CurrentUserResponse
from src.auth.security import security, get_current_user
from src.core.db import get_session
# from src.crud import driver as driver_crud
# from src.schemas.user import UserRead

from authx import TokenPayload
from src.schemas.query import QueryResponse, QueryRequest

from src.modules.rag_system import rag

router = APIRouter(prefix="/query", tags=["query"])


@router.post("/", response_model=QueryResponse)
async def post_query(query_request: QueryRequest,
                     current_user: CurrentUserResponse = Depends(get_current_user),
                     session: AsyncSession = Depends(get_session)):
    return QueryResponse(answer=rag.interaction(query_request.question, query_request.context)[0].content, confidence=0.95, sources=[], related_topic=[])

