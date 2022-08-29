from service.database.db_connect import db_session
from service.database.db_models import Dictionary
from service.logging.log_conf import log
import traceback
from sqlalchemy import exc

class DatabaseInteraction():

    def insert_data(self, word: str, description: str) -> Dictionary:
        try:
            data = Dictionary(word=word, description=description)
            db_session.add(data)
            db_session.commit()
        except Exception as err:
            log.exception(traceback.format_exc())
            raise exc.SQLAlchemyError from err


    def select_data(self, word: str) -> Dictionary:
        try:
            for item in db_session.query(Dictionary).filter(Dictionary.word == word):
                return item
        except Exception as err:
            log.exception(traceback.format_exc())
            raise exc.SQLAlchemyError from err


    def update_data(self, word: str, new_word: str, new_description: str) -> Dictionary:
        try:
            for item in db_session.query(Dictionary).filter(Dictionary.word == word):
                item.word, item.description = new_word, new_description
                db_session.commit()
        except Exception as err:
            log.exception(traceback.format_exc())
            raise exc.SQLAlchemyError from err


    def delete_data(self, word: str) -> Dictionary:
        try:
            data = db_session.query(Dictionary).filter(Dictionary.word == word)
            data.delete()
            db_session.commit()
        except Exception as err:
            log.exception(traceback.format_exc())
            raise exc.SQLAlchemyError from err
