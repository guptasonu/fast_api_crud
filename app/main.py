import datetime
import logging
import os

import requests
import uvicorn
from dateutil import parser as dateparser
from dotenv import load_dotenv
from fastapi import (BackgroundTasks, Depends, FastAPI, Request, Response,
                     Security, status)
from fastapi.exceptions import RequestValidationError
from fastapi.middleware.cors import CORSMiddleware
from fastapi.security import HTTPBasic
from fastapi.security.api_key import APIKey, APIKeyHeader
# from fastapi.responses import PlainTextResponse
from sqlalchemy.orm import Session
from starlette.responses import JSONResponse

import models
import schemas
from crud import save_reservation_info
from database import engine, get_db
from utils.email_notify import send_notification
from utils.logs import log_and_time_execution
from utils.random_keys import alpha_numeric_key, reservation_key

# from icecream import ic




load_dotenv()

models.Base.metadata.create_all(bind=engine)


class BookingPalException(Exception):
    def __init__(self, message: str, httpcode: int, errorcode: int):
        self.message = message
        self.httpcode = httpcode
        self.errorcode = errorcode


#API key added TODO: Need to place in db after discussion   
API_KEY = os.getenv("API_KEY", "furraylogic")
API_KEY_NAME = "x-api-key"
api_key_header = APIKeyHeader(name=API_KEY_NAME, auto_error=False)
callback_url = os.getenv("CALLBACK_URL", "https://channelapidemo.mybookingpal.com")
# key = "x-api-key"

app = FastAPI(title="Sojourn-BookingPal API",
    description="Welcome to the Sojourn-BookingPal API auto-docs",
    version="0.9.0"
)


security = HTTPBasic()

async def get_api_key(
    api_key_header: str = Security(api_key_header),
):
    if api_key_header == API_KEY:
        return api_key_header
    else:
        raise BookingPalException(httpcode=401,
                                  errorcode=4010,
                                  message=f"HTTP/1.1 401 Unauthorized. Invalid or missing api token."
                                  )

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
    allow_credentials=True,
)


# Dependency
# def get_db():
#     try:
#         db = SessionLocal()
#         yield db
#     finally:
#         db.close()


@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request, exc):
    
    """Your custom validation exception."""
    
    message = {
        "code": 4001,
        "message": "Validation Error: the message submitted in your request is not in the correct format. Please check and try again."
        }
    logging.exception(f'''{exc.errors()}''')
    logging.exception(f'''{exc.body}''')
    send_notification(msg=exc.body, subject="Sojourn-BookingPal data validation error")
    return JSONResponse(
        status_code= 400,
        content= message
    )


@app.exception_handler(BookingPalException)
async def bookingpal_exception_handler(request, exc):
    message = {
        "code": exc.errorcode,
        "message": exc.message
        }
    logging.error(message)
    return JSONResponse(
            status_code = exc.httpcode,
            content = message
            )


@app.exception_handler(Exception)
async def exception_handler(request, exc):
    """Handle all unspecified exceptions."""

    message = {
        "code": 5000,
        "message": f'''{exc}'''
    }
    logging.error(message)
    send_notification(msg=str(message), subject="Sojourn-BookingPal exception")
    return JSONResponse(
        status_code=500,
        content=message
    )


@app.post("/v2/listings", response_model=schemas.ListingSchema)
@log_and_time_execution
def create_listing(listing: schemas.Listing, db: Session = Depends(get_db), api_key: APIKey = Depends(get_api_key)):
    try:
        payload = listing.dict()
        amenity_data = payload.pop("amenity_categories", [])
        contact_data = payload.pop("contacts", [])
        db_listing = models.ListingSchema(**payload)
        db.add(db_listing)
        db.commit()
        db.refresh(db_listing)
        db_listing.listing_id = db_listing.id
        db.add(db_listing)
        db.commit()
        db.refresh(db_listing)

        if contact_data:
            if type(contact_data) is list:
                for contact in contact_data:
                    contact["listing_id"] = db_listing.id
                    db_contact = models.ListingContacts(**contact)
                    db.add(db_contact)
        if amenity_data:
            if len(amenity_data) > 0:
                for amenity in amenity_data:
                    db_amenity = models.AmenityCategories(listing_id = db_listing.id)
                    db_amenity.code = amenity
                    db.add(db_amenity)
        db.commit()
        response_data = None
        listing_db_response = db.query(models.ListingSchema).get(db_listing.id)
        contact_db_response = db.query(models.ListingContacts).filter(models.ListingContacts.listing_id == listing_db_response.id).all()
        amenity_db_response = db.query(models.AmenityCategories).filter(models.AmenityCategories.listing_id == listing_db_response.id).all()
        
        response_data = {key:value for key,value in listing_db_response.__dict__.items() if(value is not None)}
        if len(contact_db_response) > 0:
            response_data["contacts"] = []
            for contact_res in contact_db_response:
                contact_res = {key:value for key,value in contact_res.__dict__.items() if(value is not None)}
                del contact_res["id"]
                del contact_res["listing_id"]
                response_data["contacts"].append(contact_res)
        if len(amenity_db_response) > 0:
            response_data["amenity_categories"] = []
            for amenity_res in amenity_db_response:
                amenity_res = {key:value for key,value in amenity_res.__dict__.items() if(value is not None)}
                del amenity_res["id"]
                del amenity_res["listing_id"]
                response_data["amenity_categories"].append(amenity_res.get("code"))
        del response_data["id"]
    except Exception as exc:
        raise BookingPalException(httpcode = 500, errorcode = 5000, message = f"Unable to create the new Listing: {exc}")
    
    return response_data


