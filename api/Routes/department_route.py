from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from api.Database.deps import get_db
from api.Models.department_model import Department

router = APIRouter()

@router.get("")
def get_departments(db: Session = Depends(get_db)):
    return db.query(Department).all()
