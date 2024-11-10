from sqlalchemy.exc import SQLAlchemyError

from .database import session_maker, logger
from db import Executor


class ExecutorDao:

    @staticmethod
    async def save(executor: Executor) -> Executor:
        logger.info("Starting to save executor: %s", executor)

        async with session_maker() as session:
            async with session.begin():
                try:
                    logger.debug("Merging executor: %s", executor)
                    await session.merge(executor)
                    await session.commit()
                    logger.info("Executor saved successfully: %s", executor)
                except SQLAlchemyError as e:
                    await session.rollback()
                    logger.error("Database error while saving executor: %s", str(e))
                    raise RuntimeError(f"Database error: {str(e)}") from e

        return executor
