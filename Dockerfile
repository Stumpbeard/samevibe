FROM python:3.11.0a3

RUN pip install pipenv
WORKDIR /app

ADD Pipfile .
ADD Pipfile.lock .
RUN pipenv install --system

CMD flask run