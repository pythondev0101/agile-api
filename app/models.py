from sqlalchemy.ext.declarative import declarative_base  # type: ignore
from sqlalchemy import Column, Integer, String  # type: ignore
from typing import Any

Base = declarative_base()  # type: Any


class Values(Base):
    __tablename__ = "values"
    id = Column(Integer, primary_key=True)
    data = Column(String(255), nullable=False)


class Principles(Base):
    __tablename__ = "principles"
    id = Column(Integer, primary_key=True)
    data = Column(String(255), nullable=False)
