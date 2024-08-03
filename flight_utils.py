from amadeus import Client, ResponseError
import folium


def search_flights(origin_code, destination_code, departure_date, adults):
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
                adults=adults,
                max=3
            )
            print("flights", response.data[0])
            return response.data[:10]
        except Exception as error:
            return None
    else:
        print("Could not get IATA codes for the cities")
        return None


def search_hotel(city_code):
    amadeus = Client(
        client_id='SpBbfoEGAa8jRrbOLqApL6il8ddVoQU0',
        client_secret='rUyAVMUY44pnEyF3'
    )
    try:
        response = amadeus.reference_data.locations.hotels.by_city.get(
            cityCode=city_code)
        # print(response.data[0])
        response = response.data[:30]
        hotels = response
        # Create a map centered around the first hotel
        hotel_map = folium.Map(location=[
            hotels[0]['geoCode']['latitude'], hotels[0]['geoCode']['longitude']], zoom_start=12)
        # Add hotel markers to the map
        for hotel in hotels:
            folium.Marker(
                location=[hotel['geoCode']['latitude'],
                          hotel['geoCode']['longitude']],
                popup=hotel['name']
            ).add_to(hotel_map)

        hotel_map.save('hotel_map.html')
        return response, hotel_map
    except ResponseError as error:
        print(f"An error occurred: {error}")
        raise error


if __name__ == "__main__":
    print(search_hotel("NYC"))
