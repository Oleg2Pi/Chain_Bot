from sqlalchemy import Column, Integer, ForeignKey
from sqlalchemy.orm import relationship

from .base import BaseModel


class Executor(BaseModel):
    __tablename__ = 'executor'

    id = Column(Integer, primary_key=True, autoincrement=True)

    person_id = Column(Integer, ForeignKey('person.id'), nullable=False, unique=True)
    person = relationship('Person', back_populates='executor')

    def __repr__(self):
        return f"<Executor(id={self.id}, person_id={self.person_id})>"
