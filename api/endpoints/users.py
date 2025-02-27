from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List

from modules.auth import get_db, get_current_active_user
from models.user import User, UserCreate
from database.models import UserDB
from crud import crud as users_crud

router = APIRouter(
    prefix="/users",
    tags=["users"],
    responses={404: {"description": "Not found"}},
)


@router.post("/", response_model=User, status_code=status.HTTP_201_CREATED)
async def create_user(user: UserCreate, db: Session = Depends(get_db)):
    """
    Register a new user
    """
    db_user = users_crud.get_user(db, username=user.username)
    if db_user:
        raise HTTPException(
            status_code=400,
            detail="Username already registered"
        )
    return users_crud.create_user(db=db, user=user)


@router.get("/", response_model=List[User])
async def read_users(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db),
    current_user: UserDB = Depends(get_current_active_user)
):
    """
    Get a list of all users
    """
    users = users_crud.get_users(db, skip=skip, limit=limit)
    return [User(id=user.id, username=user.username) for user in users]


@router.get("/{user_id}", response_model=User)
async def read_user(
    user_id: int,
    db: Session = Depends(get_db),
    current_user: UserDB = Depends(get_current_active_user)
):
    """
    Get a user by ID
    """
    db_user = users_crud.get_user_by_id(db, user_id=user_id)
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return User(id=db_user.id, username=db_user.username)