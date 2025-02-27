from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List

from models.vehicle_inspection_report import VehicleInspectionReport
from database.models import UserDB
from crud import crud
from modules.auth import get_db, get_current_active_user

router = APIRouter(
    prefix="/reports",
    tags=["reports"],
    responses={404: {"description": "Not found"}},
)


@router.get("/", response_model=List[VehicleInspectionReport])
async def read_reports(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db),
    current_user: UserDB = Depends(get_current_active_user)
):
    """
    Obtener todos los reportes de inspección.

    - **skip**: Cantidad de registros a omitir (para paginación)
    - **limit**: Cantidad máxima de registros a devolver
    """
    reports = crud.get_inspection_reports(db, skip=skip, limit=limit)
    return [crud.convert_db_to_pydantic(report) for report in reports]


@router.get("/{report_id}", response_model=VehicleInspectionReport)
async def read_report(
    report_id: int,
    db: Session = Depends(get_db),
    current_user: UserDB = Depends(get_current_active_user)
):
    """
    Obtener un reporte de inspección específico por su ID.

    - **report_id**: ID del reporte a obtener
    """
    db_report = crud.get_inspection_report(db, report_id=report_id)
    if db_report is None:
        raise HTTPException(status_code=404, detail="Report not found")
    return crud.convert_db_to_pydantic(db_report)


@router.post("/", response_model=VehicleInspectionReport, status_code=status.HTTP_201_CREATED)
async def create_report(
    report: VehicleInspectionReport,
    db: Session = Depends(get_db),
    current_user: UserDB = Depends(get_current_active_user)
):
    """
    Crear un nuevo reporte de inspección.

    - **report**: Datos del reporte a crear
    """
    db_report = crud.create_inspection_report(db, report)
    return crud.convert_db_to_pydantic(db_report)


@router.put("/{report_id}", response_model=VehicleInspectionReport)
async def update_report(
    report_id: int,
    report: VehicleInspectionReport,
    db: Session = Depends(get_db),
    current_user: UserDB = Depends(get_current_active_user)
):
    """
    Actualizar un reporte de inspección existente.

    - **report_id**: ID del reporte a actualizar
    - **report**: Datos actualizados del reporte
    """
    db_report = crud.update_inspection_report(db, report_id, report)
    if db_report is None:
        raise HTTPException(status_code=404, detail="Report not found")
    return crud.convert_db_to_pydantic(db_report)


@router.delete("/{report_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_report(
    report_id: int,
    db: Session = Depends(get_db),
    current_user: UserDB = Depends(get_current_active_user)
):
    """
    Eliminar un reporte de inspección.

    - **report_id**: ID del reporte a eliminar
    """
    success = crud.delete_inspection_report(db, report_id)
    if not success:
        raise HTTPException(status_code=404, detail="Report not found")
    return None