
class ListingStroge:
    listing_fields = []
    listing_id = []
    photos_id = []
    price_rule_ids = []
    discount_ids = []
    discount_codes = []

    def __init__(self):

        self.listing_fields = ["listing_id","name", "apt","street", "city","country_code", "lat", "lng", "listing_currency",
            "detailed_description","guests_included", "pm_name", "pm_id","pricing_model"]
        self.listing_id = []
        self.photos_id = []
        self.price_rule_ids = []
        self.discount_ids = []
        self.discount_codes = []

class ListingPayload:
    # Create Listing Payload and Response
    
    listing_payload_1 = {
        "name": "Casa Scott 781153",
        "apt": "Unit 8",
        "street": "78 Polarino Uno",
        "city": "Liberia",
        "country_code": "CR",
        "lat": 10.62456,
        "lng": -85.6852,
        "listing_currency": "CRC",
        "detailed_description": "Located on the main floor. Sitting area, en-suite bathroom. The interior living areas open fully to two swimming pools, one cascading into the other, and to the ample decking surrounding both. Covered outdoor lounging and dining areas allow guests to take full advantage of these views, and there are numerous opportunities for sunning poolside, too.\\nThe property has seven bedrooms, including five roomy suites that open to a terrace or the deck, and two single rooms. The home is fully air conditioned, has WiFi, flat-screen TVs and a games room with a ping-pong table. Guests enjoy access to all the facilities at Peninsula Papagayo, including the private Prieta Beach Club, golf, tennis, dining and fitness facilities.",
        "guests_included": 12,
        "pm_name": "Jose Hernandez",
        "pm_id": 4,
        "pricing_model": "pricing_model4",
        "listing_type_category": "PCT36",
        "bedrooms": 5,
        "bathrooms": 5.5,
        "beds": 4,
        "state": "Texas",
        "zipcode": "77090",
        "person_capacity": 3,
        "neighborhood_overview": "Great neighborhood in the middle of downtown.",
        "transit": "Uber, Lyft",
        "booking_settings": "inquiry_and_instant_booking",
        "primary_contact": "George Scott",
        "amenity_categories": ["HAC116", "HAC254", "HAC195"],
        "contacts": [
            {
                "email_address": "george@furraylogic.com",
                "type": "primary_point_of_contact",
                "name": "George Scott",
                "phone": "9174055795"
            },
            {
                "email_address": "george@sojournapi.com",
                "type": "availability_contact",
                "name": "George Scott",
                "phone": "9174055795"
            }
        ],
        "min_advance_booking_offset": "P3D",
        "max_advance_booking_offset": "P12M"
    }
    payload_1_response = {
        "bedrooms": 5,
        "booking_settings": "inquiry_and_instant_booking",
        "city": "Liberia",
        "listing_id": None,
        "detailed_description": "Located on the main floor. Sitting area, en-suite bathroom. The interior living areas open fully to two swimming pools, one cascading into the other, and to the ample decking surrounding both. Covered outdoor lounging and dining areas allow guests to take full advantage of these views, and there are numerous opportunities for sunning poolside, too.\\nThe property has seven bedrooms, including five roomy suites that open to a terrace or the deck, and two single rooms. The home is fully air conditioned, has WiFi, flat-screen TVs and a games room with a ping-pong table. Guests enjoy access to all the facilities at Peninsula Papagayo, including the private Prieta Beach Club, golf, tennis, dining and fitness facilities.",
        "state": "Texas",
        "bathrooms": 5.5,
        "primary_contact": "George Scott",
        "zipcode": "77090",
        "beds": 4,
        "neighborhood_overview": "Great neighborhood in the middle of downtown.",
        "min_advance_booking_offset": "P3D",
        "country_code": "CR",
        "transit": "Uber, Lyft",
        "lat": 10.6246,
        "max_advance_booking_offset": "P12M",
        "name": "Casa Scott 781153",
        "apt": "Unit 8",
        "pm_name": "Jose Hernandez",
        "lng": -85.6852,
        "pm_id": "4",
        "person_capacity": 3,
        "street": "78 Polarino Uno",
        "guests_included": 12,
        "pricing_model": "pricing_model4",
        "listing_type_category": "PCT36",
        "listing_currency": "CRC",
        "contacts": [
            {
                "name": "George Scott",
                "type": "primary_point_of_contact",
                "email_address": "george@furraylogic.com",
                "phone": "9174055795"
            },
            {
                "name": "George Scott",
                "type": "availability_contact",
                "email_address": "george@sojournapi.com",
                "phone": "9174055795"
            }
        ],
        "amenity_categories": [
            "HAC116",
            "HAC254",
            "HAC195"
        ]
    }
    listing_payload_2 = {
        "name": "Casa Armadillo",
        "apt": "Unit 8",
        "street": "78 Polarino Uno",
        "city": "Liberia",
        "country_code": "CR",
        "lat": 10.624561,
        "lng": -85.68527,
        "listing_currency": "CRC",
        "detailed_description": "Located on the main floor. Sitting area, en-suite bathroom. The interior living areas open fully to two swimming pools, one cascading into the other, and to the ample decking surrounding both. Covered outdoor lounging and dining areas allow guests to take full advantage of these views, and there are numerous opportunities for sunning poolside, too.\\nThe property has seven bedrooms, including five roomy suites that open to a terrace or the deck, and two single rooms. The home is fully air conditioned, has WiFi, flat-screen TVs and a games room with a ping-pong table. Guests enjoy access to all the facilities at Peninsula Papagayo, including the private Prieta Beach Club, golf, tennis, dining and fitness facilities.",
        "guests_included": 12,
        "pm_name": "Jose Hernandez",
        "pm_id": 248,
        "pricing_model": "pricing_model4"
    }
    payload_2_response = {
        "detailed_description": "Located on the main floor. Sitting area, en-suite bathroom. The interior living areas open fully to two swimming pools, one cascading into the other, and to the ample decking surrounding both. Covered outdoor lounging and dining areas allow guests to take full advantage of these views, and there are numerous opportunities for sunning poolside, too.\\nThe property has seven bedrooms, including five roomy suites that open to a terrace or the deck, and two single rooms. The home is fully air conditioned, has WiFi, flat-screen TVs and a games room with a ping-pong table. Guests enjoy access to all the facilities at Peninsula Papagayo, including the private Prieta Beach Club, golf, tennis, dining and fitness facilities.",
        "min_advance_booking_offset": "",
        "country_code": "CR",
        "max_advance_booking_offset": "",
        "lat": 10.6246,
        "pm_name": "Jose Hernandez",
        "lng": -85.6853,
        "pm_id": "248",
        "pricing_model": "pricing_model4",
        "apt": "Unit 8",
        "guests_included": 12,
        "name": "Casa Armadillo",
        "listing_currency": "CRC",
        "listing_id": None,
        "street": "78 Polarino Uno",
        "city": "Liberia"
    }
    listing_payload_list = [listing_payload_1,listing_payload_2]
    listing_response_list = [payload_1_response, payload_2_response]

    # Update listing Payload and response

    update_listing_payload_1 = {
        "name": "Casa Scott 7121236 Changed",
        "apt": "Unit 8",
        "street": "78 Polarino Uno",
        "city": "Houston",
        "country_code": "US",
        "lat": 10.624561,
        "lng": -85.68527,
        "listing_currency": "USD",
        "short_description": "This is a great test listing.",
        "detailed_description": "Located on the main floor. Sitting area, en-suite bathroom. The interior living areas open fully to two swimming pools, one cascading into the other, and to the ample decking surrounding both. Covered outdoor lounging and dining areas allow guests to take full advantage of these views, and there are numerous opportunities for sunning poolside, too.\\nThe property has seven bedrooms, including five roomy suites that open to a terrace or the deck, and two single rooms. The home is fully air conditioned, has WiFi, flat-screen TVs and a games room with a ping-pong table. Guests enjoy access to all the facilities at Peninsula Papagayo, including the private Prieta Beach Club, golf, tennis, dining and fitness facilities.",
        "guests_included": 12,
        "pm_name": "Jose Hernandez",
        "pm_id": 248,
        "pricing_model": "LOS",
        "listing_type_category": "PCT36",
        "bedrooms": 4,
        "bathrooms": 5.5,
        "beds": 6,
        "state": "Texas",
        "zipcode": "77090",
        "person_capacity": 12,
        "neighborhood_overview": "Great neighborhood in the middle of downtown.",
        "transit": "Uber, Lyft",
        "booking_settings": "inquiry_and_instant_booking",
        "primary_contact": "George Scott",
        "contacts": [
            {
                "email_address": "george@furraylogic.com",
                "type": "availability_contact",
                "name": "George Scott Change 1",
                "phone": "9174055795"
            },
            {
                "email_address": "george@techfiniti.org",
                "type": "primary_point_of_contact",
                "name": "George Scott Change 2",
                "phone": "9174055795"
            }
        ],
        "min_advance_booking_offset": "P3D",
        "max_advance_booking_offset": "P12M"
    }

    update_listing_respone_1 = {
        'lng': -85.6853,
        'pm_id': '248',
        'guests_included': 12,
        'apt': 'Unit 8',
        'pricing_model': 'LOS',
        'person_capacity': 12,
        'booking_settings': 'inquiry_and_instant_booking',
        'street': '78 Polarino Uno',
        'listing_id': None,
        'name': 'Casa Scott 7121236 Changed',
        'listing_currency': 'USD',
        'city': 'Houston',
        'listing_type_category': 'PCT36',
        'short_description': 'This is a great test listing.',
        'primary_contact': 'George Scott',
        'state': 'Texas',
        'detailed_description': 'Located on the main floor. Sitting area, en-suite bathroom. The interior living areas open fully to two swimming pools, one cascading into the other, and to the ample decking surrounding both. Covered outdoor lounging and dining areas allow guests to take full advantage of these views, and there are numerous opportunities for sunning poolside, too.\\nThe property has seven bedrooms, including five roomy suites that open to a terrace or the deck, and two single rooms. The home is fully air conditioned, has WiFi, flat-screen TVs and a games room with a ping-pong table. Guests enjoy access to all the facilities at Peninsula Papagayo, including the private Prieta Beach Club, golf, tennis, dining and fitness facilities.',
        'bedrooms': 4,
        'zipcode': '77090',
        'min_advance_booking_offset': 'P3D',
        'bathrooms': 5.5,
        'neighborhood_overview': 'Great neighborhood in the middle of downtown.',
        'max_advance_booking_offset': 'P12M',
        'country_code': 'US',
        'beds': 6,
        'transit': 'Uber, Lyft',
        'pm_name': 'Jose Hernandez',
        'lat': 10.6246,
        'contacts': [
            {
            'phone': '9174055795',
            'email_address': 'george@furraylogic.com',
            'type': 'availability_contact',
            'name': 'George Scott Change 1'
            },
            {
            'phone': '9174055795',
            'email_address': 'george@techfiniti.org',
            'type': 'primary_point_of_contact',
            'name': 'George Scott Change 2'
            }
        ],
        'amenity_categories': [
            'HAC116',
            'HAC254',
            'HAC195'
        ]
    }

    update_listing_payload_2 = {
        "name": "Casa Armadillo update",
        "apt": "Unit 8 update",
        "street": "78 Polarino Uno update",
        "city": "Liberia update",
        "country_code": "CR",
        "lat": 11.624561,
        "lng": -75.68527,
        "listing_currency": "CRC",
        "detailed_description": "update Located on the main floor. Sitting area, en-suite bathroom. The interior living areas open fully to two swimming pools, one cascading into the other, and to the ample decking surrounding both. Covered outdoor lounging and dining areas allow guests to take full advantage of these views, and there are numerous opportunities for sunning poolside, too.\\nThe property has seven bedrooms, including five roomy suites that open to a terrace or the deck, and two single rooms. The home is fully air conditioned, has WiFi, flat-screen TVs and a games room with a ping-pong table. Guests enjoy access to all the facilities at Peninsula Papagayo, including the private Prieta Beach Club, golf, tennis, dining and fitness facilities.",
        "guests_included": 15,
        "pm_name": "Jose Hernandez update",
        "pm_id": 250,
        "pricing_model": "pricing_model5"
    }
    update_lisgint_response_2 = {
        'lng': -75.6853,
        'pm_id': '250',
        'guests_included': 15,
        'apt': 'Unit 8 update',
        'pricing_model': 'pricing_model5',
        'street': '78 Polarino Uno update',
        'name': 'Casa Armadillo update',
        'listing_id': None,
        'listing_currency': 'CRC',
        'city': 'Liberia update',
        'detailed_description': 'update Located on the main floor. Sitting area, en-suite bathroom. The interior living areas open fully to two swimming pools, one cascading into the other, and to the ample decking surrounding both. Covered outdoor lounging and dining areas allow guests to take full advantage of these views, and there are numerous opportunities for sunning poolside, too.\\nThe property has seven bedrooms, including five roomy suites that open to a terrace or the deck, and two single rooms. The home is fully air conditioned, has WiFi, flat-screen TVs and a games room with a ping-pong table. Guests enjoy access to all the facilities at Peninsula Papagayo, including the private Prieta Beach Club, golf, tennis, dining and fitness facilities.',
        'min_advance_booking_offset': '',
        'max_advance_booking_offset': '',
        'country_code': 'CR',
        'lat': 11.6246,
        'pm_name': 'Jose Hernandez update'
    }
    update_listing_payload_list = [update_listing_payload_1,update_listing_payload_2]
    update_listing_respone_list = [update_listing_respone_1, update_lisgint_response_2]

