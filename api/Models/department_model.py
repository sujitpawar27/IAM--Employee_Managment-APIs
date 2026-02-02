from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship
from ..Database.db import Base

class Department(Base):
    __tablename__ = "departments"

    id = Column(Integer, primary_key=True)
    name = Column(String, unique=True)


    users = relationship("User", back_populates="department")
