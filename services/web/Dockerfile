FROM python:3.8.1-slim-buster

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

RUN useradd -ms /bin/bash app

WORKDIR /home/app

RUN pip install --upgrade pip
RUN apt-get update
RUN apt-get -y upgrade
RUN apt-get install libglib2.0-0 -y libsm6 libxext6 libxrender-dev

COPY requirements.txt requirements.txt
RUN python -m venv venv
RUN pip install -r requirements.txt

COPY app app
COPY migrations migrations
COPY main.py config.py boot.dev.sh ./
RUN chmod a+x boot.dev.sh

ENV FLASK_APP main.py
ENV FLASK_DEBUG 1

RUN chown -R app:app ./
USER app

EXPOSE 5000
ENTRYPOINT ["./boot.dev.sh"]