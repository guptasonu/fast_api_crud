# from pydantic import BaseModel, constr
from typing import List, Optional
from datetime import date, datetime
from enum import Enum
from pydantic import BaseModel as PydanticBaseModel


class BaseModel(PydanticBaseModel):
    class Config:
        use_enum_values = True


class ListingTypeCategory(str, Enum):
    Condominium = "PCT8"  
    Chalet = "PCT7"  
    Campground = "PCT6"  
    Manor = "PCT52"  
    Charm_hotel = "PCT51"  
    Recreational_vehicle_park = "PCT50"  
    Cabin_or_bungalow = "PCT5"  
    Efficiency_studio = "PCT46"  
    Boutique = "PCT45"  
    Boatel = "PCT44"  
    Pension = "PCT40"  
    Bed_and_breakfast_Listing_Type_Multi_Rep_Parent = "PCT4"  
    Castle = "PCT37"  
    Wildlife_reserve = "PCT36"  
    Villa = "PCT35"  
    Vacation_home = "PCT34"  
    Tent = "PCT33"  
    Self_catering_accommodation = "PCT32"  
    Sailing_ship = "PCT31"  
    Resort_Listing_Type_Multi_Rep_Parent = "PCT30"  
    Apartment = "PCT3"  
    Residential_apartment = "PCT29"  
    Ranch = "PCT28"  
    Motel_Listing_Type_Multi_Rep_Parent = "PCT27"  
    Monastery = "PCT26"  
    Mobile_home = "PCT25"  
    Meeting_resort = "PCT23"  
    Lodge_Listing_Type_Multi_Rep_Parent = "PCT22"  
    Inn_Listing_Type_Multi_Rep_Parent = "PCT21"  
    Hotel_Listing_Type_Multi_Rep_Parent = "PCT20"  
    Hostel = "PCT19"  
    Holiday_resort = "PCT18"  
    Guest_house_limited_service = "PCT16"  
    Guest_farm = "PCT15"  
    Ferry = "PCT14"  
    Cruise = "PCT12"  
    Apart_Hotel_Listing_Type_Multi_Rep_Parent = "PCT115"  
    Cottage = "PCT114"  
    Shared_room = "PCT113"  
    Private_room = "PCT112"  
    Bungalow = "PCT111"  
    Studio = "PCT110"  
    Suite = "PCT109"  
    Family = "PCT108"  
    Quadruple = "PCT107"
    Townhome = "PCT101"
    Triple_Room_Listing_Type_Multi_Rep = "PCT106"
    Twin_Double_Listing_Type_Multi_Rep = "PCT105"  
    Twin_Listing_Type_Multi_Rep = "PCT104"  
    Double_Room_Listing_Type_Multi_Rep = "PCT103"  
    Single_Room_Listing_Type_Multi_Rep = "PCT102"  


class ContactListTypesElement(str, Enum):
    The_primary_point_of_contact = "primary_point_of_contact"
    Contact_for_availability = "availability_contact"
    Contact_for_invoice_related_inquiry = "invoices_contact"
    Contact_for_central_reservations = "central_reservations_contact"
    Contact_for_reservations_inquiry = "reservations_contact"
    Contact_for_photos_and_description_inquiry = "photos_and_description_contact"
    Contact_for_contract_related_inquiry = "contract_contact"
    Contact_for_pricing_related_inquiry = "pricing_contact"
    Contact_for_special_request = "special_request_contact"


class ListofContacts(BaseModel):
    email_address : str
    name : str = None
    phone : str = None
    type : ContactListTypesElement

    class Config:
        orm_mode = True

class AmenityCategories(BaseModel):
    code : str 
    # description : str = None

    class Config:
        orm_mode = True


class Listing(BaseModel):
    """
    Create Listing
    """
    # listing_id : int = None
    name : str
    apt : str 
    street : str
    city : str
    country_code : str
    lat : float
    lng : float
    listing_currency : str
    detailed_description : str
    guests_included : int
    pm_id : str
    pm_name : str
    pricing_model : str
    listing_type_group: Optional[str]
    listing_type_category : Optional[ListingTypeCategory]
    bedrooms: int = None
    bathrooms : float = None
    beds : int = None
    amenity_categories : Optional[List] = []
    check_in_option : Optional[str]
    permit_or_tax_id : Optional[str]
    state : Optional[str]
    zipcode : Optional[str]
    person_capacity : int = None
    short_description : Optional[str]
    neighborhood_overview : Optional[str]
    transit : Optional[str]
    house_rules : Optional[str]
    locale : Optional[str]
    booking_settings : Optional[str]
    flags : Optional[str]
    primary_contact : Optional[str] = ""
    contacts : Optional[List[ListofContacts]] = []
    min_advance_booking_offset : Optional[str]
    max_advance_booking_offset : Optional[str]
    
    class Config:
        orm_mode = True


