import re
from fastapi import FastAPI
import uvicorn
import traceback, os
import logging, logging.config
from service.database.db_crud import DatabaseInteraction
from service.app.schemas import Item

app = FastAPI()
repo = DatabaseInteraction()
logpath = os.environ["LOGGING_CONF"]
logging.config.fileConfig(fname=logpath, disable_existing_loggers=False)
logger = logging.getLogger(__name__)


@app.get("/repeater_bot/api/v1/get/", response_model=Item)
def select_word(item):
    data = repo.select_data(word=item)
    if data == None:
        Item.word = item
        return Item
    return data


@app.post("/repeater_bot/api/v1/post/", response_model=Item)
def insert_word(item: Item):
    check_word = repo.select_data(word=item.word)
    if check_word == None:
        new_item = repo.insert_data(word=item.word, description=item.description)
        return new_item
    return None


@app.put("/repeater_bot/api/v1/put/", response_model=Item)
def update_word(item: Item):
    check_word1 = repo.select_data(word=item.word)
    check_word2 = repo.select_data(word=item.new_word)
    if check_word1 or check_word2 == None:
        update_item = repo.update_data(item.word, item.new_word, item.new_description)
        return update_item
    return None


@app.delete("/repeater_bot/api/v1/delete/", response_model=Item)
def delete_word(item):
    check_word = repo.select_data(word=item)
    if check_word != None:
        delete_item = repo.delete_data(item)
        return delete_item
    Item.word = item
    return Item


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
