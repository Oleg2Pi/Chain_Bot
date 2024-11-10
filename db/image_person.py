from sqlalchemy import Column, Integer, ForeignKey, LargeBinary
from sqlalchemy.orm import relationship

from .base import BaseModel


class ImagePerson(BaseModel):
    __tablename__ = 'image_of_person'

    id = Column(Integer, primary_key=True, autoincrement=True)

    person_id = Column(Integer, ForeignKey('person.id'), nullable=False, unique=True)
    person = relationship('Person', back_populates='image')

    file = Column(LargeBinary)

    def __repr__(self):
        return f"<ImagePerson(id={self.id}, person_id={self.person_id})>"
