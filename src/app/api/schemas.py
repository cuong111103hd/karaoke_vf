from pydantic import BaseModel, Field

class JobCreateRequest(BaseModel):
    youtube_url: str = Field(..., description="The YouTube video URL to separate.")