class CalendarPayload:
    cal_payload_1 = {
        "listing_id": None,
        "calendars": [
            {
            "dates": [
                "2021-07-01",
                "2021-07-02:2021-07-05"
            ],
            "nightly_price": 250,
            "availability": True,
            "available_count": 5,
            "min_los": 2,
            "max_los": 3,
            "closed_to_arrival": True,
            "closed_to_departure": True
            }
        ],
        "los_price": [
            {
            "listing_id": 9,
            "max_guests": 2,
            "currency": "usd",
            "check_in_date": {
                "date": "2021-07-08",
                "los_value": 5,
                "amount": 250
            }
            }
        ]
    }
    cal_res_1 = {
        'listing_id': None,
        'calendars': [
            {
            'closed_to_departure': True,
            'min_los': 2,
            'max_los': 3,
            'availability': True,
            'closed_to_arrival': True,
            'available_count': 5,
            'nightly_price': 250.0,
            'listing_id': None,
            'dates': [
                '2021-07-01',
                '2021-07-02:2021-07-05'
            ]
            }
        ],
        'los_price': [
            {
            'calendar_id': 5,
            'currency': 'usd',
            'listing_id': 9,
            'max_guests': 2,
            'check_in_date': {
                'date': '2021-07-08',
                'los_value': 5,
                'amount': 250.0
            }
            }
        ]
    }
    cal_payload_list = [cal_payload_1]
    cal_response_list = [cal_res_1]

