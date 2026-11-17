from sqlalchemy import Column, Integer, String
from database import Base

class Student(Base):

    __tablename__ = "students"

    roll_no = Column(
        Integer,
        primary_key=True,
        index=True
    )

    name = Column(
        String(100),
        nullable=False
    )

    division = Column(
        String(10),
        nullable=False
    )