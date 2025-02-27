from pydantic import BaseModel
from models.trailer_inspection_items import TrailerInspectionItems


class Trailer(BaseModel):
    trailer_number: str
    inspection_items: TrailerInspectionItems