class ListingPolicyPayload:
    payload_1 = {
        "cancellation_policy_category": "strict",
        "check_in_start_time": "5",
        "check_in_end_time": "3",
        "check_out_time": "3",
        "keyCollection": {
            "type": "test type",
            "check_in_method": "lock_box",
            "additional_info": {
            "instruction": {
                "how": "test how ",
                "when": "test when"
            }
            }
        },
        "security_deposit": 50,
        "guest_policies": {
            "parking_allowed": "yes",
            "pets_allowed": "yes",
            "smoking_allowed": 0,
            "parties_allowed": 0,
            "parking_price_type": "free",
            "pets_price_type": "free",
            "quiet_hours_set": 1,
            "quiet_hours_start_time": "1:00",
            "quiet_hours_end_time": "2:00"
        },
        "fees_and_taxes": [
            {
            "amount": 250,
            "fee_tax_id": "142HJTS",
            "description": "Cleaning Fee",
            "type": "TAX",
            "charge_frequency": 1,
            "charge_type": 2,
            "percentage": 250,
            "charged_at": "BOOKING",
            "room_id": "234568",
            "min_guests": 3,
            "max_guests": 8
            }
        ]
    }
    response_1 = {
        'cancellation_policy_category': 'strict',
        'check_in_start_time': '5',
        'check_in_end_time': '3',
        'check_out_time': '3',
        'security_deposit': 50.0,
        'keyCollection': {
            'type': 'test type',
            'check_in_method': 'lock_box',
            'additional_info': {
            'instruction': {
                'how': 'test how ',
                'when': 'test when'
            }
            }
        },
        'guest_policies': {
            'smoking_allowed': False,
            'parties_allowed': False,
            'parking_allowed': 'yes',
            'parking_price_type': 'free',
            'pets_allowed': 'yes',
            'pets_price_type': 'free',
            'quiet_hours_set': 1,
            'quiet_hours_start_time': '1:00',
            'quiet_hours_end_time': '2:00'
        },
        'fees_and_taxes': [
            {
            'amount': 250.0,
            'fee_tax_id': '142HJTS',
            'description': 'Cleaning Fee',
            'type': 'TAX',
            'charge_frequency': 1,
            'charge_type': 2,
            'percentage': 250.0,
            'charged_at': 'BOOKING',
            'room_id': '234568',
            'min_guests': 3,
            'max_guests': 8
            }
        ]
    }
    payload_list = [payload_1]
    response_list = [response_1]

