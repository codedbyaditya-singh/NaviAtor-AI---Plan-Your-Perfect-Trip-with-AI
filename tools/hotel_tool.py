import os
import re

from serpapi import GoogleSearch
from dotenv import load_dotenv

load_dotenv()

SERPAPI_KEY = os.getenv("SERPAPI_KEY")


def parse_price(price):

    if price is None:
        return None

    if isinstance(price, (int, float)):
        return float(price)

    if isinstance(price, str):

        price = re.sub(r"[^\d.]", "", price)

        if price == "":
            return None

        try:
            return float(price)
        except:
            return None

    return None


def search_hotels(travel_details):

    params = {
        "engine": "google_hotels",
        "q": travel_details["destination_city"],
        "check_in_date": travel_details["start_date"],
        "check_out_date": travel_details["end_date"],
        "adults": travel_details.get("travelers", 1),
        "currency": "INR",
        "gl": "in",
        "hl": "en",
        "api_key": SERPAPI_KEY
    }

    search = GoogleSearch(params)

    results = search.get_dict()

    properties = results.get("properties", [])

    nights = travel_details.get("duration") or 1

    hotels = []

    for hotel in properties:

        price = None

        if hotel.get("rate_per_night"):
            price = hotel["rate_per_night"].get("lowest")

        elif hotel.get("total_rate"):
            price = hotel["total_rate"].get("lowest")

        price = parse_price(price)

        if price is None:
            continue

        amenities = hotel.get("amenities", [])

        if not isinstance(amenities, list):
            amenities = []

        gps = hotel.get("gps_coordinates", {})

        hotels.append({

            "hotel_name":
                hotel.get("name", "Unknown"),

            "price_per_night":
                price,

            "total_price":
                round(price * nights, 2),

            "rating":
                float(hotel.get("overall_rating") or 0),

            "reviews":
                hotel.get("reviews", 0),

            "booking_link":
                hotel.get("link"),

            "type":
                hotel.get("type"),

            "address":
                hotel.get("gps_coordinates", {}).get("name")
                or hotel.get("address")
                or "Unknown",

            "latitude":
                gps.get("latitude"),

            "longitude":
                gps.get("longitude"),

            "amenities":
                amenities[:6]

        })

    # ---------------- Remove Duplicates ---------------- #

    unique = {}

    for hotel in hotels:

        unique[hotel["hotel_name"]] = hotel

    hotels = list(unique.values())

    # ---------------- Budget Filter ---------------- #

    budget = travel_details.get("budget")

    if budget is not None:

        hotel_budget = budget * 0.40

        filtered = [

            h

            for h in hotels

            if h["total_price"] <= hotel_budget

        ]

        if filtered:
            hotels = filtered

        else:

            hotels.sort(

                key=lambda h: (

                    -h["rating"],

                    h["price_per_night"]

                )

            )

    # ---------------- Sort ---------------- #
    if not hotels:

        return {

            "recommended": [],

            "summary": {

                "total_hotels": 0,

                "lowest_price": None

            }

        }
    hotels.sort(

        key=lambda h: (

            -h["rating"],

            h["price_per_night"]

        )

    )

    recommended = hotels[:5]

    summary = {

        "total_hotels": len(hotels),

        "lowest_price":

            min(

                h["price_per_night"]

                for h in hotels

            ), 
        "budget_provided":

           travel_details.get(

               "budget_provided",

              False

            )

    }

    print("\n========== HOTEL SUMMARY ==========")
    print(summary)
    print()

    for i, hotel in enumerate(recommended, start=1):

        print(f"{i}. {hotel['hotel_name']}")
        print(f"   ⭐ Rating : {hotel['rating']}")
        print(f"   💰 ₹{hotel['price_per_night']:.0f} / night")
        print(f"   🏨 Total Stay : ₹{hotel['total_price']:.0f}")
        print(f"   📍 {hotel['address']}")

        if hotel["amenities"]:
            print(
                f"   🛎 Amenities : {', '.join(hotel['amenities'])}"
            )

        print()

    print("===================================\n")

    return {

        "recommended": recommended,

        "summary": summary

    }