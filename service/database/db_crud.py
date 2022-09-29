from database.db_connect import db_session
from database.db_models import Dictionary
from sqlalchemy import exc
import logging, logging.config
import traceback, os

logpath = os.environ["LOGGING_CONF"]
logging.config.fileConfig(fname=logpath, disable_existing_loggers=False)
logger = logging.getLogger(__name__)

class DatabaseInteraction():

    def insert_data(self, word: str, description: str):
        try:
            data = Dictionary(word=word, description=description)
            db_session.add(data)
            db_session.commit()
        except Exception as err:
            logger.exception(traceback.format_exc())
            raise exc.SQLAlchemyError from err


    def select_data(self, word: str):
        try:
            for item in db_session.query(Dictionary).filter(Dictionary.word == word):
                return item
        except Exception as err:
            logger.exception(traceback.format_exc())
            raise exc.SQLAlchemyError from err


    def update_data(self, word: str, new_word: str, new_description: str):
        try:
            for item in db_session.query(Dictionary).filter(Dictionary.word == word):
                item.word, item.description = new_word, new_description
                db_session.commit()
        except Exception as err:
            logger.exception(traceback.format_exc())
            raise exc.SQLAlchemyError from err


    def delete_data(self, word: str):
        try:
            data = db_session.query(Dictionary).filter(Dictionary.word == word)
            data.delete()
            db_session.commit()
        except Exception as err:
            logger.exception(traceback.format_exc())
            raise exc.SQLAlchemyError from err
