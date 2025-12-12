from fastapi import FastAPI, HTTPException
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from pydantic import BaseModel
from typing import Optional, List
import json
from pathlib import Path

app = FastAPI(title="Beam Health MVP")

DATA_DIR = Path("data")

# ---------- Load Data at Startup ----------

def load_json(filename: str):
    with open(DATA_DIR / filename, "r") as f:
        return json.load(f)

patients = load_json("patients.json")
appointments = load_json("appointments.json")
insurances = load_json("insurances.json")

# ---------- UI ----------
app.mount("/static", StaticFiles(directory="static"), name="static")

@app.get("/")
def serve_ui():
    return FileResponse("static/index.html")


# ---------- Health Check ----------

@app.get("/health")
def health():
    return {"status": "ok"}


# ---------- Request / Response Models ----------

class IntakeRequest(BaseModel):
    first_name: str
    last_name: str
    dob: str
    email: str
    insurance_payer: str
    insurance_plan: str


class EligibilityResponse(BaseModel):
    eligible: bool
    copay: Optional[int] = None
    reason: Optional[str] = None


class IntakeResponse(BaseModel):
    patient_id: int
    eligibility: EligibilityResponse


class BookAppointmentRequest(BaseModel):
    patient_id: int



# ---------- Endpoints ----------
@app.post("/intake", response_model=IntakeResponse)
def intake_patient(request: IntakeRequest):
    # 1. Create patient (in-memory)
    new_patient_id = get_next_patient_id()

    new_patient = {
        "id": new_patient_id,
        "first_name": request.first_name,
        "last_name": request.last_name,
        "dob": request.dob,
        "email": request.email,
        "phone": "",
        "gender": ""
    }

    patients.append(new_patient)

    # 2. Insurance eligibility check
    insurance = find_insurance(
        request.insurance_payer,
        request.insurance_plan
    )

    if not insurance:
        eligibility = EligibilityResponse(
            eligible=False,
            reason="Insurance plan not found"
        )
    elif insurance.get("eligible"):
        eligibility = EligibilityResponse(
            eligible=True,
            copay=insurance.get("coPay")
        )
    else:
        eligibility = EligibilityResponse(
            eligible=False,
            reason=insurance.get("reason", "Not eligible")
        )

    return IntakeResponse(
        patient_id=new_patient_id,
        eligibility=eligibility
    )


@app.get("/appointments/available")
def available_appointments():
    return get_available_appointments()


@app.post("/appointments/{appointment_id}/book")
def book_appointment(appointment_id: int, request: BookAppointmentRequest):
    appointment = next(
        (a for a in appointments if a["id"] == appointment_id),
        None
    )

    if not appointment:
        raise HTTPException(status_code=404, detail="Appointment not found")

    if appointment["status"] != "available":
        raise HTTPException(status_code=400, detail="Appointment not available")

    appointment["status"] = "booked"
    appointment["patient_id"] = request.patient_id

    return {
        "message": "Appointment booked successfully",
        "appointment": appointment
    }




def get_next_patient_id() -> int:
    return max(p["id"] for p in patients) + 1 if patients else 1


def find_insurance(payer: str, plan: str):
    for ins in insurances:
        if ins["payer"] == payer and ins["plan"] == plan:
            return ins
    return None


def get_available_appointments():
    return [
        a for a in appointments
        if a["status"] == "available"
    ]