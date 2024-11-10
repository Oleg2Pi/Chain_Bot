from sqlalchemy import select

from .database import session_maker, logger
from db import Person


class PersonDao:
    @staticmethod
    async def save(person: Person):
        async with session_maker() as session:
            try:
                session.add(person)
                await session.commit()
                await session.refresh(person)

                logger.info(f"Person saved: {person}")

                return person
            except Exception as e:
                logger.error(f"Error saving person {e}")
                await session.rollback()

    @staticmethod
    async def update(person_id: int, updated_person: Person):
        async with session_maker() as session:
            try:
                person = await session.get(Person, person_id)
                if person:
                    person.first_name = updated_person.first_name
                    person.last_name = updated_person.last_name
                    person.username_tg = updated_person.username_tg
                    person.phone = updated_person.phone
                    await session.commit()
                    await session.refresh(person)
                    logger.info(f"Person updated: {person}")
                    return person
                else:
                    logger.warning(f"Person with id {person_id} not found.")
                    return None
            except Exception as e:
                logger.error(f"Error updating person: {e}")
                await session.rollback()

    @staticmethod
    async def find_by_chat_id(chat_id: int):
        async with session_maker() as session:
            try:
                result = await session.execute(select(Person).where(Person.chat_id == chat_id))
                person = result.scalars().first()
                logger.info(f"Person found by chat_id {chat_id}: {person}")
                return person
            except Exception as e:
                logger.error(f"Error finding person by chat ID: {e}")
