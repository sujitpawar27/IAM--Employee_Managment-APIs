from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from ..Schema.employee_schema import UserCreate, UserUpdate, UserResponse
from ..controllers import employee_controller
from ..Database.deps import get_db
from ..controllers.employee_controller import get_user
router = APIRouter()

@router.post("/", response_model=UserResponse)
def create(user: UserCreate, db: Session = Depends(get_db)):
    return employee_controller.create_user(db, user)

@router.get("", response_model=list[UserResponse])
def read_all(db: Session = Depends(get_db)):
    return employee_controller.get_users(db)

@router.get("/{user_id}", response_model=UserResponse)
def get_user_by_id(user_id: int, db: Session = Depends(get_db)):
    user = get_user(db, user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user

@router.put("/{user_id}", response_model=UserResponse)
def update(user_id: int, data: UserUpdate, db: Session = Depends(get_db)):
    user = employee_controller.update_user(db, user_id, data)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user

@router.delete("/{user_id}")
def delete(user_id: int, db: Session = Depends(get_db)):
    success = employee_controller.delete_user(db, user_id)
    if not success:
        raise HTTPException(status_code=404, detail="User not found")
    return {"message": "User deleted"}


