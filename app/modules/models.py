# Import all models here so Base.metadata is populated for Alembic
from app.modules.organizations.models.organization import Organization  # noqa: F401
from app.modules.users.models.user import User  # noqa: F401
