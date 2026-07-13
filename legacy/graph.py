import os
import operator
import psycopg
import json
import re
from typing import TypedDict, Annotated

from langgraph.graph import StateGraph, START, END
from langgraph.checkpoint.postgres import PostgresSaver


from langchain_core.messages import (
    AnyMessage,
    HumanMessage,
    AIMessage,
    SystemMessage,
)

from langchain_groq import ChatGroq
# from tools.tavily_tool import tavily_search
from tools.flight_tool import search_flights
from tools.hotel_tool import search_hotels
from tools.itinerary_tool import generate_itinerary
from dotenv import load_dotenv
load_dotenv()
llm = ChatGroq(
    model="llama-3.3-70b-versatile"
)
DATABASE_URL = os.getenv("DATABASE_URL")

# State
# class TravelState(TypedDict):
#     messages: Annotated[list[AnyMessage], operator.add]
#     user_query: str
#     travel_details: dict  
#     flight_results: str
#     hotel_results: str
#     itinerary: str
#     llm_calls: int
class TravelState(TypedDict):
    messages: Annotated[list[AnyMessage], operator.add]
    user_query: str
    travel_details: dict
    flight_results: dict
    hotel_results: dict
    itinerary: list
    estimated_budget: dict
    llm_calls: int
#travel understanding agent
def travel_understanding_agent(state: TravelState):

    prompt = f"""
You are an AI travel information extraction assistant.

Extract the travel information from the user's request.

Return ONLY valid JSON.

Schema:

{{
    "source_city": null,
    "source_airport": null,

    "destination_city": null,
    "destination_airport": null,

    "start_date": null,
    "end_date": null,
    "duration": null,
    "budget": null,
    "budget_provided": false,
    "travelers": 1
}}

Rules:

- Convert airport names into IATA airport codes.
- Example:
  Delhi -> DEL
  Mumbai -> BOM
  Jaipur -> JAI
  Dubai -> DXB
  Bali -> DPS
  London -> LHR
  New York -> JFK

- Convert dates into YYYY-MM-DD format.
- If the user provides a budget:
    set
    "budget_provided": true
- If the user does NOT mention any budget:
    keep
    "budget": null
    "budget_provided": false
- Return ONLY JSON.
User Request:
{state["user_query"]}
"""

    response = llm.invoke([
        HumanMessage(content=prompt)
    ])

    try:
        content = response.content.strip()

        # Remove Markdown code fences if present
        content = re.sub(
            r"^```json\s*|\s*```$",
            "",
            content,
            flags=re.MULTILINE
        ).strip()

        travel_details = json.loads(content)

        AIRPORT_CODES = {
            "Delhi": "DEL",
            "Mumbai": "BOM",
            "Jaipur": "JAI",
            "Goa": "GOI",
            "Bangalore": "BLR",
            "Bengaluru": "BLR",
            "Hyderabad": "HYD",
            "Chennai": "MAA",
            "Kolkata": "CCU",
            "Ahmedabad": "AMD",
            "Pune": "PNQ",
            "Kochi": "COK",
            "Dubai": "DXB",
            "Singapore": "SIN",
            "Bangkok": "BKK",
            "Bali": "DPS",
            "Tokyo": "HND",
            "Seoul": "ICN",
            "London": "LHR",
            "New York": "JFK"
        }

        if not travel_details.get("source_airport"):
            travel_details["source_airport"] = AIRPORT_CODES.get(
                travel_details.get("source_city")
            )

        if not travel_details.get("destination_airport"):
            travel_details["destination_airport"] = AIRPORT_CODES.get(
                travel_details.get("destination_city")
            )

        travel_details.setdefault("budget", None)
        travel_details.setdefault("budget_provided", False)
        travel_details.setdefault("travelers", 1)

    except Exception:
        travel_details = {}

    print("\n========== TRAVEL DETAILS ==========")
    print(travel_details)
    print("====================================\n")

    return {
        "travel_details": travel_details,
        "messages": [
            AIMessage(content="Travel details extracted.")
        ],
        "llm_calls": state.get("llm_calls", 0) + 1
    }
# Flight Agent
# def flight_agent(state: TravelState):
#     details = state["travel_details"]
#     query = (
#          f"{details.get('source')} to "
#          f"{details.get('destination')} "
#          f"on {details.get('start_date')}"
#     )
#     flight_data = search_flights(query)
#     return {
#         "flight_results": flight_data,
#         "messages": [
#             AIMessage(content=f"Flight results fetched")
#         ],
#         "llm_calls": state.get("llm_calls", 0) + 1
#     }
# Flight Agent
def flight_agent(state: TravelState):
    details = state["travel_details"]
    flight_data = search_flights(details)
    print("\n========== FLIGHTS ==========")
    print(flight_data)
    print("=============================\n")
    return {
        "flight_results": flight_data,
        "messages": [
            AIMessage(content="Flight results fetched")
        ],
        "llm_calls": state.get("llm_calls", 0) + 1
    }

