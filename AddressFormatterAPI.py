#python -m uvicorn AddressFormatterAPI:app --reload
from fastapi import FastAPI, Request, status, Security, Depends, FastAPI, HTTPException
from pydantic import BaseModel
from typing import Optional
from fastapi.encoders import jsonable_encoder
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from fastapi.security.api_key import APIKeyQuery, APIKeyCookie, APIKeyHeader, APIKey
from fastapi.openapi.docs import get_swagger_ui_html
from fastapi.openapi.utils import get_openapi
from starlette.status import HTTP_403_FORBIDDEN
from starlette.responses import RedirectResponse, JSONResponse

API_KEY = "UIDAI12345"
API_KEY_NAME = "access_token"
COOKIE_DOMAIN = "localtest.me"

api_key_query = APIKeyQuery(name=API_KEY_NAME, auto_error=False)
api_key_header = APIKeyHeader(name=API_KEY_NAME, auto_error=False)
api_key_cookie = APIKeyCookie(name=API_KEY_NAME, auto_error=False)

app = FastAPI(docs_url=None, redoc_url=None, openapi_url=None, title="Address Formatter API")

async def get_api_key(
    api_key_query: str = Security(api_key_query),
    api_key_header: str = Security(api_key_header),
    api_key_cookie: str = Security(api_key_cookie),
):

    if api_key_query == API_KEY:
        return api_key_query
    elif api_key_header == API_KEY:
        return api_key_header
    elif api_key_cookie == API_KEY:
        return api_key_cookie
    else:
        raise HTTPException(
            status_code=HTTP_403_FORBIDDEN, detail="Could not validate credentials"
        )

@app.get("/")
async def homepage():
    return {"Details":"This is an address formatter API"}

@app.get("/openapi.json", tags=["Security"])
async def get_open_api_endpoint(api_key: APIKey = Depends(get_api_key)):
    response = JSONResponse(
        get_openapi(title="Address Formatter API", version=1, routes=app.routes)
    )
    return response

@app.get('/format_address')
async def front(api_key: APIKey = Depends(get_api_key)):
    response = get_swagger_ui_html(openapi_url="/openapi.json", title="docs")
    response.set_cookie(
        API_KEY_NAME,
        value=api_key,
        domain=COOKIE_DOMAIN,
        httponly=True,
        max_age=1800,
        expires=1800,
    )
    return response

@app.get("/logout")
async def route_logout_and_remove_cookie():
    response = RedirectResponse(url="/")
    response.delete_cookie(API_KEY_NAME, domain=COOKIE_DOMAIN)
    return response

 
#app = FastAPI()

@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):
    return JSONResponse(
        status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
        content=jsonable_encoder({"detail": exc.errors(), "Error": "One of the required field is either missing or in wrong format"}),
    )

class Label(BaseModel):
    building:Optional[str] = None
    street:Optional[str] = None
    landmark:Optional[str] = None
    locality:Optional[str] = None
    vtc:Optional[str] = None
    district:Optional[str] = None
    state:Optional[str] = None
 
class Address(BaseModel):
    lang:str
    addr:Label

class FullAddress(BaseModel):
    engAddress:Address
    localAddress:Optional[Address] = None
    class Config:
        schema_extra = {
            "example": {
                        "engAddress": {
                            "lang": "en",
                            "addr": {
                            "building": "No. 40",
                            "street": "Store Street",
                            "landmark": "Near Popular Nursing Home",
                            "locality": "Kalasipalya",
                            "vtc": "Coimbatore",
                            "district": "Coimbatore",
                            "state": "Tamil Nadu"
                            }
                        },
                        "localAddress": {
                            "lang": "ta",
                            "addr": {
                            "building": "எண் 40",
                            "street": "ஸ்டோர் தெரு",
                            "landmark": "பாப்புலர் நர்சிங் ஹோம் அருகில்",
                            "locality": "கலாசிபால்யா",
                            "vtc": "கோவை",
                            "district": "கோவை",
                            "state": "தமிழ்நாடு"
                            }
                        }                        
            }
        }