class RoomPayload:
    payload_1 = {
        "listing_id": None,
        "rooms": [
            {
            "room_type": "living_room",
            "beds": []
            },
            {
            "room_type": "bedroom",
            "beds": [
                {
                "bed_type": "KING_BED",
                "bed_count": 1
                }
            ]
            },
            {
            "room_type": "bedroom",
            "beds": [
                {
                "bed_type": "QUEEN_BED"
                }
            ]
            },
            {
            "room_type": "living_room",
            "beds": [
                {
                "bed_type": "SOFA_BED",
                "bed_count": 1
                },
                {
                "bed_type": "COT_BED",
                "bed_count": 1
                }
            ]
            }
        ]
    }

    response_1 = {
        "listing_id": None,
        "rooms": [
            {
            "room_type": "living_room",
            "beds": []
            },
            {
            "room_type": "bedroom",
            "beds": [
                {
                "bed_type": "KING_BED",
                "bed_count": 1
                }
            ]
            },
            {
            "room_type": "bedroom",
            "beds": [
                {
                "bed_type": "QUEEN_BED",
                "bed_count": 0
                }
            ]
            },
            {
            "room_type": "living_room",
            "beds": [
                {
                "bed_type": "SOFA_BED",
                "bed_count": 1
                },
                {
                "bed_type": "COT_BED",
                "bed_count": 1
                }
            ]
            }
        ]
    }
    payload_list = [payload_1]
    response_list = [response_1]

