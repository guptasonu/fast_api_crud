from dateutil import parser as dateparser
from fastapi import Depends

import schemas, models
from database import SessionLocal, get_db
from sqlalchemy.orm import Session

# Dependency
from utils.logs import log_and_time_execution


def get_db():
    try:
        db = SessionLocal()
        yield db
    finally:
        db.close()


@log_and_time_execution
def save_reservation_info(reservation_request:schemas.ReservationRequest, confirmation_code: str,
                          partner_confirmation_number: int):
    success = False
    db = SessionLocal()
    # confirmation_code = reservation_key()
    is_exist_listing = db.query(models.ListingSchema).filter(models.ListingSchema.listing_id == reservation_request.listing_id)
    # if is_exist_listing:
    payload = reservation_request.dict().get("reservation")
    if is_exist_listing:
        fee_payload = payload.pop("fees", [])
        # del payload["fees"]
        credit_card_payload = payload.pop("credit_card")
        # del payload["credit_card"]
        reward_payload = payload.pop("rewards")
        # del payload["rewards"]
        phone_payload = payload.pop("guest_phone_numbers", [])
        # del payload["guest_phone_numbers"]
        trip_payload = payload.get("trip_purpose")
        del payload["trip_purpose"]
        if payload.get("commission"):
            payload["commission_amount"] = payload.get("commission").get("commission_amount")
            payload["currency"] = payload.get("commission").get("currency")
        del payload["commission"]

        payload["partner_confirmation_code"] = partner_confirmation_number
        payload["confirmation_code"] = confirmation_code
        payload["partner_listing_id"] = reservation_request.listing_id
        payload["created_at"] = dateparser.parse(payload["created_at"])
        payload["updated_at"] = dateparser.parse(payload["updated_at"])
        payload["booked_at"] = dateparser.parse(payload["booked_at"])

        db_reservation = models.Reservation(**payload)
        db_reservation.listing_id = reservation_request.listing_id
        db.add(db_reservation)
        db.commit()
        db.refresh(db_reservation)

        if fee_payload:
            for fee in fee_payload:
                db_fee = models.ReservationFees(**fee)
                db_fee.reservation_id = db_reservation.id
                db.add(db_fee)
                # db.commit()
                # db.refresh(db_fee)

        if credit_card_payload:
            card_type = credit_card_payload.get("card_type")
            del credit_card_payload["card_type"]
            db_credit_card = models.CreditCard(**credit_card_payload)
            db_credit_card.reservation_id = db_reservation.id
            # NEED TO decide whether we store id of cc type or the string (name)
            # db_credit_card.card_type = card_type.name
            db.add(db_credit_card)
            # db.commit()
            # db.refresh(db_credit_card)

        if reward_payload:
            db_reward = models.Rewards(**reward_payload)
            db_reward.reservation_id = db_reservation.id
            db.add(db_reward)
            # db.commit()
            # db.refresh(db_reward)
        if phone_payload is not None:
            for phone in phone_payload:
                db_reservation_phone = models.ReservationPhone(reservation_id=db_reservation.id)
                db_reservation_phone.guest_phone_numbers = phone
                db.add(db_reservation_phone)
                # db.commit()
                # db.refresh(db_reservation_phone)
        if trip_payload is not None:
            for trip in trip_payload:
                db_reservation_trip = models.ReservationTrip(reservation_id=db_reservation.id)
                db_reservation_trip.trip_purpose = trip
                db.add(db_reservation_trip)
                # db.commit()
                # db.refresh(db_reservation_trip)
        db.commit()
        success = True
    return success
