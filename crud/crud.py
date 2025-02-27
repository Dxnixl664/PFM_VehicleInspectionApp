from sqlalchemy.orm import Session
from database.models import UserDB
from models.user import UserCreate, User
from modules.auth import get_password_hash

import database.models as db
from models.trailer import Trailer
from models.trailer_inspection_items import TrailerInspectionItems
from models.truck_inspection_items import TruckInspectionItems
from models.vehicle_inspection_report import VehicleInspectionReport


def create_truck_inspection_items(db_session: Session, items: TruckInspectionItems, report_id: int):
    db_items = db.TruckInspectionItemsDB(
        report_id=report_id,
        air_compressor=items.air_compressor,
        air_lines=items.air_lines,
        battery=items.battery,
        belts_and_hoses=items.belts_and_hoses,
        body=items.body,
        brake_accessories=items.brake_accessories,
        brake_parking=items.brake_parking,
        brake_service=items.brake_service,
        clutch=items.clutch,
        coupling_devices=items.coupling_devices,
        defroster_heater=items.defroster_heater,
        drive_line=items.drive_line,
        engine=items.engine,
        exhaust=items.exhaust,
        fifth_wheel=items.fifth_wheel,
        fluid_levels=items.fluid_levels,
        frame_and_assembly=items.frame_and_assembly,
        front_axle=items.front_axle,
        fuel_tanks=items.fuel_tanks,
        horn=items.horn,
        lights_head_stop=items.lights_head_stop,
        lights_tail_dash=items.lights_tail_dash,
        lights_turn_indicators=items.lights_turn_indicators,
        lights_clearance_marker=items.lights_clearance_marker,
        mirrors=items.mirrors,
        muffler=items.muffler,
        oil_pressure=items.oil_pressure,
        radiator=items.radiator,
        rear_end=items.rear_end,
        reflectors=items.reflectors,
        safety_fire_extinguisher=items.safety_fire_extinguisher,
        safety_flags_flares_fusees=items.safety_flags_flares_fusees,
        safety_reflective_triangles=items.safety_reflective_triangles,
        safety_spare_bulbs_and_fuses=items.safety_spare_bulbs_and_fuses,
        safety_spare_seal_beam=items.safety_spare_seal_beam,
        starter=items.starter,
        steering=items.steering,
        suspension_system=items.suspension_system,
        tire_chains=items.tire_chains,
        tires=items.tires,
        transmission=items.transmission,
        trip_recorder=items.trip_recorder,
        wheels_and_rims=items.wheels_and_rims,
        windows=items.windows,
        windshield_wipers=items.windshield_wipers,
        other=items.other,
        other_description=items.other_description
    )
    db_session.add(db_items)
    db_session.flush()
    return db_items


def create_trailer_inspection_items(db_session: Session, items: TrailerInspectionItems, trailer_id: int):
    db_items = db.TrailerInspectionItemsDB(
        trailer_id=trailer_id,
        brake_connections=items.brake_connections,
        brakes=items.brakes,
        coupling_devices=items.coupling_devices,
        coupling_king_pin=items.coupling_king_pin,
        doors=items.doors,
        hitch=items.hitch,
        landing_gear=items.landing_gear,
        lights_all=items.lights_all,
        reflectors_reflective_tape=items.reflectors_reflective_tape,
        roof=items.roof,
        suspension_system=items.suspension_system,
        tarpaulin=items.tarpaulin,
        tires=items.tires,
        wheels_and_rims=items.wheels_and_rims,
        other=items.other,
        other_description=items.other_description
    )
    db_session.add(db_items)
    db_session.flush()
    return db_items


def create_trailer(db_session: Session, trailer: Trailer, report_id: int):
    db_trailer = db.TrailerDB(
        report_id=report_id,
        trailer_number=trailer.trailer_number
    )
    db_session.add(db_trailer)
    db_session.flush()

    create_trailer_inspection_items(db_session, trailer.inspection_items, db_trailer.id)

    return db_trailer


