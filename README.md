# 🌍 NaviAtor – AI: Plan Your Perfect Trip with AI 

🚧 Project Status: Active Development
This project is currently under active development. New features, workflow improvements, API integrations, and architectural enhancements are being added regularly.

# 📖 Overview

NaviAtor is an AI-powered travel planning application designed to simplify trip planning through intelligent automation. Instead of manually searching across multiple websites, users can describe their travel requirements in natural language, and the system generates a personalized travel plan by combining Large Language Models (LLMs), external APIs, and structured workflows.

The project is being built with a modular backend architecture using FastAPI, LangGraph, and PostgreSQL, enabling scalable AI agents and seamless integration with real-time travel services.

⸻

# ✨ Features

* 🤖 AI-powered travel planning using Large Language Models
* 🧠 Intelligent extraction of user preferences (destination, budget, duration, travelers, travel dates, etc.)
* 🗺️ Personalized itinerary generation
* ✈️ Flight recommendation integration
* 🏨 Hotel recommendation integration
* 🌦️ Weather information support
* 🔍 Destination information and travel insights
* 🔐 JWT-based user authentication
* 🗄️ PostgreSQL database integration
* ⚡ Modular FastAPI backend architecture
* 🔄 LangGraph-based agent workflow orchestration

⸻

# 🏗️ System Workflow

The application follows a modular AI workflow:

1. User submits a travel request in natural language.
2. The system extracts structured travel details such as:
    * Destination
    * Budget
    * Travel dates
    * Number of travelers
    * Trip duration
3. Specialized AI agents process different parts of the request.
4. External APIs retrieve travel-related information.
5. Retrieved information is combined with LLM reasoning.
6. A personalized travel itinerary is generated for the user.

⸻

# 🧩 Project Structure

```text
app/
├── agents/
├── auth/
├── core/
├── database/
├── dependencies/
├── models/
├── routers/
├── schemas/
├── services/
└── utils/
tools/
├── flight_tool.py
├── hotel_tool.py
├── itinerary_tool.py
└── tavily_tool.py
templates/
static/
```
⸻

# 🛠️ Tech Stack

Backend

* Python
* FastAPI
* Pydantic
* SQLAlchemy
* PostgreSQL

AI & LLM

* LangChain
* LangGraph
* Groq LLM
* Google Gemini
* Prompt Engineering

APIs

* Tavily Search API
* Flight Information APIs
* Hotel Information APIs
* Weather APIs (ongoing integration)

Frontend

* HTML
* CSS
* JavaScript
* Jinja2 Templates

Authentication

* JWT Authentication
* Passlib
* BCrypt

⸻

# 🎯 Project Objectives

The primary goal of NaviAtor is to build an intelligent travel assistant capable of:

* Understanding natural language travel requests
* Reducing manual trip planning effort
* Providing personalized recommendations
* Combining AI reasoning with real-world information
* Demonstrating a scalable multi-agent AI architecture

⸻

# 🚀 Current Development

The project is actively evolving with continuous improvements, including:

* Improved AI agent collaboration
* Better itinerary generation
* Enhanced API integrations
* Reduced LLM hallucinations through structured retrieval
* Database optimization
* Authentication enhancements
* Improved frontend experience
* Performance optimization

⸻

# 📌 Future Roadmap

* Multi-city trip planning
* Interactive travel chatbot
* Maps integration
* Budget optimization
* Train and bus recommendations
* Hotel booking integration
* Flight booking integration
* Travel document assistance
* User travel history
* Saved itineraries
* Email itinerary export
* PDF itinerary generation

⸻

# 💻 Installation

Clone the repository:

git clone https://github.com/codedbyaditya-singh/NaviAtor-AI---Plan-Your-Perfect-Trip-with-AI.git

Navigate to the project:

cd NaviAtor-AI---Plan-Your-Perfect-Trip-with-AI

Create and activate a virtual environment:

python -m venv travel_agent
# macOS / Linux
source travel_agent/bin/activate

Install dependencies:

pip install -r requirements.txt

Run the FastAPI application:

uvicorn app.main:app --reload

⸻

# 🤝 Contributions

This repository is currently maintained as a personal learning and development project. Suggestions, feedback, and ideas for improvement are always welcome.

⸻

# 👨‍💻 Author

Aditya Singh

B.Tech – Computer Science & Engineering (Artificial Intelligence)

Building AI-powered applications with a focus on Machine Learning, Generative AI, and intelligent software systems.
