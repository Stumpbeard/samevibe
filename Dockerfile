FROM python:3.9.2
RUN pip install pipenv
WORKDIR /app

ADD Pipfile .
ADD Pipfile.lock .
RUN pipenv install --system

CMD flask run