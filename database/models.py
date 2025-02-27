from sqlalchemy import Boolean, Column, ForeignKey, Integer, String, Date, Time, Enum, Text, DateTime
from sqlalchemy.orm import relationship, declarative_base

Base = declarative_base()

class TruckInspectionItemsDB(Base):
    __tablename__ = "truck_inspection_items"

    id = Column(Integer, primary_key=True, index=True)
    report_id = Column(Integer, ForeignKey("inspection_reports.id"))
    air_compressor = Column(Boolean, default=False)
    air_lines = Column(Boolean, default=False)
    battery = Column(Boolean, default=False)
    belts_and_hoses = Column(Boolean, default=False)
    body = Column(Boolean, default=False)
    brake_accessories = Column(Boolean, default=False)
    brake_parking = Column(Boolean, default=False)
    brake_service = Column(Boolean, default=False)
    clutch = Column(Boolean, default=False)
    coupling_devices = Column(Boolean, default=False)
    defroster_heater = Column(Boolean, default=False)
    drive_line = Column(Boolean, default=False)
    engine = Column(Boolean, default=False)
    exhaust = Column(Boolean, default=False)
    fifth_wheel = Column(Boolean, default=False)
    fluid_levels = Column(Boolean, default=False)
    frame_and_assembly = Column(Boolean, default=False)
    front_axle = Column(Boolean, default=False)
    fuel_tanks = Column(Boolean, default=False)
    horn = Column(Boolean, default=False)
    lights_head_stop = Column(Boolean, default=False)
    lights_tail_dash = Column(Boolean, default=False)
    lights_turn_indicators = Column(Boolean, default=False)
    lights_clearance_marker = Column(Boolean, default=False)
    mirrors = Column(Boolean, default=False)
    muffler = Column(Boolean, default=False)
    oil_pressure = Column(Boolean, default=False)
    radiator = Column(Boolean, default=False)
    rear_end = Column(Boolean, default=False)
    reflectors = Column(Boolean, default=False)
    safety_fire_extinguisher = Column(Boolean, default=False)
    safety_flags_flares_fusees = Column(Boolean, default=False)
    safety_reflective_triangles = Column(Boolean, default=False)
    safety_spare_bulbs_and_fuses = Column(Boolean, default=False)
    safety_spare_seal_beam = Column(Boolean, default=False)
    starter = Column(Boolean, default=False)
    steering = Column(Boolean, default=False)
    suspension_system = Column(Boolean, default=False)
    tire_chains = Column(Boolean, default=False)
    tires = Column(Boolean, default=False)
    transmission = Column(Boolean, default=False)
    trip_recorder = Column(Boolean, default=False)
    wheels_and_rims = Column(Boolean, default=False)
    windows = Column(Boolean, default=False)
    windshield_wipers = Column(Boolean, default=False)
    other = Column(Boolean, default=False)
    other_description = Column(String, nullable=True)

    report = relationship("InspectionReportDB", back_populates="truck_inspection_items")


class TrailerInspectionItemsDB(Base):
    __tablename__ = "trailer_inspection_items"

    id = Column(Integer, primary_key=True, index=True)
    trailer_id = Column(Integer, ForeignKey("trailers.id"))
    brake_connections = Column(Boolean, default=False)
    brakes = Column(Boolean, default=False)
    coupling_devices = Column(Boolean, default=False)
    coupling_king_pin = Column(Boolean, default=False)
    doors = Column(Boolean, default=False)
    hitch = Column(Boolean, default=False)
    landing_gear = Column(Boolean, default=False)
    lights_all = Column(Boolean, default=False)
    reflectors_reflective_tape = Column(Boolean, default=False)
    roof = Column(Boolean, default=False)
    suspension_system = Column(Boolean, default=False)
    tarpaulin = Column(Boolean, default=False)
    tires = Column(Boolean, default=False)
    wheels_and_rims = Column(Boolean, default=False)
    other = Column(Boolean, default=False)
    other_description = Column(String, nullable=True)

    trailer = relationship("TrailerDB", back_populates="inspection_items")


class TrailerDB(Base):
    __tablename__ = "trailers"

    id = Column(Integer, primary_key=True, index=True)
    report_id = Column(Integer, ForeignKey("inspection_reports.id"))
    trailer_number = Column(String, index=True)

    report = relationship("InspectionReportDB", back_populates="trailers")
    inspection_items = relationship("TrailerInspectionItemsDB", uselist=False, back_populates="trailer", cascade="all, delete-orphan")


class InspectionReportDB(Base):
    __tablename__ = "inspection_reports"

    id = Column(Integer, primary_key=True, index=True)
    carrier = Column(String, index=True)
    address = Column(String)
    inspection_date = Column(DateTime)
    truck_number = Column(String, index=True)
    odometer_reading = Column(Integer)
    remarks = Column(Text, nullable=True)

    truck_inspection_items = relationship("TruckInspectionItemsDB", uselist=False, back_populates="report", cascade="all, delete-orphan")
    trailers = relationship("TrailerDB", back_populates="report", cascade="all, delete-orphan")


class UserDB(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True)
    hashed_password = Column(String)
    is_active = Column(Boolean, default=True)