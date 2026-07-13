# from uuid import uuid4

# from fastapi import FastAPI, Request
# from fastapi.responses import HTMLResponse, JSONResponse
# from fastapi.staticfiles import StaticFiles
# from fastapi.templating import Jinja2Templates
# from pydantic import BaseModel

# from langchain_core.messages import HumanMessage
# l
# # Import LangGraph app
# # from legacy.main import app as travel_graph


# app = FastAPI(title="AI Travel Planner")

# app.mount("/static", StaticFiles(directory="static"), name="static")

# templates = Jinja2Templates(directory="templates")


# @app.get("/", response_class=HTMLResponse)
# async def home(request: Request):

#     return templates.TemplateResponse(
#         request,
#         "index.html",
#         {}
#     )


# # ---------------- Request Model ---------------- #

# class TravelRequest(BaseModel):

#     message: str

#     thread_id: str | None = None


# # ---------------- API ---------------- #

# @app.post("/api/travel")
# async def generate_trip(data: TravelRequest):

#     try:

#         thread_id = data.thread_id or str(uuid4())

#         result = travel_graph.invoke(

#             {

#                 "messages": [

#                     HumanMessage(content=data.message)

#                 ],

#                 "user_query": data.message,

#                 "travel_details": {},

#                 "flight_results": {},

#                 "hotel_results": {},

#                 "itinerary": [],

#                 "estimated_budget": {},

#                 "llm_calls": 0

#             },

#             config={

#                 "configurable": {

#                     "thread_id": thread_id

#                 }

#             }

#         )

#         answer = result["messages"][-1].content

#         return JSONResponse(

#             {

#                 "success": True,

#                 "answer": answer,

#                 "thread_id": thread_id

#             }

#         )

#     except Exception as e:

#         return JSONResponse(

#             {

#                 "success": False,

#                 "error": str(e)

#             },

#             status_code=500

#         )

# latest change
from legacy.graph import travel_graph
from langchain_core.messages import HumanMessage

if __name__ == "__main__":

    config = {
        "configurable": {
            "thread_id": "demo_user"
        }
    }

    while True:

        query = input("\nEnter travel request : ")

        if query.lower() == "exit":
            break

        result = travel_graph.invoke(
            {
                "messages": [
                    HumanMessage(content=query)
                ],
                "user_query": query,
                "travel_details": {},
                "flight_results": {},
                "hotel_results": {},
                "itinerary": [],
                "estimated_budget": {},
                "llm_calls": 0
            },
            config=config
        )

        print("\n")
        print(result["messages"][-1].content)