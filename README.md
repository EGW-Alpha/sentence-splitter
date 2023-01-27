# Sentence splitter

Sentence splitter service for White Estate Document API

## Installation

```sh
$ pip install pipenv
$ pipenv install
$ pipenv run python -m spacy download en_core_web_lg
$ pipenv run uvicorn main:app

```

## How to run

```sh
$ pipenv run uvicorn main:app --port 8081 --host 0.0.0.0 --workers 4
```

## How to run with docker

Including spacy models in docker containers is usually a bad idea, so we
don't really provide any docker support. Feel free to implement it
on your own.

## Environment variables

* `SPACY_MODEL` - spacy model to load. By default, `en_core_web_lg`
