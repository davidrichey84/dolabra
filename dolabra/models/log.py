from pydantic import BaseModel, validator

class LogMessage(BaseModel):
    #message: dict
    message: str
    #@validator('message')
    #def _check_none(cls, value):
    #    if not value:
    #        raise ValueError
    #    else:
    #        return value