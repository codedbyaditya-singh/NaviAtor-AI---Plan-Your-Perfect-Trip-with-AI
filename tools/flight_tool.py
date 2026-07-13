# import os
# import requests
# from dotenv import load_dotenv
# load_dotenv()
# API_KEY = os.getenv("AVIATIONSTACK_API_KEY")

# def search_flights(query):

#     url = "http://api.aviationstack.com/v1/flights"

#     params = {
#         "access_key": API_KEY,
#         "limit": 5
#     }

#     response = requests.get(url, params=params)
#     data =response.json()
#     flights =[]
#     if "data" in data:
#         for flight in data["data"][:5]:
#             airline = flight.get("airline",{}).get("name","unkown")
#             departure = flight.get(
#                 "departure", {}
#             ).get("airport", "Unknown")

#             arrival = flight.get(
#                 "arrival", {}
#             ).get("airport", "Unknown")

#             status = flight.get("flight_status", "Unknown")

#             flights.append(
#                 f"""
# Airline: {airline}
# Departure: {departure}
# Arrival: {arrival}
# Status: {status}
# """
#             )

#     return "\n".join(flights)

import os

from serpapi import GoogleSearch
# from datetime import datetime
from dotenv import load_dotenv

load_dotenv()

SERPAPI_KEY = os.getenv("SERPAPI_KEY")


def search_flights(travel_details):

    params = {
        "engine": "google_flights",
        "departure_id": travel_details["source_airport"],
        "arrival_id": travel_details["destination_airport"],
        "outbound_date": travel_details["start_date"],
        "type": "2",
        "adults": travel_details.get("travelers", 1),
        "travel_class": "1",
        "hl": "en",
        "gl": "in",
        "currency": "INR",
        "deep_search": "true",
        "api_key": SERPAPI_KEY
    }

    search = GoogleSearch(params)
    results = search.get_dict()

    all_flights = (
        results.get("best_flights", [])
        + results.get("other_flights", [])
    )

    parsed_flights = []

    for flight in all_flights:

        first_leg = flight["flights"][0]
        last_leg = flight["flights"][-1]

        layovers = []

        if "layovers" in flight:
            layovers = [
                stop["name"]
                for stop in flight["layovers"]
            ]

        parsed_flights.append({

            "airline": first_leg.get("airline"),

            "flight_number": first_leg.get("flight_number"),

            "departure_airport":
                first_leg["departure_airport"]["name"],

            "departure_code":
                first_leg["departure_airport"]["id"],

            "departure_time":
                first_leg["departure_airport"]["time"],

            "arrival_airport":
                last_leg["arrival_airport"]["name"],

            "arrival_code":
                last_leg["arrival_airport"]["id"],

            "arrival_time":
                last_leg["arrival_airport"]["time"],

            "duration":
                flight.get("total_duration"),

            "price":
                flight.get("price"),

            "type":
                flight.get("type"),

            "stops":
                len(flight["flights"]) - 1,

            "layovers":
                layovers,

            "carbon":
                flight.get("carbon_emissions", {}),
            "booking_link":

                f"https://www.google.com/travel/flights?hl=en#flt="

                f"{travel_details['source_airport']}."

                f"{travel_details['destination_airport']}."

                f"{travel_details['start_date']}"
        })

    # ---------------- Remove Duplicates ---------------- #

    unique = {}

    for flight in parsed_flights:

        key = (

            flight["airline"],

            flight["flight_number"],

            flight["departure_time"],

            flight["arrival_time"]

        )

        if key not in unique:
            unique[key] = flight

    parsed_flights = list(unique.values())

    # ---------------- Budget Filter ---------------- #

    budget = travel_details.get("budget")

    if budget is not None:

        budget_per_person = budget / travel_details.get(
            "travelers",
            1
        )

        within_budget = [

            f for f in parsed_flights

            if f["price"] <= budget_per_person

        ]

        if within_budget:
            parsed_flights = within_budget
        else:

            parsed_flights.sort(

                key=lambda x: (

                    x["stops"],

                    x["duration"],

                    x["price"]

                )
        
            )

    # ---------------- Rankings ---------------- #
    if not parsed_flights:
        return {
          "recommended": [],
          "summary": {
               "total_flights": 0,
                "lowest_price": None
           }
        }     
    cheapest = min(
        parsed_flights,
        key=lambda x: x["price"]
    )

    fastest = min(
        parsed_flights,
        key=lambda x: x["duration"]
    )

    eco = min(
        parsed_flights,
        key=lambda x: x["carbon"].get(
            "this_flight",
            float("inf")
        )
    )

    best_value = min(

        parsed_flights,

        key=lambda x:

        x["price"]

        +

        (x["duration"] * 10)

        +

        (x["stops"] * 5000)

    )

    recommended = []

    seen = set()

    for flight in [

        cheapest,

        fastest,

        best_value,

        eco

    ]:

        key = (

            flight["flight_number"],

            flight["departure_time"]

        )

        if key not in seen:

            recommended.append(flight)

            seen.add(key)

    summary = {

        "total_flights": len(parsed_flights),

        "lowest_price": cheapest["price"],
        "budget_provided":
            travel_details.get(
               "budget_provided",
               False
            )
    }

    print("\n========== FLIGHT SUMMARY ==========")

    print(summary)

    print()

    for i, flight in enumerate(recommended, start=1):

        print(f"{i}. {flight['airline']}")

        print(
            f"   Flight : {flight['flight_number']}"
        )

        print(
            f"   Route  : {flight['departure_code']} → {flight['arrival_code']}"
        )

        print(
            f"   Price  : ₹{flight['price']}"
        )

        print(
            f"   Stops  : {flight['stops']}"
        )

        print(
            f"   Duration : {flight['duration']} mins"
        )

        print()

    print("====================================\n")

    return {

        "recommended": recommended,

        "summary": summary

    }