from server.app.api.projects import router as projects_router
from fastapi import FastAPI
from pydantic import BaseModel
import pandas as pd
import joblib


app = FastAPI(
    title="Infra Gati API",
    description="Predictive analytics API for land acquisition delays",
    version="1.0.0"
)
app.include_router(projects_router)

# Load the trained ML model
model = joblib.load(
    "server/app/ml_models/delay_risk_model.joblib"
)


# -----------------------------------
# Input structure
# -----------------------------------

class ProjectData(BaseModel):
    state: str
    district: str
    latitude: float
    longitude: float
    project_type: str
    land_area: float
    project_cost: float
    affected_families: int
    landowners: int
    rehabilitation_required: int
    rr_required: int
    stakeholder_responsiveness: float
    pending_approvals: int
    approval_delay_days: int
    documentation_completion: float
    departments_involved: int
    notification_status: str
    legal_disputes: int
    court_cases: int
    ownership_conflicts: int
    objections_count: int
    compensation_total: float
    compensation_paid: float
    compensation_completion: float
    funding_status: str
    rr_completion: float
    current_stage: str
    planned_duration: int
    elapsed_days: int
    possession_percentage: float
    milestone_delay_days: int
    district_historical_delay_rate: float
    state_historical_delay_rate: float


# -----------------------------------
# Home
# -----------------------------------

@app.get("/")
def home():
    return {
        "message": "Infra Gati API is running"
    }


# -----------------------------------
# Model status
# -----------------------------------

@app.get("/model-status")
def model_status():
    return {
        "model_loaded": True
    }

def get_risk_factors(project):
    factors = []

    if project.milestone_delay_days > 30:
        factors.append("High milestone delay")

    if project.stakeholder_responsiveness < 0.5:
        factors.append("Low stakeholder responsiveness")

    if project.approval_delay_days > 30:
        factors.append("High approval delay")

    if project.documentation_completion < 0.7:
        factors.append("Incomplete documentation")

    if project.compensation_completion < 0.7:
        factors.append("Low compensation completion")

    if project.rr_completion < 0.7:
        factors.append("Incomplete rehabilitation and resettlement")

    if project.pending_approvals > 2:
        factors.append("Multiple pending approvals")

    if project.legal_disputes > 0:
        factors.append("Legal disputes present")

    if project.court_cases > 0:
        factors.append("Court cases present")

    if project.ownership_conflicts > 0:
        factors.append("Ownership conflicts present")

    if project.possession_percentage < 50:
        factors.append("Low land possession")

    return factors

# -----------------------------------
# Prediction
# -----------------------------------

@app.post("/predict")
def predict(project: ProjectData):

    # Convert incoming JSON into a dictionary
    project_data = project.model_dump()

    # Convert dictionary into a DataFrame
    input_data = pd.DataFrame([project_data])

    # Make prediction
    prediction = model.predict(input_data)[0]

    # Get probability of delay
    probability = model.predict_proba(input_data)[0][1]

    # Convert probability into percentage
    probability_percentage = round(probability * 100, 2)

    # Determine risk level
    if probability_percentage < 30:
        risk_level = "LOW"
    elif probability_percentage < 60:
        risk_level = "MEDIUM"
    elif probability_percentage < 80:
        risk_level = "HIGH"
    else:
        risk_level = "CRITICAL"

    # Generate project-specific risk factors
    risk_factors = get_risk_factors(project)

    return {
        "model_version": "1.0",
        "delay_risk": int(prediction),
        "delay_probability": probability_percentage,
        "risk_level": risk_level,
        "risk_factors": risk_factors
    }

