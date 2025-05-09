from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from pydantic import BaseModel

from app.santaRepository import santaRepository

app = FastAPI()

app.mount("/static", StaticFiles(directory="./static"), name="static")

templates = Jinja2Templates(directory="./templates")

@app.get("/", response_class=HTMLResponse)
def get_exchanges(request: Request):
    
    return templates.TemplateResponse(
        request=request, name="index.html"
    )

@app.get("/santalist/{exchange}", response_class=HTMLResponse)
def get_santas(request: Request, exchange: str):
    santaList = santaRepository(exchange).getSantas(exchange)
    return templates.TemplateResponse(
        request=request, name="santas.html", context={"santaList": santaList}
    )
