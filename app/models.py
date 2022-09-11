from datetime import date, datetime
from sqlalchemy import Column, Integer, String, ForeignKey, Boolean, Text
from sqlalchemy.orm import relationship
from sqlalchemy.sql.expression import null
from sqlalchemy.sql.sqltypes import Date, Float, DateTime
from database import Base


class Listing(Base):
    __tablename__ = "listing"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    # listing_id = Column(Integer, index=True)
    name = Column(String(100), index=True, nullable=True)
    listing_type_group = Column(String(100), index=True, nullable=True)
    listing_type_category = Column(String(100), index=True, nullable=True)
    bedrooms = Column(Integer, index=True, nullable=True)
    bathrooms = Column(Float, index=True, nullable=True)
    beds = Column(Integer, index=True, nullable=True)
    check_in_option = Column(String(100), index=True, nullable=True)
    permit_or_tax_id = Column(String(100), index=True, nullable=True)
    apt = Column(String(100), index=True, nullable=True)
    street = Column(String(100), index=True, nullable=True)
    city = Column(String(100), index=True, nullable=True)
    state = Column(String(100), index=True, nullable=True)
    zipcode = Column(String(100), index=True, nullable=True)
    country_code = Column(String(5), index=True, nullable=True)
    lat = Column(Float, index=True, nullable=True)
    lng = Column(Float, index=True, nullable=True)
    person_capacity = Column(Integer, index=True, nullable=True)
    listing_currency = Column(String(5), index=True, nullable=True)
    short_description = Column(Text, nullable=True)
    detailed_description = Column(Text, nullable=True)
    neighborhood_overview = Column(String(100), index=True, nullable=True)
    transit = Column(String(100), index=True, nullable=True)
    house_rules = Column(String(100), index=True, nullable=True)
    locale = Column(String(100), index=True, nullable=True)
    guests_included = Column(Integer, index=True, nullable=True)
    booking_settings = Column(String(100), index=True, nullable=True)
    flags = Column(String(100), index=True, nullable=True)
    primary_contact = Column(String(100), index=True, nullable=True)
    min_advance_booking_offset = Column(String(100), index=True, nullable=True)
    max_advance_booking_offset = Column(String(100), index=True, nullable=True)
    pm_name = Column(String(100), index=True, nullable=True)
    pm_id = Column(String(100), index=True, nullable=True)
    pricing_model = Column(String(100), index=True, nullable=True)

    contacts = relationship("ListingContacts", back_populates="listing")
    calendars = relationship("Calendar", back_populates="listing")
    los_prices = relationship("LOSPrice", back_populates="listing")
    listing_policy = relationship("ListingPolicy", back_populates="listing", uselist=False)
    rooms = relationship("Rooms", back_populates="listing")
    photos = relationship("Photos", back_populates="listing")
    listing_status = relationship("ListingStatus", back_populates="listing")
    listing_price = relationship("ListingPrice", back_populates="listing")
    reservation = relationship("Reservation", back_populates="listing")
    amenity_categories = relationship("AmenityCategories", back_populates="listing")


class ListingSchema(Listing):
    listing_id = Column(Integer, index=True)


class ListingContacts(Base):
    __tablename__ = "listing_contacts"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    listing_id = Column(Integer, ForeignKey('listing.id'))
    email_address = Column(String(100), index=True, nullable=True)
    name = Column(String(100), index=True, nullable=True)
    phone = Column(String(100), index=True, nullable=True)
    type = Column(String(100), index=True, nullable=True)

    listing = relationship("Listing", back_populates="contacts")


class Calendar (Base):
    __tablename__ = "calendar"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    listing_id = Column(Integer, ForeignKey('listing.id'))
    calendar_date = Column(String, index=True, nullable=True)
    nightly_price = Column(Float, nullable=True)
    availability = Column(Boolean, nullable=True)
    available_count = Column(Integer, nullable=True)
    min_los = Column(Integer, nullable=True)
    max_los = Column(Integer, nullable=True)
    closed_to_arrival = Column(Boolean, nullable=True)
    closed_to_departure = Column(Boolean, nullable=True)

    calendar_dates = relationship("CalendarDate")
    listing = relationship("Listing", back_populates="calendars")


