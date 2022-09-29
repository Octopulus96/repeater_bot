from validation import Item
import uvicorn
from fastapi import FastAPI
from service.database.db_crud import DatabaseInteraction

repo = DatabaseInteraction()
app = FastAPI()

@app.get("/api/get/")
def select_word(item: Item):
    return repo.select_data(item.word)


@app.post("/api/post/")
def insert_word(item: Item):
    repo.insert_data(item.word, item.description)


@app.put("/api/put/")
def update_word(item:Item):
    repo.update_data(item.word, item.new_word, item.new_description)


@app.delete("/api/delete/{word}")
def delete_word(word: str):
    repo.delete_data(word)


if __name__ == "__main__":
        uvicorn.run(app)
