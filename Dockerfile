FROM python:3.8-slim-buster

ENV PYTHONUNBUFFERED 1

# Set the shell to Bash
SHELL ["/bin/bash", "-c"]

WORKDIR /app

COPY ./requirements.txt /app/requirements.txt
RUN which python
RUN python --version
RUN pip --version
RUN pip install -vvv -r /app/requirements.txt

COPY . /app

EXPOSE 8000

CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]