@app.put("/v2/listings/{listing_id}")
@log_and_time_execution
def update_listing(listing_id: int, listing: schemas.Listing, db: Session = Depends(get_db), api_key: APIKey = Depends(get_api_key)):
    # ic(listing)
    try:
        payload = listing.dict()
        listing_exists = db.query(models.ListingSchema).get(listing_id)
        if listing_exists is None:
            raise BookingPalException(httpcode = 404, errorcode = 4040, message = f"Listing ID {listing_id} Not Found!")
        amenity_data = payload.pop("amenity_categories", [])
        contact_data = payload.pop("contacts", [])
        payload["listing_id"] = listing_id

        db.query(models.ListingSchema).filter(models.ListingSchema.listing_id == listing_id).update(payload, synchronize_session = False)
        db.query(models.ListingContacts).filter(models.ListingContacts.listing_id == listing_id).delete()
        db.query(models.AmenityCategories).filter(models.AmenityCategories.listing_id == listing_id).delete()
        if contact_data is not None:
            if type(contact_data) is list:
                for contact in contact_data:
                    contact["listing_id"] = listing_id
                    db_contact = models.ListingContacts(**contact)
                    db.add(db_contact)
        if amenity_data is not None:
            for amenity in amenity_data:
                db_amenity = models.AmenityCategories(listing_id = listing_id)
                db_amenity.code = amenity
                db.add(db_amenity)
        db.commit()
        listing_db_response = db.query(models.ListingSchema).get(listing_exists.id)
        response_dict = schemas.ListingSchema.from_orm(listing_db_response).dict()
        amenities_list = []
        # payload = listing_db_response.dict()
        amenity_data = response_dict.pop("amenity_categories", [])
        for amenity in amenity_data:
            amenities_list.append(amenity.code)
        response_dict["amenity_categories"] = amenities_list
        # response_schema = schemas.ListingSchema.from_orm(response_dict)
        # return response_schema
        return response_dict
    except BookingPalException as exc:
        raise exc
    except Exception as exc:
        raise exc


@app.delete("/v2/listings/{listing_id}")
@log_and_time_execution
def delete_listing(listing_id: int, db: Session = Depends(get_db), api_key: APIKey = Depends(get_api_key)):
    try:
        # listing_exists = db.query(models.ListingSchema).filter(models.ListingSchema.listing_id == listing_id).first()
        # if listing_exists:
        db.query(models.ListingSchema).filter(models.ListingSchema.id == listing_id).delete()
        db.commit()
        data = {
            "listing_id": listing_id
            }
        # else:
        #     data = None
        #     raise BookingPalException(httpcode = 404, errorcode = 4040, message = f"Listing ID {listing_id} Not Found!")
        return data
    except BookingPalException as exc:
        raise exc


@app.get("/records/")
@log_and_time_execution
def get_listing(db: Session = Depends(get_db), api_key: APIKey = Depends(get_api_key)):
    listing = db.query(models.ListingSchema).all()
    listing_contact = db.query(models.ListingContacts).all()
    return {
        listing
    }


def daterange(start_date, end_date):
    for n in range(int((end_date - start_date).days) + 1):
        yield start_date + datetime.timedelta(n)

