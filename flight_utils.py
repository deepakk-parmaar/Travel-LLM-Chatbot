from amadeus import Client, ResponseError
from amadeus import Location
# Initialize the Amadeus Client
def search_flights(origin_code, destination_code, departure_date,adults):
    amadeus = Client(
        client_id='SpBbfoEGAa8jRrbOLqApL6il8ddVoQU0',
        client_secret='rUyAVMUY44pnEyF3'
    )
    if origin_code and destination_code:
        try:
            response = amadeus.shopping.flight_offers_search.get(
                originLocationCode=origin_code,
                destinationLocationCode=destination_code,
                departureDate=departure_date,
                adults=adults
            )
            return response.data
        except ResponseError as error:
            print(f"An error occurred: {error}")
            return None
    else:
        print("Could not get IATA codes for the cities")
        return None

def book_flight(flight_offer, traveler_info):
    amadeus = Client(
        client_id='SpBbfoEGAa8jRrbOLqApL6il8ddVoQU0',
        client_secret='rUyAVMUY44pnEyF3'
    )
    try:
        # Price the flight offer to get the final price
        price_response = amadeus.shopping.flight_offers.pricing.post(
            flight_offer)
        priced_flight_offer = price_response.data

        # Book the flight offer
        booking_response = amadeus.booking.flight_orders.post(
            {
                'type': 'flight-order',
                'flightOffers': [priced_flight_offer],
                'travelers': traveler_info
            }
        )
        return booking_response.data
    except ResponseError as error:
        print(f"An error occurred: {error}")
        return None
    # Example traveler information
    traveler_info = [
        {
            "id": "1",
            "dateOfBirth": "1980-01-01",
            "name": {
                "firstName": "John",
                "lastName": "Doe"
            },
            "gender": "MALE",
            "contact": {
                "emailAddress": "john.doe@example.com",
                "phones": [
                    {
                        "deviceType": "MOBILE",
                        "countryCallingCode": "1",
                        "number": "1234567890"
                    }
                ]
            },
            "documents": [
                {
                    "documentType": "PASSPORT",
                    "birthPlace": "Madrid",
                    "issuanceLocation": "Madrid",
                    "issuanceDate": "2015-04-14",
                    "number": "00000000",
                    "expiryDate": "2025-04-14",
                    "issuanceCountry": "ES",
                    "validityCountry": "ES",
                    "nationality": "ES",
                    "holder": True
                }
            ]
        }
    ]