def create_inspection_report(db_session: Session, report: VehicleInspectionReport):

    db_report = db.InspectionReportDB(
        carrier=report.carrier,
        address=report.address,
        inspection_date=report.inspection_date,
        truck_number=report.truck_number,
        odometer_reading=report.odometer_reading,
        remarks=report.remarks
    )
    db_session.add(db_report)
    db_session.flush()

    create_truck_inspection_items(db_session, report.truck_inspection_items, db_report.id)

    for trailer in report.trailers:
        create_trailer(db_session, trailer, db_report.id)

    db_session.commit()
    return db_report


def get_inspection_report(db_session: Session, report_id: int):
    return db_session.query(db.InspectionReportDB).filter(db.InspectionReportDB.id == report_id).first()


def get_inspection_reports(db_session: Session, skip: int = 0, limit: int = 100):
    return db_session.query(db.InspectionReportDB).offset(skip).limit(limit).all()


def convert_db_to_pydantic(db_report: db.InspectionReportDB) -> VehicleInspectionReport:
    truck_items = TruckInspectionItems(
        air_compressor=db_report.truck_inspection_items.air_compressor,
        air_lines=db_report.truck_inspection_items.air_lines,
        battery=db_report.truck_inspection_items.battery,
        belts_and_hoses=db_report.truck_inspection_items.belts_and_hoses,
        body=db_report.truck_inspection_items.body,
        brake_accessories=db_report.truck_inspection_items.brake_accessories,
        brake_parking=db_report.truck_inspection_items.brake_parking,
        brake_service=db_report.truck_inspection_items.brake_service,
        clutch=db_report.truck_inspection_items.clutch,
        coupling_devices=db_report.truck_inspection_items.coupling_devices,
        defroster_heater=db_report.truck_inspection_items.defroster_heater,
        drive_line=db_report.truck_inspection_items.drive_line,
        engine=db_report.truck_inspection_items.engine,
        exhaust=db_report.truck_inspection_items.exhaust,
        fifth_wheel=db_report.truck_inspection_items.fifth_wheel,
        fluid_levels=db_report.truck_inspection_items.fluid_levels,
        frame_and_assembly=db_report.truck_inspection_items.frame_and_assembly,
        front_axle=db_report.truck_inspection_items.front_axle,
        fuel_tanks=db_report.truck_inspection_items.fuel_tanks,
        horn=db_report.truck_inspection_items.horn,
        lights_head_stop=db_report.truck_inspection_items.lights_head_stop,
        lights_tail_dash=db_report.truck_inspection_items.lights_tail_dash,
        lights_turn_indicators=db_report.truck_inspection_items.lights_turn_indicators,
        lights_clearance_marker=db_report.truck_inspection_items.lights_clearance_marker,
        mirrors=db_report.truck_inspection_items.mirrors,
        muffler=db_report.truck_inspection_items.muffler,
        oil_pressure=db_report.truck_inspection_items.oil_pressure,
        radiator=db_report.truck_inspection_items.radiator,
        rear_end=db_report.truck_inspection_items.rear_end,
        reflectors=db_report.truck_inspection_items.reflectors,
        safety_fire_extinguisher=db_report.truck_inspection_items.safety_fire_extinguisher,
        safety_flags_flares_fusees=db_report.truck_inspection_items.safety_flags_flares_fusees,
        safety_reflective_triangles=db_report.truck_inspection_items.safety_reflective_triangles,
        safety_spare_bulbs_and_fuses=db_report.truck_inspection_items.safety_spare_bulbs_and_fuses,
        safety_spare_seal_beam=db_report.truck_inspection_items.safety_spare_seal_beam,
        starter=db_report.truck_inspection_items.starter,
        steering=db_report.truck_inspection_items.steering,
        suspension_system=db_report.truck_inspection_items.suspension_system,
        tire_chains=db_report.truck_inspection_items.tire_chains,
        tires=db_report.truck_inspection_items.tires,
        transmission=db_report.truck_inspection_items.transmission,
        trip_recorder=db_report.truck_inspection_items.trip_recorder,
        wheels_and_rims=db_report.truck_inspection_items.wheels_and_rims,
        windows=db_report.truck_inspection_items.windows,
        windshield_wipers=db_report.truck_inspection_items.windshield_wipers,
        other=db_report.truck_inspection_items.other,
        other_description=db_report.truck_inspection_items.other_description
    )

    trailers = []
    for db_trailer in db_report.trailers:
        trailer_items = TrailerInspectionItems(
            brake_connections=db_trailer.inspection_items.brake_connections,
            brakes=db_trailer.inspection_items.brakes,
            coupling_devices=db_trailer.inspection_items.coupling_devices,
            coupling_king_pin=db_trailer.inspection_items.coupling_king_pin,
            doors=db_trailer.inspection_items.doors,
            hitch=db_trailer.inspection_items.hitch,
            landing_gear=db_trailer.inspection_items.landing_gear,
            lights_all=db_trailer.inspection_items.lights_all,
            reflectors_reflective_tape=db_trailer.inspection_items.reflectors_reflective_tape,
            roof=db_trailer.inspection_items.roof,
            suspension_system=db_trailer.inspection_items.suspension_system,
            tarpaulin=db_trailer.inspection_items.tarpaulin,
            tires=db_trailer.inspection_items.tires,
            wheels_and_rims=db_trailer.inspection_items.wheels_and_rims,
            other=db_trailer.inspection_items.other,
            other_description=db_trailer.inspection_items.other_description
        )

        trailer = Trailer(
            trailer_number=db_trailer.trailer_number,
            inspection_items=trailer_items
        )

        trailers.append(trailer)


    return VehicleInspectionReport(
        carrier=db_report.carrier,
        address=db_report.address,
        inspection_date=db_report.inspection_date,
        truck_number=db_report.truck_number,
        odometer_reading=db_report.odometer_reading,
        truck_inspection_items=truck_items,
        trailers=trailers,
        remarks=db_report.remarks
    )