class ListingSchema(Listing):
    listing_id: int = None

    class Config:
        orm_mode = True


class Dates(BaseModel):
    start_date : date
    end_date : date

class SubCalendar(BaseModel):
    """
    Sub Module of Calendar
    """
    dates : List[str]
    nightly_price : Optional[float] = None
    availability : Optional[bool] = None
    available_count : Optional[int] = None
    min_los : Optional[int] = None
    max_los : Optional[int] = None
    closed_to_arrival : Optional[bool] = None
    closed_to_departure : Optional[bool] = None

class CheckinDate(BaseModel):
    date : date
    los_value : int
    amount : float

class LOSPrice(BaseModel):
    listing_id : int
    max_guests : int
    currency : str
    check_in_date : CheckinDate

class Calendar(BaseModel):
    """
    Create Calendar
    """
    listing_id : int
    calendars : Optional[List[SubCalendar]] = None
    los_price : Optional[List[LOSPrice]] = None

    class Config:
        orm_mode = True

class CancellationPolicyCategory(str, Enum):
    flexible = 'flexible'
    moderate = 'moderate'
    strict = 'strict'
    super_strict = 'super_strict'
    cancellation_30_days_with_grace_period = 'cancellation_30_days_with_grace_period'
    cancellation_60_days_with_grace_period = 'cancellation_60_days_with_grace_period'
    cancellation_14_days_with_grace_period = 'cancellation_14_days_with_grace_period'
    cancellation_90_days_with_grace_period = 'cancellation_90_days_with_grace_period'

class CheckinMethod(str,Enum):
    doorman = 'doorman'
    lock_box = 'lock_box'
    smart_lock = 'smart_lock'
    keypad = 'keypad'
    in_person_meet = 'in_person_meet'
    other = 'other'
    front_desk = 'front_desk'
    secret_spot = 'secret_spot'
    instruction_contact_us = 'instruction_contact_us'


class Instruction(BaseModel):
    how : str
    when : str

class AdditionalInfo(BaseModel):
    instruction : Optional[Instruction] = None

class KeyCollection(BaseModel):
  type : str
  check_in_method : CheckinMethod
  additional_info : Optional[AdditionalInfo] = None

class AllowedRequest(str, Enum):
    yes = 'yes'
    no = 'no'
    on_request = 'on_request'

class PriceType(str, Enum):
    free = 'free'
    charges_may_apply = 'charges_may_apply'

class GuestPolicies(BaseModel):
    smoking_allowed: Optional[int] = None
    parties_allowed: Optional[int] = None
    parking_allowed: AllowedRequest
    parking_price_type: Optional[PriceType]
    pets_allowed: AllowedRequest
    pets_price_type: Optional[PriceType]
    quiet_hours_set: Optional[int]
    quiet_hours_start_time: Optional[str]
    quiet_hours_end_time: Optional[str]

class Type(str, Enum):
    FEE = 'FEE'
    TAX = 'TAX'

class ChargedAt(str, Enum):
    BOOKING = 'booking'
    ARRIVAL = 'arrival'

class FeesAndTaxes(BaseModel):
    amount: Optional[float]
    fee_tax_id: str
    description: str
    type: Type
    charge_frequency: int
    charge_type: int
    percentage: Optional[float]
    charged_at: ChargedAt
    room_id: Optional[str] = None
    min_guests: Optional[int] = None
    max_guests: Optional[int] = None

class Policy(BaseModel):
    """
    Update Policy
    """
    cancellation_policy_category : Optional[CancellationPolicyCategory] = None
    check_in_start_time : Optional[str] = None
    check_in_end_time : Optional[str] = None
    check_out_time : Optional[str] = None
    keyCollection : Optional[KeyCollection] = None
    security_deposit : Optional[float]
    guest_policies : Optional[GuestPolicies] = None
    fees_and_taxes : Optional[List[FeesAndTaxes]] = None

    class Config:
        orm_mode = True

class RoomType(str, Enum):
    living_room = 'living_room'
    bedroom = 'bedroom'
    family_room = 'family_room'