@app.post("/v2/listing/calendar")
@log_and_time_execution
def get_calendar(calendar:schemas.Calendar, db: Session = Depends(get_db), api_key: APIKey = Depends(get_api_key)):
    try:
        logging.debug(f'get_calendar: {calendar.json()}')
        calendar_payload = calendar.dict()
        listing_id = calendar.listing_id  # calendar_payload.get("listing_id")
        db_listing_id = db.query(models.ListingSchema).filter(models.ListingSchema.listing_id == listing_id).first()
        date_combinations_list = []
        calendar_dates = {}

        if db_listing_id:
            calendar_response = []
            los_response = []
            affected_records = db.query(models.Calendar).filter(models.Calendar.listing_id == listing_id).delete()
            db.commit()
            affected_records = db.query(models.LOSPrice).filter(models.LOSPrice.listing_id == listing_id).delete()
            db.commit()
            # if affected_records > 0:
            #     db.commit()
            if db_listing_id.pricing_model == "per_night" and calendar_payload.get("calendars"):
                for calendar_date in calendar.calendars:
                    db_calendar = models.Calendar(listing_id=listing_id, calendar_date=','.join(calendar_date.dates), nightly_price=calendar_date.nightly_price,
                                                  availability=calendar_date.availability, available_count=calendar_date.available_count,
                                                  min_los=calendar_date.min_los, max_los=calendar_date.max_los, closed_to_arrival=calendar_date.closed_to_arrival,
                                                  closed_to_departure=calendar_date.closed_to_departure)
                    db.add(db_calendar)
                    db.commit()
                    # for each calendar date or date range:
                    calendar_dates[db_calendar.id] = calendar_date.dates
                    for date in calendar_date.dates:
                        # calendar_dates[db_calendar.id] = date
                        date_range = date.split(":")
                        if len(date_range) == 2:
                            start_date = datetime.datetime.strptime(date_range[0], '%Y-%m-%d')
                            end_date = datetime.datetime.strptime(date_range[1], '%Y-%m-%d')
                            date_combinations_list.append(f'{start_date.date()}:{end_date.date()}')
                        else:
                            start_date = datetime.datetime.strptime(date_range[0], '%Y-%m-%d')
                            end_date = datetime.datetime.strptime(date_range[0], '%Y-%m-%d')
                            date_combinations_list.append(start_date.date())

                        for my_date in daterange(start_date, end_date):
                            db_calendar_date = models.CalendarDate(calendar_id=db_calendar.id, calendar_date=my_date)
                            db.add(db_calendar_date)
                    db.commit()
            # Retrieve data from the database for our response
            if db_listing_id.pricing_model == "LOS" and calendar_payload.get("los_price"):
                for los_payload in calendar_payload.get("los_price"):
                    temp_payload = los_payload.get("check_in_date")
                    del los_payload["check_in_date"]
                    los_payload.update(temp_payload)
                    los_payload["listing_id"] = listing_id
                    db_los_price = models.LOSPrice(**los_payload)
                    db.add(db_los_price)
                    db.commit()
            calendar_lists = db.query(models.Calendar).filter(models.Calendar.listing_id == listing_id).all()
            for cal in calendar_lists:
                cal_id = cal.id
                del cal.__dict__["id"]
                cal_res = {key:value for key,value in cal.__dict__.items() if(value is not None)}
                del cal_res["calendar_date"]
                # str_date = str(calendar_dates.get(cal_id))
                cal_res.update({"dates": calendar_dates.get(cal_id)})
                # cal_res["dates"].append(calendar_dates.get(cal_id))
                # for date_combination in date_combinations_list:
                #     cal_res["dates"].append(date_combination)
                calendar_response.append(cal_res)
            los_data = db.query(models.LOSPrice).filter(models.LOSPrice.listing_id == listing_id).all()
            for los in los_data:
                del los.__dict__["id"]
                los_res = {key: value for key, value in los.__dict__.items() if (value is not None)}
                los_res["check_in_date"] = {
                    "date": los_res.get("date"),
                    "los_value": los_res.get("los_value"),
                    "amount": los_res.get("amount")
                }
                del los_res["date"]
                del los_res["los_value"]
                del los_res["amount"]
                los_response.append(los_res)
            response_data = {
                "listing_id" : listing_id,
                "calendars" : calendar_response,
                "los_price" : los_response
            }
            # if los_data:
            #     response_data["los_price"] = []

        else:
            raise BookingPalException(httpcode = 404, errorcode = 4040, message = f"Listing ID {listing_id} Not Found!")

        return response_data
    except BookingPalException as exc:
        db.rollback()
        raise exc
    except Exception as exc:
        db.rollback()
        raise exc


@app.put("/v2/listing_policies/{listing_id}")
@log_and_time_execution
def update_listing_policy(listing_id: int, listing_policy: schemas.Policy, db: Session = Depends(get_db), api_key: APIKey = Depends(get_api_key)):
    try:
        payload = listing_policy.dict()
        response_data = payload
        db_listing_id = db.query(models.ListingSchema).filter(models.ListingSchema.listing_id == listing_id).first()
        if db_listing_id:
            key_collection_payload = payload.pop("keyCollection", None)
            guest_policies_payload = payload.pop("guest_policies", None)
            fees_and_taxes_payload = payload.pop("fees_and_taxes", [])
            #  Always DELETE existing listing policy since Bookingpal will always send the complete policy
            db.query(models.ListingPolicy).filter(models.ListingPolicy.listing_id == db_listing_id.listing_id).delete()
            db_listing_policy = models.ListingPolicy(**payload)
            db_listing_policy.listing_id = db_listing_id.id
            db.add(db_listing_policy)
            db.commit()  # Create new listing policy so that we can use it's unique id for child relationships
            db.refresh(db_listing_policy)
            listing_policy_id = db_listing_policy.id

            if key_collection_payload:
                db_key_collection = models.KeyCollection(listing_policy_id=listing_policy_id)
                db_key_collection.type = key_collection_payload.get("type")
                db_key_collection.check_in_method = key_collection_payload.get("check_in_method")
                db_key_collection.how = key_collection_payload.get("additional_info").get("instruction").get("how")
                db_key_collection.when = key_collection_payload.get("additional_info").get("instruction").get("when")
                db.add(db_key_collection)
            if guest_policies_payload:
                db_guest_policy = models.GuestPolicies(**guest_policies_payload)
                db_guest_policy.listing_policy_id = listing_policy_id
                db.add(db_guest_policy)
            if fees_and_taxes_payload:
                for fee_and_tax_payload in fees_and_taxes_payload:
                    db_fee_tax = models.FeesandTaxes(**fee_and_tax_payload)
                    db_fee_tax.listing_policy_id = listing_policy_id
                    db.add(db_fee_tax)
            db.commit()  # Only commit db changes after creating all listing policy child objects
            if key_collection_payload is not None:
                response_data["keyCollection"] = key_collection_payload
            if guest_policies_payload is not None:
                response_data["guest_policies"] = guest_policies_payload
            if fees_and_taxes_payload is not None:
                response_data["fees_and_taxes"] = []
                for fee_res in fees_and_taxes_payload:
                    fee_res = {key:value for key,value in fee_res.items() if(value is not None)}
                    response_data["fees_and_taxes"].append(fee_res)
            response_data = {key:value for key,value in response_data.items() if(value is not None)}
        else:
            raise BookingPalException(httpcode = 404, errorcode = 4040, message = f"Listing ID {listing_id} Not Found!")
        return response_data
    except BookingPalException as exc:
        raise exc
    except Exception as exc:
        raise exc


