from pydantic import BaseModel

class ImageryErath(BaseModel):
    field_id: int
    lat: float
    lon: float
    dim: float
    date: str | None = None
