from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from ..Database.deps import get_db
from ..Models.department_model import Department

router = APIRouter()

@router.get("")
def get_departments(db: Session = Depends(get_db)):
    return db.query(Department).all()