@app.post("/v2/listing_rooms")
@log_and_time_execution
def create_or_update_rooms(rooms:schemas.Rooms, db: Session = Depends(get_db), api_key: APIKey = Depends(get_api_key)):
    try:
        payload = rooms.dict()
        db_listing_id = db.query(models.ListingSchema).filter(models.ListingSchema.listing_id == payload.get("listing_id")).first()
        if db_listing_id:
            # Always DELETE existing rooms and associated beds since Bookingpal will always send the complete room info.
            db.query(models.Rooms).filter(models.Rooms.listing_id == db_listing_id.id).delete()
            for room in payload.get("rooms"):
                db_room = models.Rooms(listing_id=db_listing_id.id)
                db_room.room_type = room.get("room_type")
                db_room.bath_count = room.get("bath_count")
                db.add(db_room)
                db.commit()
                db.refresh(db_room)
                if room.get("beds"):
                    for bed in room.get("beds"):
                        db_beds = models.Beds(room_id=db_room.id)
                        db_beds.bed_count = bed.get("bed_count")
                        db_beds.bed_type = bed.get("bed_type")
                        db.add(db_beds)
                    db.commit()
                    # db.refresh(db_beds)
        else:
            raise BookingPalException(httpcode = 404, errorcode = 4040, message = f"Listing ID {payload.get('listing_id')} Not Found!")
        response_dict = {
            "listing_id":payload.get("listing_id"),
            "rooms":[]
        }
        for response in payload.get("rooms"):
            return_res = {key:value for key,value in response.items() if(value is not None)}
            response_dict["rooms"].append(return_res)
        return response_dict
    except BookingPalException as exc:
        raise exc
    except Exception as exc:
        raise exc


@app.post("/v2/listing_photos")
@log_and_time_execution
def create_listing_photos(photo:schemas.Photos, db: Session = Depends(get_db), api_key: APIKey = Depends(get_api_key)):
    try:
        payload = photo.dict()
        db_listing_id = db.query(models.ListingSchema).filter(models.ListingSchema.listing_id == payload.get("listing_id")).first()
        tag_list = None
        photo_id = None
        if db_listing_id:
            # del payload["listing_id"]
            if payload.get("tags"):
                tag_list = payload.get("tags")
            del payload["tags"]
            db_photo = models.Photos(**payload)
            # db_photo.listing_id = db_listing_id.id
            db.add(db_photo)
            db.commit()
            db.refresh(db_photo)
            photo_id = db_photo.id
            if tag_list is not None:
                for tag in tag_list:
                    db_tag = models.ImageTag(photos_id=db_photo.id)
                    db_tag.name = tag
                    # db_tag.description = tag.name
                    db.add(db_tag)
                    db.commit()
                    db.refresh(db_tag)

            # photo = None
            photo = db.query(models.Photos).filter(models.Photos.id == photo_id).first()
            # for photo in photo_list:
            if photo:
                image_tag_list = db.query(models.ImageTag).filter(models.ImageTag.photos_id == photo_id).all()
                image_tag_res_data = []
                for image in image_tag_list:
                    # del image.__dict__["id"]
                    # del image.__dict__["photos_id"]
                    image_tag_res_data.append(image.name)
                photo.__dict__["tags"] = image_tag_res_data
                photo.__dict__["photo_id"] = photo.__dict__["id"]
                del photo.__dict__["id"]
                return photo
            else:
                raise BookingPalException(httpcode=421, errorcode=4210,
                                          message="Operation failed. Unable to create the new image")
        else:
            raise BookingPalException(httpcode = 404, errorcode = 4040, message = f"Listing ID {payload.get('listing_id')} Not Found!")
    except BookingPalException as exc:
        raise exc
    except Exception as exc:
        raise exc



@app.delete("/v2/listing_photos/{photo_id}")
@log_and_time_execution
def delete_photos(photo_id: int, db: Session = Depends(get_db), api_key: APIKey = Depends(get_api_key)):
    try:
        listing_id = None
        photo_exists = db.query(models.Photos).filter(models.Photos.id == photo_id).first()
        if photo_exists:
            listing_id = photo_exists.listing_id
        # db.query(models.ImageTag).filter(models.ImageTag.photos_id == photo_id).delete()
        db.query(models.Photos).filter(models.Photos.id == photo_id).delete()
        db.commit()
        return {
            "photo_id": photo_id,
            "listing_id": listing_id
        }
    except Exception as exc:
        raise exc


