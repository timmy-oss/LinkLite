from fastapi import APIRouter, Request
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse
from models.settings import Settings



settings = Settings()


router = APIRouter()


templates = Jinja2Templates(directory  = "templates/")



@router.get("/ping", response_class= HTMLResponse)
async def ping( request : Request):
   return templates.TemplateResponse("ping.html", {"request" : request})



@router.get("/", response_class= HTMLResponse)
async def ping( request : Request):
   return templates.TemplateResponse("index.html", {"request" : request})
