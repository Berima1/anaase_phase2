#!/usr/bin/env bash
set -e
if [ -f venv/bin/activate ]; then
  . venv/bin/activate
else
  python3 -m venv venv
  . venv/bin/activate
  pip install --upgrade pip
  pip install -r requirements.txt
fi
PORT=${PORT:-8000}
exec gunicorn -k uvicorn.workers.UvicornWorker service.app:app -w ${WEB_CONCURRENCY:-2} -b 0.0.0.0:${PORT}
