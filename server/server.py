from typing import Union, Annotated

from fastapi import FastAPI, File

app = FastAPI()


@app.post("/")
async def upload_image(file: Annotated[bytes, File()]):
    return {"scores": {"hiphop": 0.9, "renaissance": 0.0, "gleb": 6.5}}