# Hotel Agent
# Hotel Agent
def hotel_agent(state: TravelState):

    details = state["travel_details"]

    hotel_results = search_hotels(details)

    print("\n========== HOTELS ==========")
    print(hotel_results)
    print("================================\n")

    return {
        "hotel_results": hotel_results,
        "messages": [
            AIMessage(content="Hotel information fetched")
        ],
        "llm_calls": state.get("llm_calls", 0) + 1
    }

# Itinerary Agent
def itinerary_agent(state: TravelState):

    itinerary = generate_itinerary(
        state["travel_details"],
        state["flight_results"],
        state["hotel_results"]
    )

    # return {

    #     "itinerary": itinerary,

    #     "messages": [
    #         AIMessage(content="Itinerary generated.")
    #     ],

    #     "llm_calls": state.get("llm_calls", 0) + 1

    # }
    return {

        "itinerary": itinerary["plan"],

        "estimated_budget": itinerary["estimated_budget"],

        "messages": [

            AIMessage(
                content="Itinerary generated."
            )

        ],

        "llm_calls":
            state.get("llm_calls", 0) + 1

    }

# Final Response Agent
# ---------------- Final Response Agent ---------------- #

def final_agent(state: TravelState):

    details = state["travel_details"]

    budget = state["estimated_budget"]

    destination = details["destination_city"]

    prompt = f"""
You are an Proffesional AI Travel Assistant.

Flights, hotels and itinerary have ALREADY been generated.

DO NOT regenerate them.

DO NOT repeat them.

Generate ONLY the following sections in markdown.

# ✨ Trip Overview

Write 2-3 lines summarizing the trip to {destination}.

# 💰 Budget Analysis

Estimated Cost : ₹{budget["estimated_total"]}

User Budget : ₹{budget["user_budget"]}

Is Trip Within Budget :
{"Yes" if budget["within_budget"] else "No"}

If under budget,
mention remaining amount.

If over budget,
mention exceeded amount.

# 💡 Travel Tips

Give exactly 5 destination-specific tips.

# 🎒 Packing Suggestions

Give exactly 5 bullet points.

# 🚇 Local Transport

Explain the best way to travel inside {destination}.

Mention metro/bus/taxi etc.

# 🌦 Weather

Briefly mention expected weather.

# 📱 Emergency Information

Mention

• emergency number

• useful local apps

• currency

• visa requirement (if any)

Return ONLY markdown.

Never repeat

- flights
- hotels
- itinerary
- user details

Dont create hallucination results .
"""

    response = llm.invoke(

        [

            SystemMessage(

                content="You are an expert travel advisor."

            ),

            HumanMessage(content=prompt)

        ]

    )

    return {

        "messages": [response],

        "llm_calls": state.get("llm_calls", 0) + 1

    }
graph = StateGraph(TravelState)
graph.add_node(
    "travel_understanding_agent",
    travel_understanding_agent
)
graph.add_node("flight_agent", flight_agent)
graph.add_node("hotel_agent", hotel_agent)
graph.add_node("itinerary_agent", itinerary_agent)
graph.add_node("final_agent", final_agent)

graph.add_edge( START,"travel_understanding_agent")
graph.add_edge("travel_understanding_agent","flight_agent")
graph.add_edge("flight_agent", "hotel_agent")
graph.add_edge("hotel_agent", "itinerary_agent")
graph.add_edge("itinerary_agent", "final_agent")
graph.add_edge("final_agent", END)

##memory 
_conn = psycopg.connect(DATABASE_URL.replace("postgresql+psycopg://", "postgresql://"),autocommit=True)
checkpointer = PostgresSaver(_conn)
checkpointer.setup()
#compile graph
# app tha idhr phle travel_graph ki jgh
travel_graph = graph.compile(checkpointer=checkpointer)

if __name__ == "__main__":
    config = {
        "configurable": {
            "thread_id": "user_mohit"
        }
    }

    user_input = input("Enter travel request: ")

    result = travel_graph.invoke(
        {
            "messages": [
                HumanMessage(content=user_input)
            ],
            "user_query": user_input,
            "travel_details": {},
            "flight_results": {},
            "hotel_results": {},
            "itinerary": [],
            "llm_calls": 0
        },
        config=config
    )

    print("\nFINAL RESPONSE:\n")

    # for msg in result["messages"]:
    #     print(msg.content)
    print("\nFINAL RESPONSE:\n")
    print(result["messages"][-1].content)