@app.post("/v2/listing_status/{listing_id}")
@log_and_time_execution
def update_listing_status(listing_id: int, listing_status:schemas.ListingStatus, db: Session = Depends(get_db), api_key: APIKey = Depends(get_api_key)):
    try:
        payload = listing_status.dict()
        db_listing_id = db.query(models.ListingSchema).filter(models.ListingSchema.listing_id == listing_id).first()
        if db_listing_id:
            is_exist_status = db.query(models.ListingStatus).filter(models.ListingStatus.listing_id == db_listing_id.listing_id).first()
            if is_exist_status:
                db.query(models.ListingStatus).filter(models.ListingStatus.listing_id == db_listing_id.listing_id).update(payload, synchronize_session = False)
                db.commit()
            else:
                db_listing_status = models.ListingStatus(**payload)
                db_listing_status.listing_id = db_listing_id.id
                db.add(db_listing_status)
                db.commit()
                db.refresh(db_listing_status)
        else:
            raise BookingPalException(httpcode = 404, errorcode = 4040, message = f"Listing ID {listing_id} Not Found!")
        return {
            "listing_id": listing_id
        }
    except BookingPalException as exc:
        raise exc
    except Exception as exc:
        raise exc


@app.post("/v2/listing_price_rule")
@log_and_time_execution
def create_listing_price_rule(listing_price:schemas.ListingPrice, db: Session = Depends(get_db), api_key: APIKey = Depends(get_api_key)):
    try:
        listing_exists = db.query(models.ListingSchema).filter(models.ListingSchema.listing_id == listing_price.listing_id).first()
        if listing_exists:
            db_listing_price = models.ListingPrice()
            payload = listing_price.dict()
            if listing_price.pricing_rule:
                db_listing_price = models.ListingPrice(**payload.get("pricing_rule"))
            db_listing_price.listing_id = listing_price.listing_id
            db.add(db_listing_price)
            db.commit()
            db.refresh(db_listing_price)
            return {
                "price_rule_id": str(db_listing_price.id)
            }
        else:
            raise BookingPalException(httpcode = 404, errorcode = 4040, message = f"Listing ID {listing_price.listing_id} Not Found!")
    except BookingPalException as exc:
        raise exc
    except Exception as exc:
        raise exc


@app.delete("/v2/listing_price_rule/{price_rule_id}", status_code=status.HTTP_204_NO_CONTENT)
@log_and_time_execution
def delete_listing_price_rule(price_rule_id: int, db: Session = Depends(get_db), api_key: APIKey = Depends(get_api_key)):
    try:
        db.query(models.ListingPrice).filter(models.ListingPrice.id == price_rule_id).delete()
        db.commit()
        # pass
        return Response(status_code=status.HTTP_204_NO_CONTENT)
    except Exception as exc:
        raise exc

# Reservation Management

@app.get("/v2/check_availability")
@log_and_time_execution
def check_availability(start_date: str = datetime.date.today() , nights : int = 0, listing_id : int = 0 , db: Session = Depends(get_db), api_key: APIKey = Depends(get_api_key)):
    try:
        header = {
            "x-api-key":api_key,
            "Accept":"application/json"
        }
        r = requests.get(
            url = f"{callback_url}/v2/check_availability",
            params={
                "start_date":start_date,
                "nights":nights,
                "listing_id":listing_id
                },
            headers=header,
            )
        json_response = r.json()
        if r.status_code == 200:
            return json_response
        elif r.status_code == 403:
            raise BookingPalException(httpcode=403, errorcode = 4030, message="Unauthorized: Unable to access system with current credentials.")
        elif r.status_code == 400:
            errorcode = json_response.get("code", 4003)
            message = json_response.get("message", f"Unable to check availability for this listing: {listing_id}")
            raise BookingPalException(httpcode=400, errorcode=errorcode, message=message)
        else:
            raise BookingPalException(httpcode=r.status_code, errorcode=r.status_code * 1000,
                                      message=f"Operation failed due to unexpected error from upstream system.")

    except Exception as exc:
        raise exc


@app.get("/v2/quote")
@log_and_time_execution
def get_quote(listing_id: int, nights: int, number_of_guests: int, start_date: datetime.date, api_key: APIKey = Depends(get_api_key)):
    header = {
        "x-api-key":API_KEY,
        "Accept":"application/json"
    }
    try:
        r = requests.get(
            url = f"{callback_url}/v2/quote",
            params={
                "start_date":start_date.strftime('%Y-%m-%d'),
                "nights":nights,
                "listing_id":listing_id,
                "number_of_guests":number_of_guests
                },
            headers=header,
            )
        if r.status_code == 200:
            # print(r.json())
            # response = schemas.QuoteResponse.parse_raw(r.text)
            return r.json()
        elif r.status_code == 403:
            raise BookingPalException(httpcode=403, errorcode=4030,
                                      message="Unathorized: Unable to access quote system with current credentials.")
        else:
            raise BookingPalException(httpcode=r.status_code, errorcode=r.status_code * 10,
                                      message=f"Quote operation failed. The dates requested may be unavailable, "
                                              f"or you might have an error in your request")
    except requests.exceptions.RequestException as e:
        raise BookingPalException(httpcode=r.status_code, errorcode=r.status_code*10,
                                  message=f"Error: {e}")


