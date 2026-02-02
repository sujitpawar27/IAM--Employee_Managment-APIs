from sqlalchemy.orm import Session, joinedload
from sqlalchemy import text
from loguru import logger
from ..Models.employee_model import User
from ..Schema.employee_schema import UserCreate, UserUpdate


def create_user(db: Session, user: UserCreate):
    try:
        db_user = User(**user.dict())
        db.add(db_user)
        db.commit()
        db.refresh(db_user)

        logger.info(f"User created successfully | id={db_user.id}")
        return db_user

    except Exception as e:
        logger.debug(f"{e}")
        raise



def get_users(db: Session):
    try:
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

        logger.info(f"Fetched {len(users)} users successfully")
        return users

    except Exception as e:
        logger.debug(f"{e}")
        raise



def get_user(db: Session, user_id: int):
    try:
        user = (
            db.query(User)
            .options(joinedload(User.department))
            .filter(User.id == user_id)
            .first()
        )

        if not user:
            logger.warning(f"User not found | id={user_id}")
            return None

        logger.info(f"User fetched successfully | id={user_id}")
        return user

    except Exception as e:
        logger.debug(f"{e}")
        raise


def update_user(db: Session, user_id: int, data: UserUpdate):
    try:
        user = get_user(db, user_id)
        if not user:
            logger.warning(f"User not found for update | id={user_id}")
            return None

        for key, value in data.dict(exclude_unset=True).items():
            setattr(user, key, value)

        db.commit()
        db.refresh(user)

        logger.info(f"User updated successfully | id={user_id}")
        return user

    except Exception as e:
        logger.debug(f"{e}")
        raise


def delete_user(db: Session, user_id: int):
    try:
        user = get_user(db, user_id)
        if not user:
            logger.warning(f"User not found for delete | id={user_id}")
            return False

        db.delete(user)
        db.commit()

        logger.info(f"User deleted successfully | id={user_id}")
        return True

    except Exception as e:
        logger.debug(f"{e}")
        raise

