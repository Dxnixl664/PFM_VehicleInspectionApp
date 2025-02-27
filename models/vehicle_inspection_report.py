from pydantic import BaseModel
from datetime import datetime
from typing import List, Optional
from models.trailer import Trailer
from models.truck_inspection_items import TruckInspectionItems


class VehicleInspectionReport(BaseModel):
    carrier: str
    address: str
    inspection_date: datetime
    truck_number: str
    odometer_reading: int
    truck_inspection_items: TruckInspectionItems
    trailers: List[Trailer] = []
    remarks: Optional[str] = None