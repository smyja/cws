FROM library/python:3.8-slim-buster

RUN apt-get update \
    # dependencies for building Python packages
    && apt-get install -y build-essential \
    # psycopg2 dependencies
    && apt-get install -y libpq-dev \
    # Translations dependencies
    && apt-get install -y gettext \
    && apt-get install -y libcairo2 libpango-1.0-0 libpangocairo-1.0-0 libgdk-pixbuf2.0-0 libffi-dev shared-mime-info \
    # cleaning up unused files
    && apt-get purge -y --auto-remove -o APT::AutoRemove::RecommendsImportant=false \
    && rm -rf /var/lib/apt/lists/*

ENV PYTHONUNBUFFERED 1

# Allows docker to cache installed dependencies between builds
SHELL ["/bin/bash", "-c"]
COPY ./requirements.txt requirements.txt
RUN python --version

RUN pip install -vvv -r requirements.txt

# Adds our application code to the image
COPY . code
WORKDIR code

EXPOSE 8000

# Migrates the database, uploads staticfiles, and runs the production server
CMD ./manage.py migrate && \
    ./manage.py collectstatic --noinput && \
    newrelic-admin run-program gunicorn --bind 0.0.0.0:$PORT --access-logfile - flite.wsgi:application