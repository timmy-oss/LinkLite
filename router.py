from fastapi import APIRouter, Request, BackgroundTasks
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse, RedirectResponse
from models.settings import Settings
from models.links import ShortenLinkInput, ShortLink, Click
from db import redis_db
from nanoid import generate


# Redis Initialization 

redis_db.json().set("shortlinks", "$",  [],  nx =True)
redis_db.json().set("linktargets", "$",  [],  nx =True)
redis_db.json().set("linkclicks", "$",  [],  nx =True)
redis_db.json().set("zote", "$",  [],  nx =True)




settings = Settings()


router = APIRouter()


templates = Jinja2Templates(directory  = "templates/")


BASE_DOMAIN = settings.base_domain

RESERVED_WORDS = [ "main", "index", "ping", "input", "output", "css" ]



def generate_target():

   seed = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789_"
   N = 4
   M = 0
   target = generate(seed, N)
   matching = redis_db.json().get( "linktargets", f"$[?@ == '{target}' ]" )

   while len(matching) >= 1 or target in RESERVED_WORDS:
      M += 1
      target = generate(seed,N)
      matching = redis_db.json().get( "linktargets", f"$[?@ == '{target}' ]" )

      if M % 200 == 0 and M > 0:
         N += 1

   return target




def do_tracking(target,shortlink):
   click = Click(
            shortlink = shortlink['id']
         )

   redis_db.json().arrappend("linkclicks", "$", click.dict(by_alias = True) )
   redis_db.json().set( "shortlinks", f"$[?@.outputTarget == '{target}' ].clicks", shortlink['clicks'] + 1 )



def apply_updates(target, data):
   redis_db.json().arrappend( "linktargets", "$",  target )
   redis_db.json().arrappend("shortlinks", "$",  data )







# ROUTE HANDLERS


@router.get("/", response_class= HTMLResponse)
async def index( request : Request):
   
   return templates.TemplateResponse("index.html", {"request" : request, "base_domain" : BASE_DOMAIN})




@router.post("/ajax/shorten", response_model= ShortLink)
async def shorten_link( body : ShortenLinkInput, bg_tasks : BackgroundTasks ):

   target = generate_target()

   shortlink =  ShortLink(
      input_link = body.input_link,
      author = None,
      output_target = target,
      enable_tracking = body.enable_tracking,
      validity = body.validity,
      is_custom = body.is_custom
   )

   data = shortlink.dict(by_alias = True)

   bg_tasks.add_task(apply_updates, target, data)

   return data






@router.get("/{target}", response_class= HTMLResponse)
async def resolve_link_target( target : str, request : Request , bg_tasks : BackgroundTasks ):
   

   matching = redis_db.json().get( "shortlinks", f"$[?@.outputTarget == '{target}' ]" )

   if len(matching) == 0:

      return templates.TemplateResponse("not_found.html", { "target" : target, "base_domain" : BASE_DOMAIN, "request"  : request } )


   else:

      shortlink = matching[0]

      # Do analytics  

      if( shortlink['enableTracking']):
         bg_tasks.add_task(do_tracking, target, shortlink) 

      return RedirectResponse( shortlink["inputLink"] )


