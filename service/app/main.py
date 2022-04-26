from fastapi import FastAPI

app = FastAPI()


@app.get("/")
def get_translation():
    return {"Hello": "John"}

if __name__ == "__main__":
    uvicorn.run(app)
