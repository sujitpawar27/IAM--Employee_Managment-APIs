from sqlalchemy.orm import Session, joinedload
from sqlalchemy import text
from ..Models.employee_model import User
from ..Schema.employee_schema import UserCreate, UserUpdate

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
            d.name AS department_name
        FROM users u
        LEFT JOIN departments d
            ON u.department_id = d.id
    """)

    result = db.execute(query).mappings().all()

    users = []
    for row in result:
        users.append({
            "id": row["id"],
            "name": row["name"],
            "email": row["email"],
            "role": row["role"],
            "department": (
                {"name": row["department_name"]}
                if row["department_name"] is not None
                else None
            )
        })

    return users


def get_user(db: Session, user_id: int):
    return (
        db.query(User)
        .options(joinedload(User.department))
        .filter(User.id == user_id)
        .first()
    )

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