@app.get("/v2/quote-preview")
@log_and_time_execution
def quote_preview(nights: int, reservation_id: int, number_of_guests: int = 2, start_date: str = datetime.date.today(), api_key: APIKey = Depends(get_api_key)):
    header = {
        "x-api-key":api_key,
        "Accept":"application/json"
    }
    try:
        r = requests.get(
            url = f"{callback_url}/v2/quote-preview",
            params={
                "start_date":start_date,
                "nights":nights,
                "reservation_id":reservation_id,
                "number_of_guests":number_of_guests
                },
            headers=header,
            )
        if r.status_code == 200:
            # print(r.json())
            # response = schemas.QuoteResponse.parse_raw(r.text)
            return r.json()
        elif r.status_code == 403:
            return BookingPalException(httpcode=403, errorcode=4030,
                                      message="Unathorized: Unable to access quote system with current credentials.")
        elif r.status_code == 400:
            return r.json()["errors"][0]
        else:
            raise BookingPalException(httpcode=r.status_code, errorcode=r.status_code * 10,
                                      message=f"Operation failed due to unexpected error from upstream system.")

    except requests.exceptions.RequestException as e:
        raise BookingPalException(httpcode=r.status_code, errorcode=r.status_code*10,
                                  message=f"Error: {e}")


# Endpoint for testing save reservation to database only
# @app.post("/v2/save-reservation")
# def save_reservation(reservation_request:schemas.ReservationRequest, db: Session = Depends(get_db), api_key: APIKey = Depends(get_api_key)):
#     try:
#         save_reservation_info(reservation_request, db)
#
#     except BookingPalException as exc:
#         raise exc


def get_quote_for_reservation(listing_id: int, nights: int, number_of_guests: int, start_date: datetime.date):
    quote_response = get_quote(listing_id=listing_id, nights=nights, number_of_guests=number_of_guests, start_date=start_date)
    if "quote" in quote_response:
        # response = schemas.QuoteResponse.parse_raw(quote_response.text)
        quote = schemas.QuoteResponse(**quote_response)
        return quote
    else:
        raise BookingPalException(message="Unable to validate the quote prior to booking the reservation.",
                                  httpcode="404", errorcode=4040)


@app.post("/reservation")
def build_reservation(listing_id: int, start_date: datetime.date, end_date: datetime.date, guest_email: str,
                      guest_first_name: str, guest_last_name: str, number_of_guests: int, req: Request,
                      background_tasks: BackgroundTasks, db: Session = Depends(get_db),
                      api_key: APIKey = Depends(get_api_key)):
    listing_exists = db.query(models.ListingSchema).filter(models.ListingSchema.listing_id == listing_id).first()
    if listing_exists:
        reservation_request = schemas.ReservationRequest(listing_id= listing_id)
        reservation = schemas.Reservation(start_date= start_date.isoformat(), end_date=end_date.isoformat(),
                                          guest_email= guest_email, guest_first_name= guest_first_name, guest_last_name= guest_last_name,
                                          listing_id= listing_id, status=schemas.Status.Book, confirmation_code="",
                                          cancellation_policy_category="moderate", nightly_base_price=0, nights=0,
                                          number_of_guests=number_of_guests, tax_amount="0", session_id=alpha_numeric_key(),
                                          ip_address="0.0.0.0", total=0)
        if listing_exists.listing_policy:
            reservation.cancellation_policy_category = listing_exists.listing_policy.cancellation_policy_category
        reservation.nights = (end_date - start_date).days
        reservation.ip_address = req.client.host
        reservation.session_id = alpha_numeric_key()
        reservation.confirmation_code = reservation_key()
        quote = get_quote_for_reservation(
            listing_id=listing_id,
            nights=reservation.nights,
            number_of_guests=reservation.number_of_guests,
            start_date=reservation.start_date
        )
        reservation.total = quote.total
        reservation_request.reservation = reservation
        return create_reservation(reservation_request=reservation_request, req=req, background_tasks=background_tasks,
                                  api_key=api_key)
        # return reservation_request
    else:
        raise BookingPalException(httpcode=404, errorcode=4040, message=f"Listing ID {listing_id} Not Found!")


