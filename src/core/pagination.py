import math

from sqlalchemy import Select, func, select
from sqlalchemy.orm import Session

from src.core.schemas import PaginatedResponse, PaginationMeta


def paginate(
    db: Session,
    query: Select,
    page: int,
    page_size: int,
    count_query: Select | None = None,
) -> dict:
    if count_query is not None:
        total = db.scalar(count_query) or 0
    else:
        total = db.scalar(select(func.count()).select_from(query.subquery())) or 0

    data = db.scalars(query.offset((page - 1) * page_size).limit(page_size)).all()

    return PaginatedResponse(
        data=data,
        meta=PaginationMeta(
            total=total,
            page=page,
            page_size=page_size,
            total_pages=math.ceil(total / page_size) if total > 0 else 0,
        ),
    )
