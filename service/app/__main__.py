from fastapi import FastAPI, HTTPException
import uvicorn
import traceback, os
import logging, logging.config
from database.db_crud import DatabaseInteraction
from app.schemas import Item, Resp

app = FastAPI()
repo = DatabaseInteraction()
logpath = os.environ["LOGGING_CONF"]
logging.config.fileConfig(fname=logpath, disable_existing_loggers=False)
logger = logging.getLogger(__name__)

@app.post("/repeater_bot/api/v1/post/")
def insert_word(item: Item):
    try:
        repo.insert_data(item.word, item.description)
    except Exception as err:
        logger.exception(traceback.format_exc())
        raise HTTPException from err


@app.get("/repeater_bot/api/v1/get/", response_model=Resp)
def select_word(item: Item):
    try:
        return repo.select_data(item.word)
    except Exception as err:
        logger.exception(traceback.format_exc())
        raise HTTPException from err


@app.put("/repeater_bot/api/v1/put/")
def update_word(item: Item):
    try:
        repo.update_data(item.word, item.new_word, item.new_description)
    except Exception as err:
        logger.exception(traceback.format_exc())
        raise HTTPException from err


@app.delete("/repeater_bot/api/v1/delete/{word}")
def delete_word(word: str):
    try:
        repo.delete_data(word)
    except Exception as err:
        logger.exception(traceback.format_exc())
        raise HTTPException from err


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)

