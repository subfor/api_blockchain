FROM tiangolo/uvicorn-gunicorn:python3.9-alpine3.14

COPY ./requirements.txt /app/requirements.txt

RUN apk add gcc g++ make libffi-dev openssl-dev git

RUN pip install --no-cache-dir --upgrade -r /app/requirements.txt

COPY ./app /app