@app.post("/v2/reservation")
@log_and_time_execution
def create_reservation(reservation_request:schemas.ReservationRequest, req: Request, background_tasks: BackgroundTasks,
                       db: Session = Depends(get_db), api_key: APIKey = Depends(get_api_key)):
        confirmation_code = reservation_key()
        reservation_request.reservation.ip_address = req.client.host
        reservation_request.reservation.confirmation_code = confirmation_code
        quote = get_quote_for_reservation(
            listing_id=reservation_request.listing_id,
            nights=reservation_request.reservation.nights,
            number_of_guests=reservation_request.reservation.number_of_guests,
            start_date=reservation_request.reservation.start_date
        )
        reservation_request.reservation.fees = quote.quote
        reservation_request.reservation.nightly_base_price = quote.original_total
        # reservation_request.reservation.cancellation_policy_category = listing_exists.listing_policy.cancellation_policy_category
        # Verify that the price submitted with the reservation matches the current quote (else reservation will fail)
        if not float(reservation_request.reservation.total) == quote.total:
            raise BookingPalException(httpcode=503, errorcode=5030,
                message=f"Current quoted price differs from the {reservation_request.reservation.total} price submitted with this reservation request.")
        # reservation_request.reservation.total = quote.total
        # for fee in reservation_request.reservation.fees:
        #     if fee.type == "NIGHTLY_RATE":
        #         reservation_request.reservation.nightly_base_price = fee.amount
        header = {
            "x-api-key": api_key,
            "Accept": "application/json"
        }
        try:
            r = requests.post(
                url = f"{callback_url}/v2/reservation",
                params={
                    "confirmation_code":confirmation_code
                    },
                data= reservation_request.json(),
                headers=header
                )
            if r.status_code == 200:
                reservation_number = r.json().get("reservation_id")
                # save_reservation_info(reservation_request=reservation_request, confirmation_code=confirmation_code,
                #                       partner_confirmation_number=reservation_number)
                background_tasks.add_task(save_reservation_info, reservation_request, confirmation_code, reservation_number)
                return r.json()
            elif r.status_code == 403:
                raise BookingPalException(httpcode=403, errorcode=4030,
                                          message="Unathorized: Unable to access reservations system with current credentials.")
            elif r.status_code == 400:
                return r.json()["errors"][0]
            else:
                raise BookingPalException(httpcode=r.status_code, errorcode=r.status_code * 1000,
                                          message=f"Operation failed due to unexpected error from upstream system.")

        except requests.exceptions.RequestException as e:
            raise BookingPalException(httpcode=500, errorcode=5000,
                                      message=f"Error: {e}")


@app.put("/v2/reservation-modification")
@log_and_time_execution
def update_reservation(reservation_change_request:schemas.UpdateReservation, db: Session = Depends(get_db), api_key: APIKey = Depends(get_api_key)):
    header = {
        "x-api-key":api_key,
        "Accept":"application/json"
    }
    try:
        r = requests.put(
            url=f"{callback_url}/v2/reservation-modification",
            data= reservation_change_request.json(),
            headers=header
            )
        if r.status_code == 200:
            return r.json()
        elif r.status_code == 403:
            raise BookingPalException(httpcode=403, errorcode=4030,
                                      message="Unathorized: Unable to access reservations system with current credentials.")
        elif r.status_code == 400:
            return r.json()["errors"][0]
        else:
            raise BookingPalException(httpcode=r.status_code, errorcode=r.status_code * 1000,
                                      message=f"Operation failed due to unexpected error from upstream system.")

    except requests.exceptions.RequestException as e:
        raise BookingPalException(httpcode=r.status_code, errorcode=r.status_code*1000,
                                  message=f"Error: {e}")
    #
    # r = requests.put(
    #     url = f"{callback_url}/v2/reservation-modification",
    #     headers=header,
    #     )
    # if r.status_code == 200:
    #     msg = "Update Reservation Succesfully"
    # elif r.status_code == 403:
    #     msg = "Authentication Failed"
    #     raise HTTPException(status_code=403, detail=msg)
    # else:
    #     msg = "Getting some error while Update Reservation"
    # return {"msg": msg}


@app.delete("/v2/reservation")
@log_and_time_execution
def cancel_reservation(confirmation_code: str, background_tasks: BackgroundTasks,
                       db: Session = Depends(get_db), api_key: APIKey = Depends(get_api_key)):
    header = {
        "x-api-key":api_key,
        "Accept":"application/json"
    }
    try:
        r = requests.delete(
            url = f"{callback_url}/v2/reservation",
            params={
                "confirmation_code":confirmation_code
            },
            headers=header
            )
        if r.status_code == 200:
            background_tasks.add_task(sync_reservation, confirmation_code)
            # is_exist_listing = db.query(models.Reservation).filter(models.Reservation.confirmation_code == confirmation_code).first()
            # if is_exist_listing:
            #     is_exist_listing.updated = datetime.now()
            #     is_exist_listing.status = "Cancelled"
            return None # Return void upon successful operation (as per BookingPal spec)
        elif r.status_code == 403:
            return BookingPalException(httpcode=403, errorcode=4030,
                                      message="Unathorized: Unable to access reservations system with current credentials.")
        elif r.status_code == 400:
            return r.json()["errors"][0]
        else:
            raise BookingPalException(httpcode=r.status_code, errorcode=r.status_code * 1000,
                                      message=f"Operation failed due to unexpected error from upstream system.")
    except requests.exceptions.RequestException as e:
        raise BookingPalException(httpcode=r.status_code, errorcode=r.status_code*1000,
                                  message=f"Error: {e}")


