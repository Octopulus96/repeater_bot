from fastapi import FastAPI

from service.database.db_crud import DatabaseInteraction

app = FastAPI()
repo = DatabaseInteraction()

@app.post("/post/{word}/{description}")
def insert_word(word: str, description: str):
    repo.insert_data(word, description)


@app.get("/get/{word}")
def select_word(word: str):
    return repo.select_data(word)


@app.put("/put/{word}/{new_word}/{new_description}")
def update_word(word: str, new_word: str, new_description: str):
    repo.update_data(word, new_word, new_description)


@app.delete("/delete/{word}")
def delete_word(word: str):
    repo.delete_data(word)
