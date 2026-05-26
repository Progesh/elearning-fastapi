# Import all models here so Base.metadata is populated for Alembic
from src.modules.organizations.models.organization import Organization  # noqa: F401
from src.modules.users.models.user import User  # noqa: F401
from src.modules.courses.models.course import Course  # noqa: F401
from src.modules.courses.models.course_type import CourseType  # noqa: F401
