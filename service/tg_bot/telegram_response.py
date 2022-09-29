import httpx
import logging, logging.config
import os, traceback

logpath = os.environ["LOGGING_CONF"]
logging.config.fileConfig(fname=logpath, disable_existing_loggers=False)
logger = logging.getLogger(__name__)

class BackendClient:

    def search(self, word: str):
        try:
            resp = httpx.get(url="http://app:8000/repeater_bot/api/v1/get/",
                             params={"word": word})
            data = resp.json()
            logger.debug(f"{resp.encoding}, {resp.url}, {resp.text}")
            return data["description"]
        except Exception as exc:
            logger.exception(traceback.format_exc())
            raise httpx.HTTPStatusError(response=resp.status_code) from exc


    def add(self, word: str, description: str):
        try:
            resp = httpx.post(url=f"http://app:8000/repeater_bot/api/v1/post/",
                              json={"word": word,
                                    "description": description})
            logger.debug(f"{resp.encoding}, {resp.url}, {resp.text}")
        except Exception as exc:
            logger.exception(traceback.format_exc())
            raise httpx.HTTPStatusError(response=resp.status_code) from exc

    def change(self, word: str, new_word: str, new_description: str):
        try:
            resp = httpx.put(url="http://app:8000/repeater_bot/api/v1/put/",
                             json={"word": word,
                                   "new_word": new_word,
                                   "new_description": new_description})
            logger.debug(f"{resp.encoding}, {resp.url}, {resp.text}")
        except Exception as exc:
            logger.exception(traceback.format_exc())
            raise httpx.HTTPStatusError(response=resp.status_code) from exc


    def delete(self, word: str):
        try:
            resp = httpx.delete(url=f"http://app:8000/repeater_bot/api/v1/delete/{word}")
            logger.debug(f"{resp.encoding}, {resp.url}, {resp.text}")
        except Exception as exc:
            logger.exception(traceback.format_exc())
            raise httpx.HTTPStatusError(response=resp.status_code) from exc

if __name__ == "__main__":
    a = BackendClient()
    a.add(word="fish", description="рыба")
    a.search(word="fish")
    a.change(word="fish", new_word="main", new_description="основной")
    a.delete(word="main")

