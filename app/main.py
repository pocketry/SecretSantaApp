from typing import Annotated

from fastapi import FastAPI, Request, Depends, Form
from fastapi.responses import HTMLResponse, RedirectResponse, Response
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from sqlmodel import Session, SQLModel, create_engine, select

from app.santaRepository import santaRepository
from . import models

sqlite_file_name = "santas.db"
sqlite_url = f"sqlite:///{sqlite_file_name}"

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
    return RedirectResponse(url="/exchanges")
    # return templates.TemplateResponse(
    #     request=request, name="index.html"
    # )

@app.get("/exchanges", response_class=HTMLResponse)
def get_exchanges(
        request: Request,
        session: SessionDep,
        ):
    exchanges = session.exec(select(models.Exchange)).all()
    return templates.TemplateResponse(
        request=request, name="exchanges.html", context={"exchangeList": exchanges}
    )

@app.post("/exchanges")
def create_exchange(
        request: Request, 
        session: SessionDep, 
        exchangeName: Annotated[str, Form()]):
    exchange = models.Exchange(name=exchangeName)
    session.add(exchange)
    session.commit()
    session.refresh(exchange)
    headers = {"HX-Redirect": f"/exchanges/{exchange.id}"}
    return Response(status_code=201, headers=headers)

@app.get("/exchanges/{exchangeID}", response_class=HTMLResponse)
def get_santas(request: Request, session: SessionDep, exchangeID: int):
    exchange = session.exec(select(models.Exchange).where(models.Exchange.id == exchangeID)).first()
    # TODO: need to handle empty result
    # santaList = exchange.first().santaParticipants
    return templates.TemplateResponse(
        request=request, name="exchange.html", context={"name": exchange.name}
    )
