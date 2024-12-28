from pydantic import BaseModel, HttpUrl

class VideoRequest(BaseModel):
    url: str

class SummaryResponse(BaseModel):
    summary: str
    status: str = "success"