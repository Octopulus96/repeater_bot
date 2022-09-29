from sqlalchemy import Column, Integer, String, Date
from database.db_connect import Base, engine
from datetime import date

class Dictionary(Base):
    __tablename__ = "dictionary"
    uid = Column(Integer(), primary_key=True)
    word = Column(String(20),nullable=False ,unique=True)
    description = Column(String(120), nullable=False)
    date_created = Column(Date(), default=date.today())
    date_updated = Column(Date(), default=date.today(), onupdate=date.today())

    def __repr__(self):
        return f"Word: {self.word}"


if __name__ == "__main__":
    Base.metadata.create_all(engine)
