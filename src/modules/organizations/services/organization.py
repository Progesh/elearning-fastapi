from sqlalchemy import select, update
from sqlalchemy.orm import Session

from src.modules.organizations.schemas.organization import (
    OrganizationCreate,
    OrganizationUpdate,
    OrganizationPatch,
)
from src.modules.organizations.models.organization import Organization
from src.core.pagination import paginate
from src.core.enums import Status as OrganizationStatus
from src.core.exceptions import NotFoundException


class OrganizationService:
    def __init__(self, db: Session):
        self.db = db

    def _get_active_organization(self, organization_id: int) -> Organization:
        organization = self.db.scalar(
            select(Organization)
            .where(Organization.id == organization_id)
            .where(Organization.status != OrganizationStatus.DELETED)
        )
        if not organization:
            raise NotFoundException("Organization not found")

        return organization

    def get_all(self, page: int = 1, page_size: int = 20) -> dict:
        query = select(Organization).where(
            Organization.status == OrganizationStatus.ACTIVE
        )
        return paginate(self.db, query, page, page_size)

    def get_by_id(self, organization_id: int) -> Organization:
        return self._get_active_organization(organization_id)

    def create(self, organization_data: OrganizationCreate) -> Organization:
        organization = Organization(**organization_data.model_dump())
        self.db.add(organization)
        self.db.commit()
        self.db.refresh(organization)

        return organization

    def update(
        self, organization_id: int, organization_data: OrganizationUpdate
    ) -> Organization:
        organization = self._get_active_organization(organization_id)

        self.db.execute(
            update(Organization)
            .where(Organization.id == organization_id)
            .values(**organization_data.model_dump())
        )
        self.db.commit()
        self.db.refresh(organization)

        return organization

    def partial_update(
        self, organization_id: int, organization_data: OrganizationPatch
    ) -> Organization:
        organization = self._get_active_organization(organization_id)
        for key, value in organization_data.model_dump(exclude_unset=True).items():
            setattr(organization, key, value)

        self.db.commit()
        self.db.refresh(organization)

        return organization

    def delete(self, organization_id: int):
        organization = self._get_active_organization(organization_id)
        organization.status = OrganizationStatus.DELETED
        self.db.commit()
