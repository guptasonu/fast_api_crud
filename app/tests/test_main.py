import json
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.engine.url import URL
from sqlalchemy.orm import sessionmaker
from dotenv import load_dotenv
import os
import pytest

from app.main import app, get_db
from app.database import Base
from app.tests import conftest as test_helper

load_dotenv()
DB = {
    'drivername': 'mysql+mysqlconnector',
    'host': os.getenv('TEST_DB_ADDRESS', '34.71.20.154'),
    'port': os.getenv('TEST_DB_PORT', '3306'),
    'username': os.getenv('TEST_DB_USER', 'furraylogic'),
    'password': os.getenv('TEST_DB_PWD', 'FurrayL@2AVEl'),
    'database': os.getenv('TEST_DB_SCHEMA', 'test_bkgpal'),
    'query': {'charset': 'utf8'}
}
API_KEY = os.getenv("API_KEY", "furraylogic")
# DB = {
#     'drivername': 'mysql+mysqlconnector',
#     'host': '34.71.20.154',
#     'port': '3306',
#     'username': 'furraylogic',
#     'password': "FurrayL@2AVEl",
#     'database': 'test_bkgpal',
#     'query': {'charset':'utf8'}
# }

engine = create_engine(URL.create(**DB), isolation_level="AUTOCOMMIT")

TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base.metadata.create_all(bind=engine)


def override_get_db():
    try:
        db = TestingSessionLocal()
        yield db
    finally:
        db.close()


app.dependency_overrides[get_db] = override_get_db

client = TestClient(app)

