from sqlalchemy import Column, Integer, String, Date
from db import Base, engine

class Dictionary(Base):
    __tablename__ = "dictionary"
    uid = Column(Integer, primary_key=True)
    word = Column(String())
    description = Column(String())
    date = Column(Date())

    def __repr__(self):
        return f"Word: {self.word}"


if __name__ == "__main__":
    Base.metadata.create_all(engine)
