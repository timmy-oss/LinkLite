
from fastapi import FastAPI, Request,Response,UploadFile, Form, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from models.settings import Settings
from router import router




app_settings = Settings()



app = FastAPI( debug= app_settings.debug, title=  app_settings.app_name, description= "The quintessential link shortener", version= "0.1.0" )

app.mount("/static", StaticFiles(directory="static"), name="static")


app.include_router(
    router = router,
    # prefix = "/v1"
)



app.add_middleware(
    CORSMiddleware,
    allow_origins= app_settings.allowed_origins,
    allow_credentials=False,
    allow_methods=["*"],
    allow_headers=["*"],
    max_age=3600,
    
)




   




