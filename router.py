from fastapi import APIRouter, Request, Path
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse, RedirectResponse
from models.settings import Settings
from models.links import ShortenLinkInput, ShortLink, Click
from .db import redis_db


# Redis Initialization 

redis_db.json().set("shortlinks", "$",  [],  nx =True)




settings = Settings()


router = APIRouter()


templates = Jinja2Templates(directory  = "templates/")


@router.get("/{target}")
async def resolve_link_target( request : Request, target : str = Path() ):

   matching = redis_db.json().get( "shortlinks", f"$[?@.outputTarget == '{target}' ]" )

   if len(matching) == 0:

      return templates.TemplateResponse("not_found.html", {"request" :  Request, "target" : target } )


   else:

      shortlink = matching[0]

      # Do all the weird analytics shit 

      if( shortlink['enableTracking']):
         click = Click(
            shortlink = shortlink['id']
         )

         redis_db.json().arrappend("linkclicks", click.dict(by_alias = True) )
         redis_db.json().set( "shortlinks", f"$[?@.outputTarget == '{target}' ].clicks", shortlink['clicks'] + 1 )

      return RedirectResponse( shortlink["inputLink"] )










@router.get("/ping", response_class= HTMLResponse)
async def ping( request : Request):
   return templates.TemplateResponse("ping.html", {"request" : request})



@router.get("/", response_class= HTMLResponse)
async def ping( request : Request):
   return templates.TemplateResponse("index.html", {"request" : request})




@router.post("/ajax/shorten", response_model= ShortLink)
async def shorten_link( body : ShortenLinkInput ):
   
   shortlink =  ShortLink(
      input_link = body.input_link,
      input_link_hash = "input_link_hash",
      author = None,
      output_target = "output_target",
      enable_tracking = body.enable_tracking,
      validity = body.validity,
      is_custom = body.is_custom
   )


   # Save Link To DB 

   data = shortlink.dict(by_alias = True)

   redis_db.json().arrappend("shortlinks", data )

   return data
