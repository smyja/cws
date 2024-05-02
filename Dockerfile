FROM python:3.8-slim-buster

ENV PYTHONUNBUFFERED 1

# Allows docker to cache installed dependencies between builds
SHELL ["/bin/bash", "-c"]
COPY ./requirements.txt requirements.txt
RUN pip install -vvv -r requirements.txt

# Adds our application code to the image
COPY . code
WORKDIR code

EXPOSE 8000

# Migrates the database, uploads staticfiles, and runs the production server
CMD ./manage.py migrate && \
    ./manage.py collectstatic --noinput && \
    newrelic-admin run-program gunicorn --bind 0.0.0.0:$PORT --access-logfile - flite.wsgi:application