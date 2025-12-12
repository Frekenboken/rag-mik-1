import asyncio
from functools import lru_cache
from pathlib import Path
from typing import List, Dict
import time
from concurrent.futures import ThreadPoolExecutor
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from src.auth.schemas import CurrentUserResponse
from src.auth.security import security, get_current_user
from src.core.db import get_session
# from src.crud import driver as driver_crud
# from src.schemas.user import UserRead

from authx import TokenPayload
from src.schemas.query import QueryResponse, QueryRequest

from src.modules.rag_system import RAG

executor = ThreadPoolExecutor(max_workers=4)

router = APIRouter(prefix="/rag", tags=["rag"])


@lru_cache()
def get_rag() -> RAG:
    print("Инициализирую RAG...")
    return RAG('src/static/questions/', 'src/static/docs/', 'src/vector_db/', '*.md')


@router.post("/query", response_model=QueryResponse)
async def post_query(query_request: QueryRequest,
                     current_user: CurrentUserResponse = Depends(get_current_user),
                     rag=Depends(get_rag),
                     session: AsyncSession = Depends(get_session)):
    loop = asyncio.get_event_loop()

    # Выполняем CPU-bound операцию в отдельном потоке
    result = await loop.run_in_executor(
        executor,
        lambda: rag.interaction(query_request.question, query_request.context, k=10, d=3)  # ваша синхронная функция
    )
    return QueryResponse(answer=result, confidence=0.95,
                         sources=[], related_topic=[])


@router.get("/docs")
async def get_documents():
    """Возвращает список документов из папки src/static/docs"""
    folder_path = Path("src/static/docs")

    # Проверяем существует ли папка
    if not folder_path.exists() or not folder_path.is_dir():
        return {"documents": [], "message": "Папка не найдена"}

    # Получаем список файлов с детальной информацией
    documents = []

    for idx, file_path in enumerate(folder_path.iterdir(), start=1):
        if file_path.is_file():  # Проверяем что это файл
            # Получаем размер файла в байтах и конвертируем в мегабайты
            size_bytes = file_path.stat().st_size
            size_mb = size_bytes / (1024 * 1024)  # Конвертация в MB

            # Получаем расширение файла
            extension = file_path.suffix
            if extension:
                extension = extension[1:].lower()  # Убираем точку и приводим к нижнему регистру

            documents.append({
                "id": idx,
                "name": file_path.name,
                "size": round(size_mb, 2),  # Размер в MB с округлением до 2 знаков
                "extension": extension if extension else "unknown"
            })

    # Сортируем по имени файла
    documents.sort(key=lambda x: x["name"])

    return {
        "documents": documents,
        "count": len(documents)
    }