class Response(BaseModel):
    GivenAddress:Optional[FullAddress] = None
    FormattedAddress:Optional[FullAddress] = None
    class Config:
        schema_extra = {
            "example": {
                200: {
                        "GivenAddress": {
                            "engAddress": {
                                "lang": "en",
                                "addr": {
                                "building": "No. 40",
                                "street": "Store Street",
                                "landmark": "Near Popular Nursing Home",
                                "locality": "Kalasipalya",
                                "vtc": "Coimbatore",
                                "district": "Coimbatore",
                                "state": "Tamil Nadu"
                                }
                            },
                            "localAddress": {
                                "lang": "ta",
                                "addr": {
                                "building": "எண் 40",
                                "street": "ஸ்டோர் தெரு",
                                "landmark": "பாப்புலர் நர்சிங் ஹோம் அருகில்",
                                "locality": "கலாசிபால்யா",
                                "vtc": "கோவை",
                                "district": "கோவை",
                                "state": "தமிழ்நாடு"
                                }
                            }
                        },
                        "FormattedAddress": {
                            "engAddress": {
                                "lang": "en",
                                "addr": {
                                "building": "No. 40",
                                "street": "Store Street",
                                "landmark": "Near Popular Nursing Home",
                                "locality": "Kalasipalya",
                                "vtc": None,
                                "district": "Coimbatore",
                                "state": "Tamil Nadu"
                                }
                            },
                            "localAddress": {
                                "lang": "ta",
                                "addr": {
                                "building": "எண் 40",
                                "street": "ஸ்டோர் தெரு",
                                "landmark": "பாப்புலர் நர்சிங் ஹோம் அருகில்",
                                "locality": "கலாசிபால்யா",
                                "vtc": None,
                                "district": "கோவை",
                                "state": "தமிழ்நாடு"
                                }
                            }
                        }
                    }
                                             
            }
        }


def initialFormat(string):
    if string == None or string=="Null" or string=="NULL":
        string=" "
    string.title().strip()
    return string

def format(string:str):
    if string == "" or string=="," or string==" " or string==None:
        return None 
    string = string.replace(",,",",")
    string = string.replace(", ,",",")
    if string[0]==",":
        string[0]=""
    if string[-1]==",":
        string[-1]=""
    string.strip()
    if string == "" or string=="," or string==" ":
        return None   
    return string 

def merge1(a,b):
    list_a = a.split(',')
    list_b = b.split(',')
    common_elements = set(list_a).intersection(list_b)
    for c in common_elements:
        i = list_b.index(c)
        list_b[i] = ""
        if len(list_b)>2:
            b = ",".join(map(str,list_b))
        else:
            b = "".join(map(str,list_b))
    #b = format(str(b))
    return [str(a),str(b)]

def merge2(a,b,c,d):
    list_a = a.split(',')
    list_b = b.split(',')
    list_d = d.split(',')
    common_elements = set(list_a).intersection(list_b)
    for c in common_elements:
        i = list_b.index(c)
        list_b[i] = ""
        list_d[i] = ""
        if len(list_b)>2:
            b = ",".join(map(str,list_b))
            d = ",".join(map(str,list_d))
        else:
            b = "".join(map(str,list_b))
            d = "".join(map(str,list_d))
    #b = format(str(b))
    #d = format(str(d))      
    return [str(a),str(b),str(c),str(d)] 

def compare(a,b):
    return [c for c in a if c.isalpha()] == [c for c in b if c.isalpha()]

@app.get('/format_address')
async def front():
    return {"Details":"This is an address formatter API"}
             
