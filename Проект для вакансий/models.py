from sqlalchemy import Column, Integer, String
from database import Base

class Work(Base):
    __tablename__ = "Work_chernigiv"

    id = Column(Integer, primary_key=True, index=True)
    Work_name = Column(String(100), nullable=False)
    Salary = Column(String(100), nullable=False)
    City = Column(String(100), nullable=False)
    Info = Column(String(2000), nullable=False)
    
