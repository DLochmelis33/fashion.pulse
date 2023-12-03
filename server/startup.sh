#!/bin/bash

pip install -r requirements.txt
gunicorn server:app --workers 4 --worker-class uvicorn.workers.UvicornWorker --bind 0.0.0.0:80
