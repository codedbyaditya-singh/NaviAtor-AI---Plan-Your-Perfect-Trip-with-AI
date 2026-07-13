# from datetime import datetime, timedelta


# def generate_itinerary(
#     travel_details,
#     flight_data,
#     hotel_data
# ):

#     start_date = datetime.strptime(
#         travel_details["start_date"],
#         "%Y-%m-%d"
#     )

#     duration = travel_details.get("duration", 3)

#     destination = travel_details["destination_city"]

#     budget = travel_details.get("budget")

#     hotels = hotel_data.get("recommended", [])

#     flights = flight_data.get("recommended", [])

#     hotel = hotels[0] if hotels else None

#     flight = flights[0] if flights else None

#     hotel_area = hotel["hotel_name"] if hotel else "your hotel"

#     itinerary = []

#     for day in range(duration):

#         current_date = (
#             start_date +
#             timedelta(days=day)
#         ).strftime("%d %b %Y")

#         # ---------------- Day 1 ---------------- #

#         if day == 0:

#             activities = [

#                 {
#                     "time": "Arrival",

#                     "activity":
#                     f"Arrive at {destination}"

#                 },

#                 {
#                     "time": "Morning / Afternoon",

#                     "activity":
#                     f"Check in at {hotel_area}"

#                 },

#                 {
#                     "time": "Evening",

#                     "activity":
#                     "Explore attractions close to the hotel. Keep the first day relaxed."
#                 }

#             ]

#         # ---------------- Last Day ---------------- #

#         elif day == duration - 1:

#             activities = [

#                 {
#                     "time": "Morning",

#                     "activity":
#                     "Breakfast and check-out"
#                 },

#                 {
#                     "time": "Before Flight",

#                     "activity":
#                     "Visit any nearby place if time permits."
#                 },

#                 {
#                     "time": "Departure",

#                     "activity":
#                     "Leave for the airport."
#                 }

#             ]

#         # ---------------- Middle Days ---------------- #

#         else:

#             activities = [

#                 {
#                     "time": "Morning",

#                     "activity":
#                     f"Visit one of the major attractions in {destination}."
#                 },

#                 {
#                     "time": "Afternoon",

#                     "activity":
#                     "Lunch and nearby sightseeing."
#                 },

#                 {
#                     "time": "Evening",

#                     "activity":
#                     "Explore markets, cafés or sunset viewpoints near your hotel."
#                 }

#             ]

#         itinerary.append(

#             {

#                 "day": day + 1,

#                 "date": current_date,

#                 "activities": activities

#             }

#         )

#     # ---------------- Estimated Budget ---------------- #

#     estimated_budget = {}

#     if hotel:

#         hotel_cost = hotel["total_price"]

#     else:

#         hotel_cost = 0

#     if flight:

#         flight_cost = (
#             flight["price"]
#             *
#             travel_details.get("travelers", 1)
#         )

#     else:

#         flight_cost = 0

#     food = (
#         1500
#         *
#         duration
#         *
#         travel_details.get("travelers", 1)
#     )

#     transport = (
#         700
#         *
#         duration
#     )

#     sightseeing = (
#         1000
#         *
#         duration
#         *
#         travel_details.get("travelers", 1)
#     )

#     miscellaneous = 3000

#     total = (

#         flight_cost

#         + hotel_cost

#         + food

#         + transport

#         + sightseeing

#         + miscellaneous

#     )

#     estimated_budget = {

#         "flight": flight_cost,

#         "hotel": hotel_cost,

#         "food": food,

#         "transport": transport,

#         "sightseeing": sightseeing,

#         "miscellaneous": miscellaneous,

#         "estimated_total": total,

#         "user_budget": budget,

#         "within_budget":

#             budget is None

#             or

#             total <= budget

#     }

#     return {

#         "plan": itinerary,

#         "estimated_budget": estimated_budget

#     }

# last change
from langchain_groq import ChatGroq
from langchain_core.messages import HumanMessage
from dotenv import load_dotenv
import os

load_dotenv()

llm = ChatGroq(
    model="llama-3.3-70b-versatile"
)


def generate_itinerary(
    travel_details,
    flight_data,
    hotel_data
):

    destination = travel_details["destination_city"]
    duration = travel_details["duration"]
    travelers = travel_details.get("travelers", 1)

    hotel = None
    if hotel_data.get("recommended"):
        hotel = hotel_data["recommended"][0]

    flight = None
    if flight_data.get("recommended"):
        flight = flight_data["recommended"][0]

    hotel_name = hotel["hotel_name"] if hotel else None
    

    flight_info = ""

    if flight:
        flight_info = f"""
Airline : {flight["airline"]}

Flight : {flight["flight_number"]}

Departure :
{flight["departure_time"]}

Arrival :
{flight["arrival_time"]}

Airport :
{flight["departure_airport"]}

Destination Airport :
{flight["arrival_airport"]}
"""

    prompt = f"""
You are a professional travel planner.

Create a COMPLETE day-wise itinerary.

Destination:
{destination}

Trip Duration:
{duration} days

Travelers:
{travelers}

Hotel:
{hotel_name if hotel_name else "Not Selected"}

Flight:
{flight_info}

Rules:

Generate exactly {duration} days.

For EVERY day include

Morning

Afternoon

Evening

Night

Mention:

• famous attractions

• opening timings

• approximate ticket prices

• travelling time

• nearby restaurants

• transport suggestion

• shopping if applicable

Day 1 should include

Airport arrival

Hotel check-in

Nearby attractions

Dinner

Last day should include

Breakfast

Checkout

Airport departure

Return ONLY markdown.

Example format:

# Day 1

🌅 Morning

Reach Dubai Airport at 11:00 AM

Taxi to hotel (35 mins)

🏨 Check-in at hotel

🍽 Lunch

Al Mallah Restaurant

₹1200

🌇 Evening

Dubai Marina Walk

5 PM – 11 PM

Free Entry

🍽 Dinner

Pier 7

Night

Return Hotel

Continue similarly till Day {duration}.
IMPORTANT

If hotel is "Not Selected"

DO NOT invent a hotel.

Write

"Check in at your selected hotel."

If flight information is missing

DO NOT invent flight timings.

Simply say

"Arrive at destination."
"""

    response = llm.invoke([
        HumanMessage(content=prompt)
    ])

    estimated_budget = {}

    hotel_cost = (
        hotel["total_price"]
        if hotel
        else 0
    )

    flight_cost = (
        flight["price"] * travelers
        if flight
        else 0
    )

    food = 1500 * duration * travelers

    transport = 700 * duration

    sightseeing = 1000 * duration * travelers

    miscellaneous = 3000

    total = (
        hotel_cost
        + flight_cost
        + food
        + transport
        + sightseeing
        + miscellaneous
    )

    estimated_budget = {

        "flight": flight_cost,

        "hotel": hotel_cost,

        "food": food,

        "transport": transport,

        "sightseeing": sightseeing,

        "miscellaneous": miscellaneous,

        "estimated_total": total,

        "user_budget": travel_details.get("budget"),

        "within_budget":
        travel_details.get("budget") is None
        or
        total <= travel_details.get("budget")
    }

    return {

        "plan": response.content,

        "estimated_budget": estimated_budget

    }