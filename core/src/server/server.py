from typing import Union, Annotated
from fastapi import FastAPI, UploadFile

from models.predict import load_eval_model, predict
from utils.env_utils import read_env_var

app = FastAPI()
model = load_eval_model(read_env_var('MODEL_CKPT'))


@app.get("/")
async def healthcheck():
    return "OK"


@app.post("/analyze")
async def upload_image(image: UploadFile):
    img_bytes = await image.read()
    scores = predict(img_bytes, model)
    return {"scores": scores}
