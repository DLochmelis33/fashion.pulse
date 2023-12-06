FROM python:3.10

ARG model_ckpt

COPY ../server_requirements.txt /server_requirements.txt

RUN pip install --no-cache-dir --upgrade -r /server_requirements.txt

COPY .. /src
COPY ${model_ckpt} /model.ckpt

ENV MODEL_CKPT=/model.ckpt

WORKDIR /src
CMD ["python", "-m", "uvicorn", "src.server.server:app", "--host", "0.0.0.0", "--port", "8000"]
