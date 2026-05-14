from fastapi import APIRouter

router = APIRouter()

@router.get("/")
def read_users():
    return [{"username": "user1"}, {"username": "user2"}]