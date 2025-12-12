# Beam Health MVP – Patient Acquisition & Scheduling

## Overview
This project is a small MVP demonstrating an end-to-end **patient acquisition, insurance eligibility, and scheduling workflow** inspired by Beam Health’s product themes: automation, connected workflows, reduced clicks, and clinician enablement.

The goal is to show how data typically received from an EMR system can be orchestrated into a streamlined experience that minimizes administrative overhead while surfacing clear next actions.

---

## Feature Implemented
**Automated Patient Intake with Real-Time Insurance Eligibility and Smart Scheduling**

The MVP focuses on:
- Automating insurance eligibility checks at intake time
- Reducing manual decision-making for clinic staff
- Connecting intake, eligibility, and scheduling into a single workflow

---

## Demo Flow
1. **Patient Intake**
    - A new patient enters basic demographic and insurance information.
    - The system creates the patient in memory and immediately evaluates insurance eligibility.

2. **Insurance Eligibility Automation**
    - Eligibility is determined using payer and plan data.
    - If eligible, an estimated copay is shown.
    - If not eligible, a clear reason is displayed.

3. **Smart Scheduling**
    - Eligible patients are shown only available appointment slots.
    - Booking a slot updates the appointment status and links it to the patient.

4. **Confirmation**
    - The appointment is confirmed with minimal user interaction.

---

## Data Sources
The application uses JSON files to simulate EMR-provided data:
- `patients.json`
- `appointments.json`
- `insurances.json`

All data is loaded at application startup and managed in memory for simplicity.

---

## Assumptions & Design Decisions
- JSON files represent upstream EMR or payer system feeds.
- Newly acquired patients are stored in memory for the session duration.
- Data persistence is intentionally omitted to keep the MVP focused on workflow automation.
- Each patient has a single active insurance plan.
- No authentication or authorization is required.

---

## Tech Stack
- **Backend:** Python, FastAPI
- **Frontend:** HTML, CSS, Vanilla JavaScript
- **Data Storage:** JSON files (no database)
---

## How to Run

### 1. Install dependencies
```bash
pip install fastapi uvicorn
```

### 2. Start the server
```bash
uvicorn main:app --reload
```

### 3. Access the app
- UI: http://127.0.0.1:8000
- API Docs: http://127.0.0.1:8000/docs
