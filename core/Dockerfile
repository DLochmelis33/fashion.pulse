FROM python:3.10

COPY src/requirements.txt /requirements.txt

RUN pip install --no-cache-dir --upgrade -r /requirements.txt

COPY src /src

COPY artifacts/current_model.ckpt /model.ckpt

COPY data/classes_labels.json /data/classes_labels.json 

ENV MODEL_CKPT=/model.ckpt
ENV DATA_DIR=/data

WORKDIR /src
CMD ["python", "-m", "uvicorn", "server.server:app", "--host", "0.0.0.0", "--port", "8000"]
