#===================================================
# MODELS.PY --> Define las tablas de la base de datos
# Cada clase representa una tabla, y cada atributo
# (Column) representa una columna de esa tabla
#===================================================

from sqlalchemy import Column, Integer, String
from database import Base

#-----------------------------------------------------
# TABLA USUARIOS 
#-----------------------------------------------------
class Usuario(Base):
    __tablename__ = "usuarios"
    
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True)  #unique evita duplicados 
    password = Column(String)   #acá se guarda el hash, no la contrasela real 
    