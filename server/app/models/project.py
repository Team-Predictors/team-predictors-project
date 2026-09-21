from pydantic import BaseModel


class ProjectResponse(BaseModel):

    project_name: str
    id: int
    project_code: str
    user_id: int | None

    state: str | None
    district: str | None

    latitude: float | None
    longitude: float | None

    project_type: str | None

    land_area: float | None
    project_cost: float | None

    affected_families: int | None
    landowners: int | None

    rehabilitation_required: bool | None
    rr_required: bool | None

class ProjectCreate(BaseModel):
    project_code: str

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

class PredictionResponse(BaseModel):
    project_code: str
    latitude: float
    longitude: float
    delay_risk: int
    delay_probability: float
    risk_level: str
    risk_factors: list[str]