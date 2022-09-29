import json
from urllib import request
import httpx

class BackendClient:

    def search(word: str):
        resp = httpx.get(url="http://localhost:8000/repeater_bot/api/v1/get/",
                         params={"word": word})
        # print(resp)
        # print(type(resp))
        # data = resp.text
        # print(type(data))
        # print(data)
        new_data = resp.json()
        print(new_data["description"])

    def add(word: str, description: str):
        resp = httpx.post(url=f"http://localhost:8000/api/post/",
                          json={"word": word,
                                "description": description})
        print(resp)
        print(type(resp))
        new_data = resp.json()
        print(new_data)
        print(type(new_data))
        print(resp.headers)
        print(resp.content)

    def change(word: str, new_word: str, new_description: str):

        resp = httpx.put(url="http://localhost:8000/api/put/",
                            json={"word": word,
                                "new_word": new_word,
                                "new_description": new_description})

        print(resp)
        print(type(resp))
        new_data = resp.json()
        print(new_data)
        print(type(new_data))
        print(resp.headers)
        print(resp.content)

    def delete(word: str):
        # resp = httpx.delete(url="http://localhost:8000/api/delete/{word}")
        resp = httpx.delete(url=f"http://localhost:8000/api/delete/{word}")

        print(resp)
        print(type(resp))
        new_data = resp.json()
        print(new_data)
        print(type(new_data))
        print(resp.headers)
        print(resp.content)


if __name__ == "__main__":
    BackendClient.delete(word="fish")

