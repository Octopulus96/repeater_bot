from service.database.db_connect import db_session
from service.database.db_models import Dictionary

class DatabaseInteraction():

    def insert_data(self, word: str, description: str) -> Dictionary:
        data = Dictionary(word=word, description=description)
        db_session.add(data)
        db_session.commit()

    def select_data(self, word: str) -> Dictionary:
        for item in db_session.query(Dictionary).filter(Dictionary.word == word):
            return item

    def update_data(self, word: str, new_word: str, new_description: str) -> Dictionary:
        for item in db_session.query(Dictionary).filter(Dictionary.word == word):
            item.word, item.description = new_word, new_description
            db_session.commit()

    def delete_data(self, word: str) -> Dictionary:
        data = db_session.query(Dictionary).filter(Dictionary.word == word)
        data.delete()
        db_session.commit()