class CalendarDate(Base):
    __tablename__ = "calendar_dates"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    calendar_id = Column(Integer, ForeignKey('calendar.id'))
    calendar_date = Column(Date, index=True, nullable=True)

    calendar = relationship("Calendar", back_populates="calendar_dates")
    # los_price = relationship("LOSPrice", back_populates="calendar")
    

class LOSPrice(Base):
    __tablename__ = "los_price"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    # calendar_id = Column(Integer, ForeignKey('calendar.id'))
    listing_id = Column(Integer, ForeignKey('listing.id'))
    max_guests = Column(Integer, nullable=True)
    currency = Column(String(5), index=True, nullable=True)
    date = Column(Date, nullable=True)
    los_value = Column(Integer, nullable=True)
    amount = Column(Float, nullable=True)

    listing = relationship("Listing", back_populates="los_prices")
    # calendar = relationship("Calendar", back_populates="los_price")


class KeyCollection(Base):
    __tablename__ = "key_collection"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    listing_policy_id = Column(Integer, ForeignKey('listing_policy.id'))
    type =  Column(String(100), index=True, nullable=True)
    check_in_method = Column(String(100), index=True, nullable=True)
    how =  Column(String(100), index=True, nullable=True)
    when =  Column(String(100), index=True, nullable=True)

    listing_policy = relationship("ListingPolicy", back_populates="key_collection")

class GuestPolicies(Base):
    __tablename__ = "guest_policies"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    listing_policy_id = Column(Integer, ForeignKey('listing_policy.id'))
    smoking_allowed = Column(Integer, nullable=True)
    parties_allowed = Column(Integer, nullable=True)
    parking_allowed = Column(String(20), index=True, nullable=True)
    parking_price_type = Column(String(20), index=True, nullable=True)
    pets_allowed = Column(String(20), index=True, nullable=True)
    pets_price_type = Column(String(20), index=True, nullable=True)
    quiet_hours_set = Column(Integer , nullable=True)
    quiet_hours_start_time = Column(String(100), index=True, nullable=True)
    quiet_hours_end_time = Column(String(100), index=True, nullable=True)

    listing_policy = relationship("ListingPolicy", back_populates="guest_policies")

class FeesandTaxes(Base):
    __tablename__ = "fees_and_taxes"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    listing_policy_id = Column(Integer, ForeignKey('listing_policy.id'))
    amount = Column(Float, nullable=True)
    fee_tax_id = Column(String(100), index=True, nullable=True)
    description = Column(Text, nullable=True)
    type = Column(String(100), index=True, nullable=True)
    charge_frequency = Column(Integer, nullable=True)
    charge_type = Column(Integer, nullable=True)
    percentage = Column(Float, nullable=True)
    charged_at = Column(String(100), index=True, nullable=True)
    room_id = Column(String(100), index=True, nullable=True)
    min_guests = Column(Integer, nullable=True)
    max_guests = Column(Integer, nullable=True)

    listing_policy = relationship("ListingPolicy", back_populates="fees_and_taxes")


class ListingPolicy(Base):
    __tablename__ = "listing_policy"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    listing_id = Column(Integer, ForeignKey('listing.id'))
    cancellation_policy_category =  Column(String(100), index=True, nullable=True)
    check_in_start_time =  Column(String(100), index=True, nullable=True)
    check_in_end_time =  Column(String(100), index=True, nullable=True)
    check_out_time =  Column(String(100), index=True, nullable=True)
    security_deposit =  Column(Float, index=True, nullable=True)

    listing = relationship("Listing", back_populates="listing_policy")
    key_collection = relationship("KeyCollection", back_populates="listing_policy")
    guest_policies = relationship("GuestPolicies", back_populates="listing_policy")
    fees_and_taxes = relationship("FeesandTaxes", back_populates="listing_policy")