@app.post('/format_address',response_model=Response)
async def format_address(add:FullAddress):
    #Initial formatting of Address
    ebuilding = initialFormat(add.engAddress.addr.building)
    estreet = initialFormat(add.engAddress.addr.street)
    elandmark = initialFormat(add.engAddress.addr.landmark)
    elocality = initialFormat(add.engAddress.addr.locality)
    evtc = initialFormat(add.engAddress.addr.vtc)
    edistrict = initialFormat(add.engAddress.addr.district)
    estate = initialFormat(add.engAddress.addr.state)

    #Initial formatting of Address in local language
    if add.localAddress:
        lbuilding = initialFormat(add.localAddress.addr.building)
        lstreet = initialFormat(add.localAddress.addr.street)
        llandmark = initialFormat(add.localAddress.addr.landmark)
        llocality = initialFormat(add.localAddress.addr.locality)
        lvtc = initialFormat(add.localAddress.addr.vtc)
        ldistrict = initialFormat(add.localAddress.addr.district)
        lstate =initialFormat(add.localAddress.addr.state)

    #Merging repititive text
    edistrict,estreet = merge1(edistrict,estreet)
    edistrict,elocality = merge1(edistrict,elocality)
    edistrict,elandmark = merge1(edistrict,elandmark)
    estreet,elocality = merge1(estreet,elocality)
    edistrict,ebuilding = merge1(edistrict,ebuilding)
    if add.localAddress:
        edistrict,estreet,ldistrict,lstreet = merge2(edistrict,estreet,ldistrict,lstreet)
        edistrict,elocality,ldistrict,llocality = merge2(edistrict,elocality,ldistrict,llocality)
        edistrict,elandmark,ldistrict,llandmark = merge2(edistrict,elandmark,ldistrict,llandmark)
        estreet,elocality,lstreet,llocality = merge2(estreet,elocality,lstreet,llocality)
        edistrict,ebuilding,ldistrict,lbuilding = merge2(edistrict,ebuilding,ldistrict,lbuilding)

    #Merging repititive text between district and vtc
    city = [""," City"," G.P.O","GPO","P.O.","PO","New"]
    for ex in city:
        if edistrict+ex==evtc or ex+edistrict==evtc:
            evtc = None
            if add.localAddress:
                lvtc = None

    #Merging repititive text between district and state
    if estate in edistrict or edistrict in estate:
        edistrict = None
        if add.localAddress:
            ldistrict = None

    #Formatting address
    road = ["Road","Lane","Salai","Gali","Galli","Street","Cross"]
    land = ["Near","Opposite","Opp","Opp.","Behind","Beside","In"]
    build = ["Building","Apt","Apartment","Appartments","Block"]    
    
    #Formatting Building
    ebuilding = ebuilding.replace("#","No.")
    ebuilding_list = ebuilding.split(",")
    for i in range(len(ebuilding_list)):
        ebuilding_set = set(ebuilding_list[i].split(" "))
        if ebuilding_set.intersection(road):
            if estreet==None:
                estreet = ebuilding_list[i]
            else:
                estreet = estreet+","+ebuilding_list[i]
            if add.localAddress:            
                lbuilding_list = lbuilding.split(",")
                if lstreet==None:
                    lstreet = lbuilding_list[i]
                else:
                    lstreet = lstreet+","+lbuilding_list[i]
                lbuilding_list[i] = " "
                lbuilding = ",".join(map(str,lbuilding_list))
            ebuilding_list[i] = " "

        if ebuilding_set.intersection(land):
            if elandmark==None:
                elandmark = ebuilding_list[i]
            else:
                elandmark = elandmark+ebuilding_list[i]
            if add.localAddress:            
                lbuilding_list = lbuilding.split(",")
                if llandmark==None:
                    llandmark = lbuilding_list[i]
                else:
                    llandmark = llandmark+lbuilding_list[i]
                lbuilding_list[i] = " "
                lbuilding = ",".join(map(str,lbuilding_list))         
            ebuilding_list[i] = " "
    ebuilding = ",".join(map(str,ebuilding_list))
    if edistrict in ebuilding and evtc is not None:
        ebuilding = ebuilding.replace(edistrict,"")
        if add.localAddress:
            lbuilding = lbuilding.replace(ldistrict,"")

    #Formatting street
    estreet_list = estreet.split(",")
    for i in range(len(estreet_list)):
        estreet_set = set(estreet_list[i].split(" "))
        if estreet_set.intersection(build):
            if ebuilding==None:
                ebuilding = estreet_list[i]
            else:
                ebuilding = ebuilding+ebuilding_list[i]
            if add.localAddress:            
                lstreet_list = lstreet.split(",")
                if lbuilding==None:
                    lbuilding = lstreet_list[i]
                else:
                    lbuilding = lbuilding+lstreet_list[i]
                lstreet_list[i] = " "
                lstreet = ",".join(map(str,lstreet_list))

        if estreet_set.intersection(land):
            if elandmark==None:
                elandmark = estreet_list[i]
            else:
                elandmark = elandmark+estreet_list[i]
            if add.localAddress:            
                lstreet_list = lstreet.split(",")
                if llandmark==None:
                    llandmark = lstreet_list[i]
                else:
                    llandmark = llandmark+lstreet_list[i]
                lstreet_list[i] = " "
                lstreet = ",".join(map(str,lstreet_list))         

            estreet_list[i] = " "
    estreet= ",".join(map(str,estreet_list))
    if edistrict in estreet and evtc is not None:
        estreet = estreet.replace(edistrict,"")
        if add.localAddress:
            lstreet = lstreet.replace(ldistrict,"")
    
    if edistrict in elandmark and evtc is not None:
        elandmark = elandmark.replace(edistrict,"")
        if add.localAddress:
            llandmark = llandmark.replace(ldistrict,"")
    
    if edistrict in elocality and evtc is not None:
        elocality = elocality.replace(edistrict,"")
        if add.localAddress:
            llocality = llocality.replace(ldistrict,"")
    
    ebuilding = format(ebuilding)
    estreet = format(estreet)
    elandmark = format(elandmark)
    elocality = format(elocality)
    evtc = format(evtc)
    edistrict = format(edistrict)
    estate = format(estate)

    lbuilding = format(lbuilding)
    lstreet = format(lstreet)
    llandmark = format(llandmark)
    llocality = format(llocality)
    lvtc = format(lvtc)
    ldistrict = format(ldistrict)
    lstate = format(lstate)


    
    result = {
            "GivenAddress": add,
            "FormattedAddress":{
                "engAddress":{
                    "lang" : add.engAddress.lang,
                    "addr" : {
                        "building":ebuilding,
                        "street":estreet,
                        "landmark":elandmark,
                        "locality":elocality,
                        "vtc":evtc,
                        "district":edistrict,
                        "state":estate
                    }
                 },
                "localAddress":{
                    
                 }
                }
            }
    if add.localAddress:
        result["FormattedAddress"]["localAddress"]={"lang" : add.localAddress.lang,
                    "addr" : {
                        "building":lbuilding,
                        "street":lstreet,
                        "landmark":llandmark,
                        "locality":llocality,
                        "vtc":lvtc,
                        "district":ldistrict,
                        "state":lstate
                    }}
    return(result)
