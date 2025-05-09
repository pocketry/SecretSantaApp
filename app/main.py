from typing import Annotated

from fastapi import FastAPI, Request, Depends, Query
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from sqlmodel import Session, SQLModel, create_engine, select

from app.santaRepository import santaRepository
from app.models import *

sqlite_file_name = "santas.db"
sqlite_url = f"sqlite:///./db/{sqlite_file_name}"

connect_args = {"check_same_thread": False}
engine = create_engine(sqlite_url, connect_args=connect_args)

# def create_db_and_tables():
#     SQLModel.metadata.create_all(engine)

def get_session():
    with Session(engine) as session:
        yield session

SessionDep = Annotated[Session, Depends(get_session)]

app = FastAPI()

app.mount("/static", StaticFiles(directory="./static"), name="static")

templates = Jinja2Templates(directory="./templates")

@app.get("/", response_class=HTMLResponse)
def home(request: Request):
    return templates.TemplateResponse(
        request=request, name="index.html"
    )

@app.get("/exchanges", response_class=HTMLResponse)
def get_exchanges(
    request: Request,
    session: SessionDep,
    ) -> list[Exchange]:
    exchanges = session.exec(select(Exchange)).all()
    return templates.TemplateResponse(
        request=request, name="exchanges.html", context={"exchangeList": exchanges}
    )

@app.get("/santalist/{exchange}", response_class=HTMLResponse)
def get_santas(request: Request, exchange: str):
    santaList = santaRepository(exchange).getSantas(exchange)
    return templates.TemplateResponse(
        request=request, name="santas.html", context={"santaList": santaList}
    )