class BedTypesElement(str, Enum):
    KING_BED = 'KING_BED'
    QUEEN_BED = 'QUEEN_BED'
    DOUBLE_BED = 'DOUBLE_BED'
    SOFA_BED = 'SOFA_BED'
    BUNK_BED = 'BUNK_BED'
    TWIN_BED = 'TWIN_BED'
    SINGLE_BED = 'SINGLE_BED'
    COT_BED = 'COT_BED'
    CRIBS = 'CRIBS'


class BedObject(BaseModel):
    bed_type: Optional[BedTypesElement] = None
    bed_count : Optional[int] = 0


class RoomObject(BaseModel):
    room_type : RoomType
    beds : List[BedObject] = []
    bath_count : Optional[int]

class Rooms(BaseModel):
    """
    Create or Update Rooms
    """
    listing_id : int
    rooms : Optional[List[RoomObject]] = None

    class Config:
        orm_mode = True

class ContentType(str,Enum):
    image_jpeg = 'image/jpeg'
    image_jpg = 'image/jpg'
    image_png = 'image/png'
    image_gif = 'image/gif'

class ImageTag(int,Enum):
    Shower = 1
    shower = 2
    Property_building = 3 
    Patio = 4 
    Nearby_landmark = 5 
    Staff = 6 
    Restaurant_places_to_eat = 7 
    Communal_lounge_TV_room = 8 
    Facade_entrance = 10
    Spring = 11
    spring = 13
    Off_site = 14 
    Food_close_up = 37
    Day = 41
    Night = 42
    People = 43
    Property_logo_or_sign = 50
    Neighborhood = 55
    Natural_landscape = 61
    Activities = 70
    Birds_eye_view = 74
    Winter = 81
    Summer = 82
    BBQ_facilities = 87
    Billiard = 89
    Bowling = 90
    Casino = 94
    Place_of_worship = 95
    Children_play_ground = 96
    Darts = 97
    Fishing = 100
    Game_Room = 102
    Garden = 103
    Golf_course = 104
    Horse_riding = 106
    Hot_Spring_Bath = 107
    Hot_Tub = 108
    Karaoke = 112
    Library = 113
    Massage = 114
    Minigolf = 115
    Nightclub_DJ = 116
    Sauna = 124
    On_site_shops = 125
    Ski_School = 128
    Skiing = 131
    Snorkeling = 133
    Solarium = 134
    Squash = 137
    Table_tennis = 141
    Steam_room = 143
    Bathroom = 153
    TV_and_multimedia = 154
    Coffee_tea_facilities = 155
    View_from_property_room = 156
    Balcony_Terrace = 157
    Kitchen_or_kitchenette = 158
    Living_room = 159
    Lobby_or_reception = 160
    Lounge_or_bar = 161
    Spa_and_wellness_center_facilities = 164
    Fitness_center_facilities = 165
    Food_and_drinks = 167
    Other = 172
    Photo_of_the_whole_room = 173
    Business_facilities = 177
    Banquet_Function_facilities = 178
    Decorative_detail = 179
    Seating_area = 182
    Floor_plan = 183
    Dining_area = 184
    Beach = 185
    Aqua_park = 186
    Tennis_court = 187
    Windsurfing = 188
    Canoeing = 189
    Hiking = 190
    Cycling = 191
    Diving = 192
    Kids_club = 193
    Evening_entertainment = 194
    Logo_Certificate_Sign = 197
    Animals = 198
    Bedroom = 199
    Communal_kitchen = 204
    Autumn = 205
    On_site = 240
    Meeting_conference_room = 241
    Food = 242
    Text_overlay = 245
    Pets = 246
    Guests = 247
    City_view = 248
    Garden_view = 249
    Lake_view = 250
    Landmark_view = 251
    Mountain_view = 252
    Pool_view = 253
    River_view = 254
    Sea_view = 255
    Street_view = 256
    Area_and_facilities = 257
    Supermarket_grocery_shop = 258
    Shopping_Area = 259
    Swimming_pool = 260
    Sports = 261
    Entertainment = 262
    Meals = 263
    Breakfast = 264
    Continental_breakfast = 265
    Buffet_breakfast = 266
    Asian_breakfast = 267
    Italian_breakfast = 268
    English_Irish_breakfast = 269
    American_breakfast = 270
    Lunch = 271
    Dinner = 272
    Drinks = 273
    Alcoholic_drinks = 274
    Nonalcoholic_drinks = 275
    Seasons = 276
    Time_of_day = 277
    Location = 278
    Sunrise = 279
    Sunset = 280
    children = 281
    young_children = 282
    older_children = 283
    group_of_guests = 284
    cot = 285
    bunk_bed = 286
    Certificate_Award = 287
    ADAM = 288
    Open_Air_Bath = 289
    Public_Bath = 290
    Family = 291

