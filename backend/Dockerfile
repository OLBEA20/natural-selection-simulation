FROM python:3.7

RUN pip install --upgrade \
    pipenv \
    gunicorn \
    gevent


COPY Pipfile .
COPY Pipfile.lock .
RUN pipenv install --system --deploy

WORKDIR /application
COPY src src
COPY main.py .

CMD gunicorn -k gevent -w 1 --bind=0.0.0.0:8000 main:app