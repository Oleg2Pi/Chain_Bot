from sqlalchemy.orm import relationship

from .base import BaseModel
from sqlalchemy import Column, Integer, VARCHAR, BIGINT

class Person(BaseModel):
    __tablename__ = 'person'

    id = Column(Integer, primary_key=True, autoincrement=True)
    first_name = Column(VARCHAR(255), nullable=True, name='first_name')
    last_name = Column(VARCHAR(255), nullable=True, name='last_name')
    username_tg = Column(VARCHAR(255), nullable=False, name='username_tg')
    phone = Column(VARCHAR(255), nullable=True)
    chat_id = Column(BIGINT, nullable=False, name='chat_id')

    image = relationship('ImagePerson', back_populates='person', cascade='all, delete-orphan')
    executor = relationship('Executor', back_populates='person', cascade='all, delete-orphan')

    def __str__(self) -> str:
        return f'{self.first_name} {self.last_name} {self.username_tg} {self.phone} {self.chat_id}'