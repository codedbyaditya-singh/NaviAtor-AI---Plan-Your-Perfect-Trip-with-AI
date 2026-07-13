from uuid import uuid4

from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from pydantic import BaseModel
from langchain_core.messages import HumanMessage

from legacy.graph import travel_graph
# from app.routers.auth import router as auth_router 9/1:45
# from app.database.database import engine

app = FastAPI(title="AI Travel Planner")
# app.include_router(auth_router) 9/1:45

app.mount("/static", StaticFiles(directory="static"), name="static")

templates = Jinja2Templates(directory="templates")


@app.get("/", response_class=HTMLResponse)
async def home(request: Request):
    return templates.TemplateResponse(
        request,
        "index.html",
        {}
    )


class TravelRequest(BaseModel):
    message: str
    thread_id: str | None = None


@app.post("/api/travel")
async def generate_trip(data: TravelRequest):
    thread_id = data.thread_id or str(uuid4())

    result = travel_graph.invoke(
        {
            "messages": [HumanMessage(content=data.message)],
            "user_query": data.message,
            "travel_details": {},
            "flight_results": {},
            "hotel_results": {},
            "itinerary": [],
            "estimated_budget": {},
            "llm_calls": 0,
        },
        config={"configurable": {"thread_id": thread_id}},
    )

    return JSONResponse(
        {
            "success": True,
            "thread_id": thread_id,
            "travel_details": result["travel_details"],
            "flights": result["flight_results"].get("recommended", []),
            "hotels": result["hotel_results"].get("recommended", []),
            "itinerary": result["itinerary"],
            "estimated_budget": result.get("estimated_budget", {}),
            "summary": result["messages"][-1].content,
        }
    )