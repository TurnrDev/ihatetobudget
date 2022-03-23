FROM python:3.8

ENV PYTHONUNBUFFERED=1

WORKDIR /usr/src/app

# Note: Rust is required by `cryptography` (python package)
RUN apt-get update && apt-get -y install cron rustc

COPY Pipfile Pipfile
COPY Pipfile.lock Pipfile.lock
RUN pip install pipenv
RUN pipenv install --deploy --ignore-pipfile
RUN pipenv lock -r > requirements.txt
RUN pip install -r requirements.txt

COPY . .

RUN python manage.py collectstatic --noinput

RUN python manage.py crontab add
