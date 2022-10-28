import httpx
import logging, logging.config
import os, traceback

logpath = os.environ["LOGGING_CONF"]
logging.config.fileConfig(fname=logpath, disable_existing_loggers=False)
logger = logging.getLogger(__name__)
back_url = os.environ["BACKEND_URL"]

class BackendClient:

    def search(self, word: str):
        resp = httpx.get(url=f"{back_url}/repeater_bot/api/v1/get/",
                         params={"item": word})
        data = resp.json()
        return data


    def add(self, word: str, description: str):
        resp = httpx.post(url=f"{back_url}/repeater_bot/api/v1/post/",
                          json={"word": word,
                                "description": description})
        data = resp.json()
        return data


    def change(self, word: str, new_word: str, new_description: str):
        resp = httpx.put(url=f"{back_url}/repeater_bot/api/v1/put/",
                         json={"word": word,
                               "new_word": new_word,
                               "new_description": new_description})
        data = resp.json()
        return data


    def delete(self, word: str):
        resp = httpx.delete(url=f"{back_url}/repeater_bot/api/v1/delete/",
                            params={"item": word})
        data = resp.json()
        return data


if __name__ == "__main__":
    pass
