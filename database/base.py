from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

# Configuración de la conexión a la base de datos
SQLALCHEMY_DATABASE_URL = "sqlite:///./vehicle_inspection.db"
# Para PostgreSQL usaríamos algo como:
# SQLALCHEMY_DATABASE_URL = "postgresql://user:password@postgresserver/db"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)