class PhotoPyaload:
    payload_1 = {
        "listing_id": None,
        "content_type": "image/jpg",
        "filename": "filename8",
        "caption": "Test caption",
        "sort_order": 124,
        "tags": [
            37,
            55
        ],
        "locale": "HN"
    }
    response_1 = {
        "locale": "HN",
        "caption": "Test caption",
        "content_type": "image/jpg",
        "filename": "filename8",
        "sort_order": 124,
        "listing_id": None,
        "tags": [
            37,
            55
        ],
        "photo_id": None
    }
    payload_list = [payload_1]
    response_list = [response_1]

class PriceRulePayload:
    payload_1 = {
        "listing_id": None,
        "pricing_rule": {
            "rule_type": "LOS_ADJUSTMENT",
            "price_change": 1,
            "price_change_type": "PERCENT",
            "start_date": "2021-08-28",
            "end_date": "2021-08-30",
            "threshold": 28
        }
    }
    payload_list = [payload_1]


class CreateDiscountPayload:
    payload_1 = {
        "discount_code": "DISC15",
        "discount_rules": [
            {
            "rule_name": "PM_LIST",
            "rule_value": [
                "rule_value1",
                "rule_value2"
            ]
            },
            {
            "rule_name": "PM_LIST",
            "rule_value": [
                "rule_value0",
                "rule_value1"
            ]
            },
            {
            "rule_name": "PM_LIST",
            "rule_value": [
                "rule_value9",
                "rule_value0",
                "rule_value1"
            ]
            }
        ],
        "adr_options": [
            {
            "discount_percent": 10,
            "channel_contribution": 5,
            "pm_contribution": "9",
            "min_adr": "test min adr",
            "max_adr": "test max adr"
            }
        ],
        "discount_description": "Test discount description"
    }
    payload_list = [payload_1]

class UpdateDiscountPayload:
    payload_1 = {
        "discount_code": None,
        "discount_rules": [
            {
            "rule_name": "PM_LIST",
            "rule_value": [
                "rule_value1update",
                "rule_value2update"
            ]
            },
            {
            "rule_name": "PM_LIST",
            "rule_value": [
                "rule_value0update",
                "rule_value1update"
            ]
            },
            {
            "rule_name": "PM_LIST",
            "rule_value": [
                "rule_value9",
                "rule_value0"
            ]
            }
        ],
        "adr_options": [
            {
            "discount_percent": 11,
            "channel_contribution": 5,
            "pm_contribution": "6",
            "min_adr": "test min adr update",
            "max_adr": "test max adr update"
            }
        ],
        "discount_description": "Test discount description update"
    }
    payload_list = [payload_1]
