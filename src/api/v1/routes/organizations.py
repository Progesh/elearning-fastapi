from fastapi import APIRouter, Query, status

from src.modules.organizations.schemas.organization import (
    OrganizationResponse,
    OrganizationCreate,
    OrganizationUpdate,
    OrganizationPatch,
)
from src.modules.organizations.services.organization import OrganizationService
from src.core.database import DbSession
from src.core.schemas import SingleResponse, PaginatedResponse

router = APIRouter()


@router.get("/", response_model=PaginatedResponse[OrganizationResponse])
def index(
    db: DbSession,
    page: int = Query(default=1, ge=1),
    page_size: int = Query(default=20, ge=1, le=100),
):
    return OrganizationService(db).get_all(page=page, page_size=page_size)


@router.get("/{organization_id}", response_model=SingleResponse[OrganizationResponse])
def show(organization_id: int, db: DbSession):
    return SingleResponse(data=OrganizationService(db).get_by_id(organization_id))


@router.post(
    "/",
    response_model=SingleResponse[OrganizationResponse],
    status_code=status.HTTP_201_CREATED,
)
def store(organization_data: OrganizationCreate, db: DbSession):
    return SingleResponse(data=OrganizationService(db).create(organization_data))


@router.put(
    "/{organization_id}",
    response_model=SingleResponse[OrganizationResponse],
)
def update(organization_id: int, organization_data: OrganizationUpdate, db: DbSession):
    return SingleResponse(
        data=OrganizationService(db).update(organization_id, organization_data)
    )


@router.patch("/{organization_id}", response_model=SingleResponse[OrganizationResponse])
def partial_update(
    organization_id: int, organization_data: OrganizationPatch, db: DbSession
):
    return SingleResponse(
        data=OrganizationService(db).partial_update(organization_id, organization_data)
    )


@router.delete("/{organization_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete(organization_id: int, db: DbSession):
    OrganizationService(db).delete(organization_id)
