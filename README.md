# Vehicle Control API Demo

A backend REST API demo simulating vehicle control commands.  
Designed to demonstrate backend service design, RESTful API principles, and API endpoint management.  

> **Note:** This is a **demo project**. It does **not** connect to real vehicles and is intended for learning and portfolio purposes.

---

## **Features**

- Retrieve vehicle status (engine, fuel level, locked/unlocked)
- Lock and unlock vehicle doors
- Start and stop the vehicle engine (simulated)
- RESTful API endpoints with structured JSON responses
- Service-layer separation for clean backend logic
- Basic error handling (e.g., engine already running/stopped)
- In-memory mock database simulating multiple vehicles

---

## **Tech Stack**

- **Language:** Python 3.x  
- **Framework:** FastAPI  
- **Dependencies:** Pydantic, Uvicorn  
- **Concepts:** REST API, backend service logic, in-memory data store, API error handling

---

## **Installation**

1. Clone the repository:

```bash
git clone https://github.com/Joylizzie/vehicle-control.git
cd vehicle-control
# vehicle_control