class TestListing:

    def comman_func(self, response, fields_list=None):

        assert response.status_code == 200, response.text
        data = response.json()
        if fields_list is not None:
            for field in fields_list:
                assert field in data
        return data

    @pytest.mark.filterwarnings('ignore::RuntimeWarning')
    def test_create_listing(self):
        for payload , payload_response in zip(test_helper.ListingPayload.listing_payload_list, test_helper.ListingPayload.listing_response_list):
            response = client.post(
                "/v2/listings",
                headers={"x-api-key": API_KEY},
                json=payload
            )
            data = self.comman_func(response=response,fields_list=test_helper.ListingStroge.listing_fields)
            test_helper.ListingStroge.listing_id.append(data.get("listing_id"))
            payload_response["listing_id"] = data.get("listing_id")
            assert data == payload_response
    
    @pytest.mark.filterwarnings('ignore::RuntimeWarning')
    def test_update_listing(self):
        
        """ Update the listing """

        for payload , payload_response, listing_id in zip(test_helper.ListingPayload.update_listing_payload_list, test_helper.ListingPayload.update_listing_respone_list,test_helper.ListingStroge.listing_id):
            response = client.put(
                f"/v2/listings/{listing_id}",
                headers={"x-api-key": API_KEY},
                json=payload
            )

            data = self.comman_func(response=response,fields_list=test_helper.ListingStroge.listing_fields)
            payload_response["listing_id"] = listing_id

            assert data == payload_response
    
    @pytest.mark.filterwarnings('ignore::RuntimeWarning')
    def test_get_calendar(self):

        """Create and Update the Calendar"""
        for payload, payload_response, listing_id in zip(test_helper.CalendarPayload.cal_payload_list,test_helper.CalendarPayload.cal_response_list, test_helper.ListingStroge.listing_id):

            payload["listing_id"] = listing_id
            response = client.post(
                "/v2/listing/calendar",
                headers={"x-api-key": API_KEY},
                json=payload
            )

            data = self.comman_func(response=response,fields_list=["listing_id"])
            payload_response["listing_id"] = listing_id
            for calendar in payload_response.get("calendars"):
                calendar["listing_id"] = listing_id
            assert data == payload_response
    
    @pytest.mark.filterwarnings('ignore::RuntimeWarning')
    def test_update_listing_policy(self):

        """ Update Policy Listing """
        for payload, payload_response, listing_id in zip(test_helper.ListingPolicyPayload.payload_list,test_helper.ListingPolicyPayload.response_list, test_helper.ListingStroge.listing_id):

            response = client.put(
                f"/v2/listing_policies/{listing_id}",
                headers={"x-api-key": API_KEY},
                json=payload
            )

            data = self.comman_func(response=response)
            assert data == payload_response

    @pytest.mark.filterwarnings('ignore::RuntimeWarning')
    def test_create_or_update_rooms(self):

        """ Create and Update the Rooms"""

        for payload, payload_response, listing_id in zip(test_helper.RoomPayload.payload_list, test_helper.RoomPayload.response_list ,test_helper.ListingStroge.listing_id):
            
            payload["listing_id"] = listing_id
            response = client.post(
                f"/v2/listing_rooms",
                headers={"x-api-key": API_KEY},
                json=payload
            )
            data = self.comman_func(response)
            payload_response["listing_id"] = listing_id
            assert data == payload_response
    
    @pytest.mark.filterwarnings('ignore::RuntimeWarning')
    def test_create_listing_photos(self):
        
        """ Create Listing Photos"""

        for payload ,response_payload, listing_id in zip(test_helper.PhotoPyaload.payload_list, test_helper.PhotoPyaload.response_list, test_helper.ListingStroge.listing_id):
            
            payload["listing_id"] = listing_id
            response = client.post(
                f"/v2/listing_photos",
                headers={"x-api-key": API_KEY},
                json=payload
            )

            data = self.comman_func(response=response, fields_list=["photo_id"])
            test_helper.ListingStroge.photos_id.append(data.get("photo_id"))
            response_payload["listing_id"] = listing_id
            response_payload["photo_id"] = data.get("photo_id")
            assert data == response_payload

    @pytest.mark.filterwarnings('ignore::RuntimeWarning')
    def test_delete_photos(self):
        
        """ Delete Listing Photos """

        for photo_id in test_helper.ListingStroge.photos_id:

            response = client.delete(
                f"/v2/listing_photos/{photo_id}",
                headers={"x-api-key": API_KEY}
            )

            assert response.status_code == 200, response.text
            data = response.json()
            
            assert "listing_id" in data
            assert "photo_id" in data
            assert response.json() == {
                "photo_id": photo_id,
                "listing_id": data.get("listing_id")
            }
    
    @pytest.mark.filterwarnings('ignore::RuntimeWarning')
    def test_update_listing_status(self):
        
        """ Update Listing Status """

        for listing_id in test_helper.ListingStroge.listing_id:
            response = client.post(
                f"/v2/listing_status/{listing_id}",
                headers={"x-api-key": API_KEY},
                json={
                    "activate": True
                }
            )

            data = self.comman_func(response=response,fields_list=["listing_id"])

            assert data == {
                "listing_id" : listing_id
            }
    
    @pytest.mark.filterwarnings('ignore::RuntimeWarning')
    def test_create_listing_price_rule(self):
        
        """ Create Listing Price Rule """

        for payload , listing_id in zip( test_helper.PriceRulePayload.payload_list, test_helper.ListingStroge.listing_id):
            
            payload["listing_id"] = listing_id
            response = client.post(
                f"/v2/listing_price_rule",
                headers={"x-api-key": API_KEY},
                json=payload
            )

            data = self.comman_func(response=response)
            test_helper.ListingStroge.price_rule_ids.append(data.get("price_rule_id"))

            assert data == {
                "price_rule_id" : str(data.get("price_rule_id"))
            }
    
    @pytest.mark.filterwarnings('ignore::RuntimeWarning')
    def test_delete_listing_price_rule(self):
        
        """ Delete Listing Price Rule """

        for price_rule_id in test_helper.ListingStroge.price_rule_ids:
            response = client.delete(
                f"/v2/listing_price_rule/{price_rule_id}",
                headers={"x-api-key": API_KEY}
            )
            assert response.status_code == 200, response.text
    
    @pytest.mark.filterwarnings('ignore::RuntimeWarning')
    def test_create_discount(self):
        
        """ Create Discount """

        for payload in test_helper.CreateDiscountPayload.payload_list:
            response = client.post(
                f"/v2/discountdetails",
                headers={"x-api-key": API_KEY},
                json=payload
            )

            data = self.comman_func(response=response,fields_list=["discount_id","discount_code"])
            discount_id = data.get("discount_id")
            discount_code = data.get("discount_code")
            test_helper.ListingStroge.discount_ids.append(discount_id)
            test_helper.ListingStroge.discount_codes.append(discount_code)

            assert response.json() == {
                "discount_id" : str(discount_id),
                "discount_code" : discount_code
            }
    
    @pytest.mark.filterwarnings('ignore::RuntimeWarning')
    def test_update_discount(self):

        """ Update Discount """
        for discount_code , payload in zip(test_helper.ListingStroge.discount_codes, test_helper.UpdateDiscountPayload.payload_list):

            payload["discount_code"] = discount_code
            response = client.put(
                f"/v2/discountdetails/{discount_code}",
                headers={"x-api-key": API_KEY},
                json=payload
            )

            data = self.comman_func(response=response, fields_list=["discount_id","discount_code"])
            discount_id = data.get("discount_id")
            discount_code = data.get("discount_code")
            test_helper.ListingStroge.discount_id = discount_id
            test_helper.ListingStroge.discount_code = discount_code

            assert response.json() == {
                "discount_id" : str(discount_id),
                "discount_code" : str(discount_code)
            }

    @pytest.mark.filterwarnings('ignore::RuntimeWarning')
    def test_delete_discount(self):

        """ Delete Discount """

        for discount_code in test_helper.ListingStroge.discount_codes:
            response = client.delete(
                f"/v2/discountdetails/{discount_code}",
                headers={"x-api-key": API_KEY}
            )

            assert response.status_code == 200, response.text

    @pytest.mark.filterwarnings('ignore::RuntimeWarning')
    def test_delete_listing(self):

        """Delete the listing that was created in test_create_listing"""

        for listing_id in test_helper.ListingStroge.listing_id:
            response = client.delete(
                f"/v2/listings/{listing_id}",
                headers={"x-api-key": API_KEY}
            )
            assert response.status_code == 200, response.text
            data = response.json()
            assert "listing_id" in data
            assert response.json() == {
                "listing_id":listing_id
            }

    def test_disconnect_db(self):
        with engine.connect() as default_conn:
            default_conn.execute(f"DROP DATABASE {os.getenv('TEST_DB_SCHEMA', 'test_bkgpal')};")
            default_conn.execute(f"CREATE SCHEMA {os.getenv('TEST_DB_SCHEMA', 'test_bkgpal')};")
