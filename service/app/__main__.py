from fastapi import FastAPI, HTTPException
import uvicorn
from service.logging.log_conf import log
import traceback
from service.database.db_crud import DatabaseInteraction

app = FastAPI()
repo = DatabaseInteraction()

@app.post("/post/{word}/{description}")
def insert_word(word: str, description: str):
    try:
        repo.insert_data(word, description)
    except Exception as err:
        log.exception(traceback.format_exc())
        raise HTTPException from err


@app.get("/get/{word}")
def select_word(word: str):
    try:
        return repo.select_data(word)
    except Exception as err:
        log.exception(traceback.format_exc())
        raise HTTPException from err


@app.put("/put/{word}/{new_word}/{new_description}")
def update_word(word: str, new_word: str, new_description: str):
    try:
        repo.update_data(word, new_word, new_description)
    except Exception as err:
        log.exception(traceback.format_exc())
        raise HTTPException from err

@app.delete("/delete/{word}")
def delete_word(word: str):
    try:
        repo.delete_data(word)
    except Exception as err:
        log.exception(traceback.format_exc())
        raise HTTPException from err

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
