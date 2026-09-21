import pandas as pd
import joblib


model = joblib.load(
    "server/app/ml_models/delay_risk_model.joblib"
)


ML_FEATURES = [
    "state",
    "district",
    "latitude",
    "longitude",
    "project_type",
    "land_area",
    "project_cost",
    "affected_families",
    "landowners",
    "rehabilitation_required",
    "rr_required",
    "stakeholder_responsiveness",
    "pending_approvals",
    "approval_delay_days",
    "documentation_completion",
    "departments_involved",
    "notification_status",
    "legal_disputes",
    "court_cases",
    "ownership_conflicts",
    "objections_count",
    "compensation_total",
    "compensation_paid",
    "compensation_completion",
    "funding_status",
    "rr_completion",
    "current_stage",
    "planned_duration",
    "elapsed_days",
    "possession_percentage",
    "milestone_delay_days",
    "district_historical_delay_rate",
    "state_historical_delay_rate"
]


def predict_project(project):

    input_data = pd.DataFrame(
        [[project[feature] for feature in ML_FEATURES]],
        columns=ML_FEATURES
    )

    prediction = model.predict(input_data)[0]
    probability = model.predict_proba(input_data)[0][1]

    delay_probability = round(probability * 100, 2)

    if probability >= 0.75:
        risk_level = "CRITICAL"
    elif probability >= 0.50:
        risk_level = "HIGH"
    elif probability >= 0.25:
        risk_level = "MEDIUM"
    else:
        risk_level = "LOW"

    risk_factors = []

    if project["milestone_delay_days"] >= 60:
        risk_factors.append("High milestone delay")

    if project["approval_delay_days"] >= 60:
        risk_factors.append("High approval delay")

    if project["stakeholder_responsiveness"] <= 0.5:
        risk_factors.append("Low stakeholder responsiveness")

    if project["compensation_completion"] < 0.5:
        risk_factors.append("Low compensation completion")

    if project["possession_percentage"] < 50:
        risk_factors.append("Low land possession")

    return {
        "project_code": project["project_code"],
        "latitude": project["latitude"],
        "longitude": project["longitude"],
        "delay_risk": int(prediction),
        "delay_probability": delay_probability,
        "risk_level": risk_level,
        "risk_factors": risk_factors
    }