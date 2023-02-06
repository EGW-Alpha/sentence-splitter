import spacy
import typing
import os

from fastapi import FastAPI, Request, Form
from pydantic import BaseModel
from spacy.tokens import Span
from fastapi.templating import Jinja2Templates

model = os.getenv("SPACY_MODEL", "en_core_web_lg")
nlp = spacy.load(model)
nlp.add_pipe("sentencizer")

templates = Jinja2Templates(directory="templates")

app = FastAPI()


class Item(BaseModel):
    text: str


class Chunk(BaseModel):
    begin: int = 0
    end: int = 0
    text: str = ""
    length: int = 0


class Response(BaseModel):
    text: typing.List[Chunk] = []


def extract_chunk(sent: Span, with_text: bool, trim_spaces: bool) -> Chunk:
    begin = sent.start_char
    end = sent.end_char
    text = sent.text

    text_len = len(text)
    if trim_spaces:
        text = text.lstrip()
        begin = begin + text_len - len(text)

        text_len = len(text)
        text = text.rstrip()
        end = end - text_len + len(text)

    result = Chunk(begin=begin, end=end)
    if with_text:
        result.text = text
        result.length = len(text)
    return result


@app.get("/")
async def index(request: Request):
    return templates.TemplateResponse("index.html", context={'request': request})


@app.post("/sentence", response_model_exclude_unset=True)
async def split_sentence(text: str = Form(), with_text: bool = Form(default=False), trim_spaces: bool = Form(default=False)) -> Response:
    doc = nlp(text)
    return Response(text=[extract_chunk(sent, with_text, trim_spaces) for sent in doc.sents])
