#=========================================================
# DATABASE.PY --> Configuración de la conexión a SQL
# Este archivo se encarga de crear la conexión a la
# base de datos y dejar todo listo para que los
# modelos (tablas) puedan usarla
#=========================================================


from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

#direccion de la base de datos 
SQLALCHEMY_DATABASE_URL = "sqlite:///./usuarios.db"

#creando la conexión 
#Es el motor de la conexión, el que se comunica con la base de datos
engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
)

#Fabrica de la sesión 
#cada vez que se llama a
# SessionLocal(), se crea una nueva sesión para
# hacer consultas
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Clase base de la que van a heredar todos los modelos
# (tablas) definidos en models.py
Base = declarative_base()