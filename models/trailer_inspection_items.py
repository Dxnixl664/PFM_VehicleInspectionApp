from pydantic import BaseModel
from typing import Optional


class TrailerInspectionItems(BaseModel):
    brake_connections: bool = False
    brakes: bool = False
    coupling_devices: bool = False
    coupling_king_pin: bool = False
    doors: bool = False
    hitch: bool = False
    landing_gear: bool = False
    lights_all: bool = False
    reflectors_reflective_tape: bool = False
    roof: bool = False
    suspension_system: bool = False
    tarpaulin: bool = False
    tires: bool = False
    wheels_and_rims: bool = False
    other: bool = False
    other_description: Optional[str] = None