class Photos(BaseModel):
    """
    Create Photo
    """
    listing_id: int
    content_type: ContentType
    filename: str
    caption: Optional[str]
    sort_order: Optional[int]
    tags: Optional[List[ImageTag]]
    locale: Optional[str] = "EN"

    class Config:
        orm_mode = True


class ListingStatus(BaseModel):
    """
    Updating Listing Status
    """
    activate : bool = False

    class Config:
        orm_mode = True

class RuleType(str, Enum):
    SEASONAL_ADJUSTMENT = 'SEASONAL_ADJUSTMENT'
    LOS_ADJUSTMENT = 'LOS_ADJUSTMENT'
    WEEKEND_ADJUSTMENT = 'WEEKEND_ADJUSTMENT'
    LAST_MIN_DISCOUNT = 'LAST_MIN_DISCOUNT'
    EARLY_BIRD_DISCOUNT = 'EARLY_BIRD_DISCOUNT'

class PriceChangeType(str,Enum):
    PERCENT = 'PERCENT'
    ABSOLUTE = 'ABSOLUTE'


class ListingPricingRules(BaseModel):
    rule_type: RuleType
    price_change: int
    price_change_type: PriceChangeType
    threshold : Optional[int]
    start_date: str
    end_date: str


class ListingPrice(BaseModel):
    """
    Creating Listing Price
    """
    listing_id: int
    pricing_rule: Optional[ListingPricingRules]

    class Config:
        orm_mode = True


class Fees(BaseModel):
    amount: float
    discounted_amount: Optional[float]
    description: str
    type: str
    sub_type: Optional[str]
    included: Optional[bool]

class CommissionObject(BaseModel):
    commission_amount : str
    currency : str

class Status(str,Enum):
    Book = 'Book'
    Modify = 'Modify'
    Cancel = 'Cancel'


class CreditCardElement(int, Enum):
    MasterCard = 0
    Visa = 1
    AmericanExpress = 2
    DinersClub = 3
    Discover = 4
    JCB = 5


class CreditCardObject(BaseModel):
    card_number: str
    card_month: str
    card_year: str
    card_type: CreditCardElement
    cc_security_code: str
    cc_address: str
    cc_country: str
    cc_state: Optional[str]
    cc_city: str
    cc_birth_date: Optional[str]
    cc_zipcode: Optional[str]
    cc_first_name: Optional[str]
    cc_last_name: Optional[str]

class RewardsObject(BaseModel):
    reward_number: int
    reward_email: str
    reward_level: str
    reward_points_used: int
    reward_points_earn: int


class GuestPhoneNumber(BaseModel):
    guest_phone_numbers: str


class Reservation(BaseModel):
    """
    Create Reservation SUb Model
    """
    cancellation_policy_category: str
    confirmation_code: str
    created_at: str = datetime.now().isoformat()
    updated_at: str = datetime.now().isoformat()
    booked_at: str = datetime.now().isoformat()
    start_date : date
    end_date : date
    guest_email : str
    guest_first_name : str
    guest_last_name : str
    guest_phone_numbers : Optional[List[str]] = []
    guest_preferred_locale : str = "EN"
    currency : str = "USD"
    nightly_base_price : float
    fees: List[Fees] = []
    cancellation_fee: str = "0"
    commission : Optional[CommissionObject]
    listing_id : int
    nights : int
    number_of_guests : int
    tax_amount: str = "0"
    status: Status
    total : str
    credit_card : Optional[CreditCardObject]
    rewards : Optional[RewardsObject]
    notes : Optional[str] = ""
    trip_purpose : List[str] = []
    discount_code : Optional[str]
    session_id : str
    ip_address : str

    class Config:
        orm_mode = True


class ReservationRequest(BaseModel):
    """
    V2 Reservation Request
    """
    listing_id : int
    reservation : Optional[Reservation]

    class Config:
        orm_mode = True

class SubUpdateReservation(BaseModel):
    """
    Update Reservation Sub Model
    """
    recalculate_price : str
    recalculate_channel_commission : str
    confirmation_id : str
    reservation_id : str
    property_manager_id : str
    property_id : str
    from_date : str
    to_date : str
    notes : str
    guest_count : str
    adults : str
    children : str
    renter : str
    quote : str
    commission : str

