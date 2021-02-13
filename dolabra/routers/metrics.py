import fastapi

router = fastapi.APIRouter()

@router.get("/v1/metrics")
def get_metrics():
    # do stuff here about getting metrics about api requests
    pass