from passlib.context import CryptContext
from jose import jwt
from datetime import datetime, timedelta 
from fastapi import Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError

#configuracion para hashear contraseñas 
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

#clave secreata para firmar los tokens (en un proyecto real, esto va en variables de entorno)
SECRET_KEY = "mi-clave-secreta-super-segura-12345"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

#convierte una contraseña en texto plano a un hash 
def hashear_password(password: str):
    return pwd_context.hash(password)

#verifica que una contraseña coinsida con su hash
def verificar_password(password: str, password_hash: str):
    return pwd_context.verify(password, password_hash)

#crea un token JWT con el username del usuario 
def crear_token(data: dict):
    to_encode = data.copy()
    expira = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expira})   #le agraga fecha de expiración
    token = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return token

#le dice a FastAPI donde esta el endpoint del login 
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login") 
    
def obtener_usuario_actual(token: str = Depends(oauth2_scheme)):
    try: 
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username = payload.get("sub")
        if username is None:
            raise HTTPException(status_code=401, detail="token invalido")
        return username
    except JWTError:
        raise HTTPException(status_code=401, detail="token incalido o expirado")