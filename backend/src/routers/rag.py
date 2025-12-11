import os
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

router = APIRouter(prefix="/rag", tags=["rag"])


@router.post("/query", response_model=QueryResponse)
async def post_query(query_request: QueryRequest,
                     current_user: CurrentUserResponse = Depends(get_current_user),
                     session: AsyncSession = Depends(get_session)):
    return QueryResponse(answer=rag.interaction(query_request.question, query_request.context), confidence=0.95, sources=[], related_topic=[])


@router.get("/docs")
async def get_documents():
    """Возвращает список документов из папки src/static/docs"""
    folder_path = "src/static/docs"

    # Проверяем существует ли папка
    if not os.path.exists(folder_path):
        return {"documents": [], "message": "Папка не найдена"}

    # Получаем список файлов
    files = []
    for filename in os.listdir(folder_path):
        file_path = os.path.join(folder_path, filename)
        if os.path.isfile(file_path):  # Проверяем что это файл, а не папка
            files.append(filename)

    # Сортируем по алфавиту
    files.sort()

    return {
        "documents": files,
        "count": len(files)
    }