class RenterObject(BaseModel):
    firstName : str
    lastName : str
    phone : str
    email : str

class FeesforReservationModificationObject(BaseModel):
    name : str
    value : str
    taxType : int
    currency : str
    unit : int

class TaxTypesforQuoteElement(str, Enum):
    IncomeTax = 'IncomeTax'
    PayrollTax = 'PayrollTax'
    PurchaseTax = 'PurchaseTax'
    SalesTaxIncluded = 'SalesTaxIncluded'
    SalesTaxExcluded = 'SalesTaxExcluded'
    SalesTaxOnTax = 'SalesTaxOnTax'


class TaxesforReservationModificationObject(BaseModel):
    name : str
    amount : float
    type : TaxTypesforQuoteElement


class QuoteforReservationModificationObject(BaseModel):
    currency : str
    price : float
    fees : List[FeesforReservationModificationObject] = []
    taxes : List[TaxesforReservationModificationObject] = []

class CommissionforReservationModificationObject(BaseModel):
    channel_commission_amount : float
    currency : str


class ReservationModificationObject(BaseModel):
    confirmation_id : str
    recalculate_price : bool = False
    recalculate_channel_commission : bool = False
    reservation_id : Optional[str]
    property_manager_id : Optional[str]
    property_id : Optional[str]
    from_date : Optional[date]
    to_date : Optional[date]
    notes : Optional[str]
    guest_count : Optional[int]
    adults_count : Optional[int]
    children_count : Optional[int]
    renter : Optional[RenterObject] = None
    quote : Optional[QuoteforReservationModificationObject] = None
    commission : Optional[CommissionforReservationModificationObject] = None


class UpdateReservation(BaseModel):
    """
    Update Reservation
    """
    # listing_id : int
    reservation : ReservationModificationObject

    class Config:
        orm_mode = True

class RuleNameEnum(str,Enum):
    PM_LIST = 'PM_LIST'
    BLACKOUT_DATES = 'BLACKOUT_DATES'
    VALID_DATES = 'VALID_DATES'
    ADDL_DATES = 'ADDL_DATES'

class SubDiscountRule(BaseModel):
    """
    Sub Models of Discount Rules
    """
    rule_name : RuleNameEnum 
    rule_value : List[str]

class SubADROptions(BaseModel):
    """
    Sub Models of ADR Options
    """
    discount_percent: Optional[float]
    channel_contribution: Optional[float]
    pm_contribution: Optional[str]
    min_adr: Optional[str]
    max_adr: Optional[str]

class CreateDiscount(BaseModel):
    """
    Create Discouont
    """
    discount_code: str
    discount_description: Optional[str]
    discount_rules: List[SubDiscountRule]
    adr_options: Optional[List[SubADROptions]]

    class Config:
        orm_mode = True


class CancellationItemsObject(BaseModel):
    """
    Cancellation Items Object
    """
    cancellation_amount_after: float
    cancellation_date: str
    cancellation_time: str = None
    cancellation_nights: Optional[int] = None
    cancellation_type: Optional[str] = None
    cancellation_amount_before: Optional[float] = None
    days_before_arrival_amount: Optional[int] = None
    transaction_fee: Optional[float] = None
    actual_cancellation_date: Optional[str] = None
    actual_cancellation_time: Optional[str] = None


class Quote(BaseModel):
    """
    V2 Quote Object
    """
    amount: float
    description: str
    type: str
    discounted_amount: Optional[float] = None
    sub_type: Optional[str] = None
    included: Optional[bool] = None


class QuoteResponse(BaseModel):
    """
    V2 Quote Response
    """
    available: bool
    failure_code: Optional[str] = None
    cancellation_items: List[CancellationItemsObject] = []
    currency: Optional[str] = None
    first_payment: Optional[float] = None
    second_payment: Optional[float] = None
    second_payment_date: Optional[str] = None
    min_stay: Optional[int] = None
    check_in_time: Optional[str] = None
    check_out_time: Optional[str] = None
    property_manager_supported_cc: List[str] = []
    terms_link: Optional[str] = None
    quote: List[Quote] = []
    total: Optional[float] = None
    total_in_points_denomination: Optional[float] = None
    original_total: Optional[float] = None
    discounted_total: Optional[float] = None
    discount_percentage: Optional[float] = None
    discount_amount: Optional[float] = None
