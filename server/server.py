from typing import Union, Annotated

from fastapi import FastAPI, UploadFile

app = FastAPI()


@app.post("/")
async def upload_image(image: UploadFile):
    return {"scores": {"hiphop": 0.9, "renaissance": 0.0, "gleb": 6.5}}