class Rooms(Base):
    __tablename__ = "rooms"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    listing_id = Column(Integer, ForeignKey('listing.id'))
    room_type = Column(String(100), index=True, nullable=True)
    bath_count = Column(Integer, nullable=True)

    listing = relationship("Listing", back_populates="rooms")
    beds = relationship("Beds", back_populates="rooms")

class Beds(Base):
    __tablename__ = "beds"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    room_id = Column(Integer, ForeignKey('rooms.id'))
    bed_count = Column(Integer, nullable=True)
    bed_type = Column(String(100), index=True, nullable=True)

    rooms = relationship("Rooms", back_populates="beds")


class Photos(Base):
    __tablename__ = "photos"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    listing_id = Column(Integer, ForeignKey('listing.id'))
    content_type =  Column(String(100), index=True, nullable=True)
    filename =  Column(Text, nullable=True)
    caption = Column(String(100), index=True, nullable=True)
    sort_order  = Column(Integer, nullable=True)
    locale = Column(String(100), index=True, nullable=True)

    listing = relationship("Listing", back_populates="photos")
    image_tag = relationship("ImageTag", back_populates="photos")

class ImageTag(Base):
    __tablename__ = "image_tag"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    photos_id = Column(Integer, ForeignKey('photos.id'))
    name = Column(Integer, index=True, nullable=True)
    description = Column(Text, nullable=True)

    photos = relationship("Photos", back_populates="image_tag")

class ListingStatus(Base):
    __tablename__ = "listing_status"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    listing_id = Column(Integer, ForeignKey('listing.id'))
    activate = Column(Boolean, unique=False, default=False)

    listing = relationship("Listing", back_populates="listing_status")

class ListingPrice(Base):
    __tablename__ = "listing_price"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    listing_id = Column(Integer, ForeignKey('listing.id'))
    rule_type = Column(String(100), index=True, nullable=True)
    price_change = Column(Integer, nullable=True)
    price_change_type = Column(String(100), index=True, nullable=True)
    threshold = Column(Integer, nullable=True)
    start_date = Column(Date, index=True, nullable=True)
    end_date = Column(Date, index=True, nullable=True)

    listing = relationship("Listing", back_populates="listing_price")

class Reservation(Base):
    __tablename__ = "reservation"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    listing_id = Column(Integer, ForeignKey('listing.id'))
    cancellation_policy_category = Column(String(100), index=True, nullable=True)
    confirmation_code = Column(String(100), index=True, nullable=True)
    partner_confirmation_code = Column(String(100), index=True, nullable=True)
    created_at = Column(DateTime, nullable=True)
    updated_at = Column(DateTime, nullable=True)
    booked_at = Column(DateTime, nullable=True)
    start_date = Column(Date, index=True, nullable=True)
    end_date = Column(Date, index=True, nullable=True)
    guest_email = Column(String(100), index=True, nullable=True)
    guest_first_name = Column(String(100), index=True, nullable=True)
    guest_last_name = Column(String(100), index=True, nullable=True)
    guest_preferred_locale = Column(String(100), index=True, nullable=True)
    currency = Column(String(5), index=True, nullable=True)
    nightly_base_price = Column(Float, nullable=True)
    cancellation_fee = Column(String(100), index=True, nullable=True)
    partner_listing_id = Column(Integer, index=True, nullable=True)
    commission_amount = Column(String(100), index=True, nullable=True)
    nights = Column(Integer, nullable=True)
    number_of_guests = Column(Integer, nullable=True)
    tax_amount = Column(String(100), index=True, nullable=True)
    status = Column(String(100), index=True, nullable=True)
    total = Column(String(100), index=True, nullable=True)
    notes = Column(String(100), index=True, nullable=True)
    discount_code = Column(String(100), index=True, nullable=True)
    session_id = Column(String(100), index=True, nullable=True)
    ip_address = Column(String(100), index=True, nullable=True)

    listing = relationship("Listing", back_populates="reservation")
    fees = relationship("ReservationFees", back_populates="reservation")
    credit_card = relationship("CreditCard", back_populates="reservation")
    rewards = relationship("Rewards", back_populates="reservation")
    guest_phone_numbers = relationship("ReservationPhone", back_populates="reservation")
    reservation_trip = relationship("ReservationTrip", back_populates="reservation")

