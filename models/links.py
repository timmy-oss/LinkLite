from pydantic import BaseModel, Field, AnyUrl, IPvAnyAddress
from uuid import uuid4
from typing import Union
from time import time


def uid():
    return uuid4().hex


class ShortenLinkInput(BaseModel):
    author : Union[None,str] = Field( default= None)
    enable_tracking : bool = Field(default= True, alias="enableTracking")
    is_custom : bool = Field(default= False, alias = "isCustom")
    custom_target : Union[str,None] = Field( default=None, alias="customTarget")
    input_link : AnyUrl = Field(alias= "inputLink" )
    validity : float = Field( ge = 0, le = 365,default = 0)
    custom_link : Union[str,None] = Field( default  = None, alias = "customLink")




    class Config:
        allow_population_by_field_name = True






class ShortLink(BaseModel):
    " Model for a shortened link "

    id  : str  = Field( default_factory= uid)
    input_link : AnyUrl = Field(alias= "inputLink" )
    author : Union[None,str] = Field( default= None)
    clicks : int = Field( default= 0, min = 0)
    output_target : str = Field( alias="outputTarget")
    created : float = Field( default_factory= time)
    last_updated : float = Field( default_factory= time, alias = "lastUpdated" )
    enable_tracking : bool = Field(default= True, alias="enableTracking")
    validity : float = Field( default = 0)
    is_custom : bool = Field(default= False, alias = "isCustom")
    is_valid : bool = Field( default = True, alias = "isValid")

    class Config:
        allow_population_by_field_name = True




class Click(BaseModel):
    " Model for a click on a shortlink "
    id  : str  = Field( default_factory= uid)
    shortlink : str
    created : float = Field( default_factory= time)
    ip_address : Union[IPvAnyAddress,None] = Field(default= None)


    class Config:
        allow_population_by_field_name = True







    