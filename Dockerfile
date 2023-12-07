FROM python:3.7-alpine3.7

COPY requirements.txt requirements.txt

RUN python3.7 -m pip install -r requirements.txt

RUN mkdir /flask && \
    chmod o+rwx /flask

COPY api/ /flask/api

WORKDIR /flask/api

CMD python3.7 start_app.py