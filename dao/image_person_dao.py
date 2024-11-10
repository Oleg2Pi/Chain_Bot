from sqlalchemy import select
from sqlalchemy.exc import SQLAlchemyError

from .database import session_maker, logger
from db import ImagePerson


class ImagePersonDao:

    @staticmethod
    async def save(image: ImagePerson) -> ImagePerson:
        async with session_maker() as session:
            async with session.begin():
                try:
                    session.add(image)
                    logger.info(f"Image saved: {image}")
                except SQLAlchemyError as e:
                    await session.rollback()
                    logger.error(f"Error saving image: {str(e)}")
                    raise RuntimeError(f"Database error: {str(e)}") from e

        return image

    @staticmethod
    async def find_by_person_id(person_id: int) -> ImagePerson | None:
        async with session_maker() as session:
            try:
                image_person = await session.execute(
                    select(ImagePerson).where(ImagePerson.person_id == person_id)
                )
                found_image = image_person.scalars().first()
                if found_image:
                    logger.info(f"Found image for person_id {person_id}: {found_image}")
                else:
                    logger.warning(f"No image found for person_id {person_id}")
                return found_image
            except SQLAlchemyError as e:
                logger.error(f"Error finding image by person_id: {str(e)}")
                raise RuntimeError(f"Database error: {str(e)}") from e
