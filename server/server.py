from typing import Union, Annotated

from fastapi import FastAPI, UploadFile

app = FastAPI()


@app.get("/")
async def healthcheck():
    return "OK"


@app.post("/analyze")
async def upload_image(image: UploadFile):
    return {"scores": {"hiphop": 0.9, "renaissance": 0.0, "gleb": 6.5}}
