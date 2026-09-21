from fastapi import APIRouter, status, HTTPException

from server.app.database.connection import get_db_connection
from server.app.models.project import (
    ProjectResponse,
    ProjectCreate,
    PredictionResponse
)
from server.app.services.ml_service import (
    predict_project as run_ml_prediction,
    ML_FEATURES
)

router = APIRouter()

@router.get("/projects", response_model=list[ProjectResponse])
def get_projects():
    db = get_db_connection()
    cursor = db.cursor(dictionary=True)

    cursor.execute("SELECT * FROM projects")
    projects = cursor.fetchall()

    cursor.close()
    db.close()

    # Handle projects where project_name is NULL
    for project in projects:
        if not project.get("project_name"):
            project["project_name"] = project.get("project_code", "Unnamed Project")

    return projects

@router.get("/projects/{project_id}", response_model=ProjectResponse)
def get_project(project_id: int):
    db = get_db_connection()
    cursor = db.cursor(dictionary=True)

    cursor.execute(
        "SELECT * FROM projects WHERE id = %s",
        (project_id,)
    )

    project = cursor.fetchone()

    cursor.close()
    db.close()

    if project is None:
        raise HTTPException(
            status_code=404,
            detail="Project not found"
        )

    # Prevent NULL project_name from breaking response validation
    if not project.get("project_name"):
        project["project_name"] = project.get(
            "project_code",
            "Unnamed Project"
        )

    return project

@router.post("/projects", status_code=status.HTTP_201_CREATED)
def create_project(project: ProjectCreate):

    db = get_db_connection()
    cursor = db.cursor()

    query = """
    INSERT INTO projects (
        project_code,
        state,
        district,
        latitude,
        longitude,
        project_type,
        land_area,
        project_cost,
        affected_families,
        landowners,
        rehabilitation_required,
        rr_required,
        stakeholder_responsiveness,
        pending_approvals,
        approval_delay_days,
        documentation_completion,
        departments_involved,
        notification_status,
        legal_disputes,
        court_cases,
        ownership_conflicts,
        objections_count,
        compensation_total,
        compensation_paid,
        compensation_completion,
        funding_status,
        rr_completion,
        current_stage,
        planned_duration,
        elapsed_days,
        possession_percentage,
        milestone_delay_days,
        district_historical_delay_rate,
        state_historical_delay_rate
    )
    VALUES (
        %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s,
        %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s,
        %s, %s, %s, %s, %s, %s, %s, %s, %s, %s
    )
"""

    values = (
    project.project_code,
    project.state,
    project.district,
    project.latitude,
    project.longitude,
    project.project_type,
    project.land_area,
    project.project_cost,
    project.affected_families,
    project.landowners,
    project.rehabilitation_required,
    project.rr_required,
    project.stakeholder_responsiveness,
    project.pending_approvals,
    project.approval_delay_days,
    project.documentation_completion,
    project.departments_involved,
    project.notification_status,
    project.legal_disputes,
    project.court_cases,
    project.ownership_conflicts,
    project.objections_count,
    project.compensation_total,
    project.compensation_paid,
    project.compensation_completion,
    project.funding_status,
    project.rr_completion,
    project.current_stage,
    project.planned_duration,
    project.elapsed_days,
    project.possession_percentage,
    project.milestone_delay_days,
    project.district_historical_delay_rate,
    project.state_historical_delay_rate
)

    try:
        cursor.execute(query, values)
        db.commit()

    except Exception as e:
        db.rollback()
        raise HTTPException(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        detail="Failed to create project"
        )

    cursor.close()
    db.close()

    return {"message": "Project created successfully"}

@router.put("/projects/{project_id}")
def update_project(project_id: int, project: ProjectCreate):

    db = get_db_connection()
    cursor = db.cursor()

    query = """
        UPDATE projects
        SET
            project_code = %s,
            state = %s,
            district = %s,
            latitude = %s,
            longitude = %s,
            project_type = %s,
            land_area = %s,
            project_cost = %s,
            affected_families = %s,
            landowners = %s,
            rehabilitation_required = %s,
            rr_required = %s
        WHERE id = %s
    """

    values = (
        project.project_code,
        project.state,
        project.district,
        project.latitude,
        project.longitude,
        project.project_type,
        project.land_area,
        project.project_cost,
        project.affected_families,
        project.landowners,
        project.rehabilitation_required,
        project.rr_required,
        project_id
    )

    cursor.execute(query, values)
    
    if cursor.rowcount == 0:
        cursor.close()
        db.close()
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Project not found"
        )
    db.commit()

    cursor.close()
    db.close()

    return {"message": "Project updated successfully"}

@router.delete("/projects/{project_id}")
def delete_project(project_id: int):

    db = get_db_connection()
    cursor = db.cursor()

    query = """
        DELETE FROM projects
        WHERE id = %s
    """

    cursor.execute(query, (project_id,))

    if cursor.rowcount == 0:
        cursor.close()
        db.close()
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Project not found"
        )
    db.commit()

    cursor.close()
    db.close()

    return {"message": "Project deleted successfully"}

@router.post(
    "/projects/{project_id}/predict",
    response_model=PredictionResponse
)
def predict_project(project_id: int):

    db = get_db_connection()
    cursor = db.cursor(dictionary=True)

    query = """
        SELECT *
        FROM projects
        WHERE id = %s
    """

    cursor.execute(query, (project_id,))
    project = cursor.fetchone()

    cursor.close()
    db.close()

    if project is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Project not found"
        )
        
    missing_features = [
    feature
    for feature in ML_FEATURES
    if project[feature] is None
    ]

    if missing_features:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail={
                "message": "Project is missing required ML features",
                "missing_features": missing_features
            }
        )

    try:
        prediction_result = run_ml_prediction(project)
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Prediction failed: {str(e)}"
    )

    return prediction_result