class ReservationPhone(Base):
    __tablename__ = "reservation_phone"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    reservation_id = Column(Integer, ForeignKey('reservation.id'))
    guest_phone_numbers = Column(String(100), index=True, nullable=True)

    reservation = relationship("Reservation", back_populates="guest_phone_numbers")

class ReservationTrip(Base):
    __tablename__ = "reservation_trip"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    reservation_id = Column(Integer, ForeignKey('reservation.id'))
    trip_purpose = Column(String(100), index=True, nullable=True)

    reservation = relationship("Reservation", back_populates="reservation_trip")

class Rewards(Base):
    __tablename__ = "rewards"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    reservation_id = Column(Integer, ForeignKey('reservation.id'))
    reward_number = Column(Integer, nullable=True)
    reward_email = Column(String(100), index=True, nullable=True)
    reward_level = Column(String(100), index=True, nullable=True)
    reward_points_used = Column(Integer, nullable=True)
    reward_points_earn = Column(Integer, nullable=True)

    reservation = relationship("Reservation", back_populates="rewards")

class CreditCard(Base):
    __tablename__ = "credit_card"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    reservation_id = Column(Integer, ForeignKey('reservation.id'))
    card_number = Column(String(100), index=True, nullable=True)
    card_month = Column(String(100), index=True, nullable=True)
    card_year = Column(String(100), index=True, nullable=True)
    card_type = Column(String(100), index=True, nullable=True)
    cc_security_code = Column(String(100), index=True, nullable=True)
    cc_address = Column(String(100), index=True, nullable=True)
    cc_country = Column(String(5), index=True, nullable=True)
    cc_state = Column(String(100), index=True, nullable=True)
    cc_city = Column(String(100), index=True, nullable=True)
    cc_birth_date = Column(Date, index=True, nullable=True)
    cc_zipcode = Column(String(100), index=True, nullable=True)
    cc_first_name = Column(String(100), index=True, nullable=True)
    cc_last_name = Column(String(100), index=True, nullable=True)

    reservation = relationship("Reservation", back_populates="credit_card")


class ReservationFees(Base):
    __tablename__ = "reservation_fees"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    reservation_id = Column(Integer, ForeignKey('reservation.id'))
    amount = Column(Float, nullable=True)
    discounted_amount = Column(Float, nullable=True)
    description = Column(Text, nullable=True)
    type = Column(String(100), index=True, nullable=True)
    sub_type = Column(String(100), index=True, nullable=True)
    included = Column(Boolean, nullable=True)

    reservation = relationship("Reservation", back_populates="fees")

class DiscountRules(Base):
    __tablename__ = "discount_rules"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    discount_id = Column(Integer, ForeignKey('discount.id'))
    rule_name = Column(String(100), index=True, nullable=True)
    rule_value = Column(String(100), index=True, nullable=True)

    discount = relationship("Discount", back_populates="discount_rules")

class DiscountAdr(Base):
    __tablename__ = "discount_adr"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    discount_id = Column(Integer, ForeignKey('discount.id'))
    discount_percent = Column(Float, nullable=True)
    channel_contribution = Column(Float, nullable=True)
    pm_contribution = Column(String(100), index=True, nullable=True)
    min_adr = Column(String(100), index=True, nullable=True)
    max_adr = Column(String(100), index=True, nullable=True)

    discount = relationship("Discount", back_populates="discount_adr")

class Discount(Base):
    __tablename__ = "discount"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    discount_code = Column(String(100), index=True, nullable=True)
    discount_description = Column(Text, nullable=True)

    discount_rules = relationship("DiscountRules", back_populates="discount")
    discount_adr = relationship("DiscountAdr", back_populates="discount")

class AmenityCategories(Base):
    __tablename__ = "amenity_categories"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    listing_id = Column(Integer, ForeignKey('listing.id'))
    code = Column(String(100), index=True, nullable=True) 

    listing = relationship("Listing", back_populates="amenity_categories")