@app.get("/v2/reservationdetails")
@log_and_time_execution
def reservationdetails(confirmation_id : str = "", api_key: APIKey = Depends(get_api_key)):
    header = {
        "x-api-key":API_KEY,
        "Accept":"application/json"
    }
    try:
        r = requests.get(
            url = f"{callback_url}/v2/reservationdetails",
            params={
                "confirmation_id":confirmation_id
            },
            headers=header,
            )
        if r.status_code == 200:
            return r.json()
        elif r.status_code == 403:
            raise BookingPalException(httpcode=403, errorcode=4030,
                                      message="Unathorized: Unable to access reservations system with current credentials.")
        elif r.status_code == 400:
            raise BookingPalException(httpcode=400, errorcode=4000,
                                      message="Bad Request: Unable to process the request due to client error "
                                              "(e.g., invalid confirmation code, malformed message format, etc.)")
        else:
            raise BookingPalException(httpcode=r.status_code, errorcode=9999,
                                      message=r.text)
    except requests.exceptions.RequestException as e:
        raise BookingPalException(httpcode=r.status_code, errorcode=r.status_code*1000,
                                  message=f"Error: {e}")


@app.post("/v2/discountdetails")
@log_and_time_execution
def create_discount(create_discount:schemas.CreateDiscount, db: Session = Depends(get_db), api_key: APIKey = Depends(get_api_key)):
    try:
        payload = create_discount.dict()
        discount_code = payload.get("discount_code")
        discount_code_exists = db.query(models.Discount).filter(models.Discount.discount_code == discount_code).first()
        if discount_code_exists:
            raise BookingPalException(httpcode = 400, errorcode = 4000, message = f"Discount code {discount_code} already exists.")
        discount_rules_payload = payload.pop("discount_rules", [])
        adr_options_payload = payload.pop("adr_options", [])
        db_discount = models.Discount(**payload)
        db.add(db_discount)
        db.commit()
        db.refresh(db_discount)
        # if discount_rules_payload:
        for discount_rule in discount_rules_payload:
            for rule_value in discount_rule.get("rule_value"):
                db_discount_rule = models.DiscountRules(discount_id=db_discount.id)
                db_discount_rule.rule_name = discount_rule.get("rule_name")
                db_discount_rule.rule_value = rule_value
                db.add(db_discount_rule)
        if adr_options_payload:
            for adr_option in adr_options_payload:
                adr_option = {key: value for key, value in adr_option.items() if (value is not None)}
                if adr_option:
                    db_adr_option = models.DiscountAdr(**adr_option)
                    db_adr_option.discount_id = db_discount.id
                    db.add(db_adr_option)
        db.commit()
        return {
            "discount_id": str(db_discount.id),
            "discount_code": payload.get("discount_code")
        }
    except Exception as exc:
        raise exc


@app.put("/v2/discountdetails/{discount_code}")
@log_and_time_execution
def update_discount(update_discount:schemas.CreateDiscount, discount_code: str, db: Session = Depends(get_db), api_key: APIKey = Depends(get_api_key)):
    try:
        payload = update_discount.dict()
        discount_exists = db.query(models.Discount).filter(models.Discount.discount_code == discount_code).first()

        if discount_exists:
            discount_rules_payload = payload.pop("discount_rules", [])
            adr_options_payload = payload.pop("adr_options", [])
            if discount_code != update_discount.discount_code:  # Check if discount code in payload body already exists
                new_discount_exists = db.query(models.Discount).filter(models.Discount.discount_code == update_discount.discount_code).first()
                if new_discount_exists:
                    raise BookingPalException(httpcode = 400, errorcode = 4000, message = f"Discount code {update_discount.discount_code} already exists.")
            db.query(models.DiscountRules).filter(models.DiscountRules.discount_id == discount_exists.id).delete()
            for discount_rule in discount_rules_payload:
                for rule_value in discount_rule.get("rule_value"):
                    db_discount_rule = models.DiscountRules(discount_id=discount_exists.id)
                    db_discount_rule.rule_name = discount_rule.get("rule_name")
                    db_discount_rule.rule_value = rule_value
                    db.add(db_discount_rule)
            db.query(models.DiscountAdr).filter(models.DiscountAdr.discount_id == discount_exists.id).delete()
            if adr_options_payload:
                for adr_option in adr_options_payload:
                    db_adr_option = models.DiscountAdr(**adr_option)
                    db_adr_option.discount_id = discount_exists.id
                    db.add(db_adr_option)
            db.query(models.Discount).filter(models.Discount.discount_code == discount_code).update(payload, synchronize_session=False)
            db.commit()
            db.refresh(discount_exists)
        else:
            raise BookingPalException(httpcode = 404, errorcode = 4040, message = f"Discount Code {discount_code} Not Found!")
        return {
            "discount_id": str(discount_exists.id),
            "discount_code": str(discount_exists.discount_code)
        }
    except Exception as exc:
        raise exc


@app.delete("/v2/discountdetails/{discount_code}", status_code=status.HTTP_204_NO_CONTENT, responses={204: {"model": None}})
@log_and_time_execution
def delete_discount(discount_code : str = "", db: Session = Depends(get_db), api_key: APIKey = Depends(get_api_key)):
    try:
        db.query(models.Discount).filter(models.Discount.discount_code == discount_code).delete()
        db.commit()
        return Response(status_code=status.HTTP_204_NO_CONTENT)
    except Exception as exc:
        raise exc


def sync_reservation(confirmation_id : str):
    """Update the reservation record in our database according to latest reservation details from BookingPal"""
    reservation = reservationdetails(confirmation_id=confirmation_id)
    logging.debug(reservation)
    # TBD - code to update the reservation record in our database


if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8000)
