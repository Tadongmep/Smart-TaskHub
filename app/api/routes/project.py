from fastapi import APIRouter


router = APIRouter()

@router.get("/projects", response_model=list[str])
def get_projects():
    """
    Get a list of projects.
    """
    # This is a placeholder implementation. Replace with actual database logic.
    return ["Project A", "Project B", "Project C"]