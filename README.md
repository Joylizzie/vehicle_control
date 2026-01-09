

# 🚀 High-Performance Vehicle Fleet Control

A custom-built, "weaved" IoT management system using **FastAPI**, **PostgreSQL**, and **Vanilla JS**. This project bypasses heavy ORMs to achieve maximum database performance and real-time control of 100+ vehicles.

## 🛠 Tech Stack
- **Backend:** FastAPI (Python)
- **Database:** PostgreSQL (using `psycopg` 3.x)
- **Frontend:** HTML5/CSS3 & Vanilla JavaScript (Fetch API)
- **Automation:** Bash (`run.sh` orchestration)

## 🏁 Features
- **Randomized VIN Generation:** Uses a 17-character alphanumeric generator for realistic simulation.
- **Async DB Connections:** High-concurrency handling using connection pooling.
- **Live Dashboard:** Real-time lock/unlock and engine control via a custom-mounted static frontend.
- **RESTful API:** Clean `PATCH` and `POST` endpoints for state management.

## 🚀 How to Run
1. Create venv: `python3 -m venv venv && source venv/bin/activate`
2. Install dependencies: `pip install fastapi uvicorn psycopg pyyaml`
3. Launch system: `./run.sh`
4. Access dashboard: `http://localhost:8000/static/dashboard.html`

🔗 Quick Access Links

Once the system is running via ./run.sh, you can access the following:
Control Dashboard:http://localhost:8000/static/dashboard.html	The main UI to see and control all vehicles.
Interactive Docs:http://localhost:8000/docs	Full Swagger UI to test POST, PATCH, and GET manually.
Fleet JSON:http://localhost:8000/vehicles	View the raw data for all 100+ random VINs.
Health Check:http://localhost:8000/health	Verify the API and DB connection status.
🛠 Manual Command Examples (For Testing)

Each run the VIN code is randomly generated, visiting the Fleet JSON link first, copying one of the 17-character VINs, and then pasting it into the Docs or your browser URL to test the individual vehicle controls.
1. Check a Specific Vehicle
GET http://localhost:8000/vehicle/{YOUR_RANDOM_VIN}

2. Lock/Unlock (PATCH)
To lock a car manually via URL parameters: PATCH http://localhost:8000/vehicle/{VIN}/lock?locked=true

3. Engine Control (POST)
    If you are using the action-based endpoints:

    Start: POST http://localhost:8000/vehicle/{VIN}/start

    Stop: POST http://localhost:8000/vehicle/{VIN}/stop