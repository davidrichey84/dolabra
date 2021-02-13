import fastapi
from models.log_message import log_message

router = fastapi.APIRouter()

@router.post("/v1/classify")
def classify(payload: log_message):
    # do things about classifying the log message
    pass