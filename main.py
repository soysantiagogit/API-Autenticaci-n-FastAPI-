#========================================================
# MAIN.PY --> Archivo principal de la API
# Conecta FastAPI con la base de datos y define
# todos los endpoints (rutas) de la aplicación 
#========================================================
from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from pydantic import BaseModel
from fastapi.security import OAuth2PasswordRequestForm
from database import SessionLocal, engine
import models
import auth

#crea las tablas en la base de datos automaticamente 
# (si ya existe no hace nada)
models.Base.metadata.create_all(bind=engine)


app = FastAPI()

def get_db():
    db = SessionLocal()
    try:
        yield db 
    finally:
        db.close()
        
#esquema para el registro y login 
class UsuarioSchema(BaseModel):
    username: str 
    password: str 

#post/registro --> agrega un nuevo registro 
@app.post("/registro")
def registro(usuario: UsuarioSchema, db: Session = Depends(get_db)):
    #verifica que el username no exista ya 
    existe = db.query(models.Usuario).filter(models.Usuario.username == usuario.username).first()
    if existe: 
        raise HTTPException(status_code=400, detail="El usuario ya existe")
    
    #hashear la contraseña antes de guardarla 
    password_hash = auth.hashear_password(usuario.password)
    
    nuevo_usuario = models.Usuario(username= usuario.username, password= password_hash)
    db.add(nuevo_usuario)
    db.commit()
    db.refresh(nuevo_usuario)
    
    return {"mensaje": "Usuario registrado correctamente", "username": nuevo_usuario.username}


#post/login --> verifica las credenciales y devuelve el token JWT
@app.post("/login")
def login(from_data: OAuth2PasswordRequestForm =  Depends(), db: Session = Depends(get_db)):
    #buscar el usuario por username 
    usuario_db = db.query(models.Usuario).filter(models.Usuario.username == from_data.username).first()
    
    if not usuario_db:
        raise HTTPException(status_code=401, detail="usuario o contraseña incorrectos")
    
    #verifica que la contraseña coincida con el hash guardado 
    if not auth.verificar_password(from_data.password, usuario_db.password):
        raise HTTPException(status_code=401, detail="usuario o contraseña incorrectos")
    
    #si todo esta bien, generar el token 
    token = auth.crear_token({"sub": usuario_db.username})
    return{"access_token": token, "token_type": "bearer"}
  
#get/perfil --> endpoint protegido 
@app.get("/perfil")
def perfil(usuario_actual: str = Depends(auth.obtener_usuario_actual)):
    return {"mensaje": f"hola {usuario_actual}, este es tu perfil protegido"}