def update_inspection_report(db_session: Session, report_id: int, report: VehicleInspectionReport):
    db_report = get_inspection_report(db_session, report_id)
    if not db_report:
        return None

    db_report.carrier = report.carrier
    db_report.address = report.address
    db_report.inspection_date = report.inspection_date
    db_report.truck_number = report.truck_number
    db_report.odometer_reading = report.odometer_reading
    db_report.remarks = report.remarks

    for key, value in report.truck_inspection_items.dict().items():
        if hasattr(db_report.truck_inspection_items, key):
            setattr(db_report.truck_inspection_items, key, value)

    for db_trailer in db_report.trailers:
        db_session.delete(db_trailer)

    for trailer in report.trailers:
        create_trailer(db_session, trailer, db_report.id)

    db_session.commit()
    return db_report


def delete_inspection_report(db_session: Session, report_id: int):
    db_report = get_inspection_report(db_session, report_id)
    if db_report:
        db_session.delete(db_report)
        db_session.commit()
        return True
    return False


def get_user(db: Session, username: str):
    """Get a user by username"""
    return db.query(UserDB).filter(UserDB.username == username).first()


def get_user_by_id(db: Session, user_id: int):
    """Get a user by ID"""
    return db.query(UserDB).filter(UserDB.id == user_id).first()


def create_user(db: Session, user: UserCreate):
    """Create a new user"""
    hashed_password = get_password_hash(user.password)
    db_user = UserDB(
        username=user.username,
        hashed_password=hashed_password
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)

    return User(
        id=db_user.id,
        username=db_user.username
    )


def get_users(db: Session, skip: int = 0, limit: int = 100):
    """Get a list of users"""
    return db.query(UserDB).offset(skip).limit(limit).all()