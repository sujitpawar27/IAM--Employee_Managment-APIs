from sqlalchemy.orm import Session
from sqlalchemy import text
from api.Models.employee_model import User
from api.Schema.employee_schema import UserCreate, UserUpdate

def create_user(db: Session, user: UserCreate):
    db_user = User(**user.dict())
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user


def get_users(db: Session):
    query = text("""
        SELECT 
            u.id,
            u.name,
            u.email,
            u.role,
            d.name AS department
        FROM users u
        LEFT JOIN departments d
            ON u.department_id = d.id
    """)

    result = db.execute(query)
    return result.mappings().all()

def get_user(db: Session, user_id: int):
    return db.query(User).filter(User.id == user_id).first()

def update_user(db: Session, user_id: int, data: UserUpdate):
    user = get_user(db, user_id)
    if not user:
        return None

    for key, value in data.dict(exclude_unset=True).items():
        setattr(user, key, value)

    db.commit()
    db.refresh(user)
    return user

def delete_user(db: Session, user_id: int):
    user = get_user(db, user_id)
    if not user:
        return False

    db.delete(user)
    db.commit()
    return True

# def get_users_with_department_raw(db: Session):
#     query = text("""
#         SELECT
#             u.id,
#             u.name,
#             u.email,
#             u.role,
#             d.name AS department
#         FROM users u
#         LEFT JOIN departments d
#             ON u.department_id = d.id
#     """)
#
#     result = db.execute(query)
#     return result.mappings().all()