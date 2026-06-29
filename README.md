 API Autenticación FastAPI 

API REST desarrollada con **FastAPI**, **SQLAlchemy** y **JWT** que implementa un sistema de autenticación de usuarios: registro, login y rutas protegidas.

## Tecnologías utilizadas

- **Python 3**
- **FastAPI** — framework para construir la API
- **SQLAlchemy** — ORM para conectar con la base de datos
- **SQLite** — base de datos
- **Pydantic** — validación de datos
- **Passlib (bcrypt)** — hasheo seguro de contraseñas
- **python-jose** — creación y validación de tokens JWT
- **Uvicorn** — servidor ASGI

##  Funcionalidades

- `POST /registro` — registra un nuevo usuario (la contraseña se guarda hasheada, nunca en texto plano)
- `POST /login` — valida las credenciales y devuelve un token JWT
- `GET /perfil` — ruta protegida, solo accesible con un token válido

##  ¿Cómo funciona la autenticación?

1. **Registro:** el usuario envía `username` y `password`. La contraseña se hashea con bcrypt antes de guardarse en la base de datos.
2. **Login:** el usuario envía sus credenciales. Si son correctas, la API genera un **token JWT** con una expiración de 30 minutos.
3. **Acceso a rutas protegidas:** el usuario envía el token en el header `Authorization: Bearer <token>`. La API valida el token antes de responder.

##  Estructura del proyecto

```
api-auth/
├── main.py        # Endpoints de la API
├── models.py      # Tabla de usuarios (SQLAlchemy)
├── database.py    # Configuración de la conexión a SQL
├── auth.py        # Hasheo de contraseñas, creación y validación de JWT
└── usuarios.db    # Base de datos SQLite (se genera automáticamente)
```

##  Instalación y uso

1. Cloná el repositorio:
   ```bash
   git clone https://github.com/soysantiagogit/api-autenticacion-fastapi.git
   cd api-autenticacion-fastapi
   ```

2. Instalá las dependencias:
   ```bash
   pip install fastapi uvicorn sqlalchemy passlib[bcrypt] python-jose[cryptography] python-multipart bcrypt==4.0.1
   ```

3. Corré el servidor:
   ```bash
   python -m uvicorn main:app --reload
   ```

4. Abrí la documentación interactiva (Swagger UI):
   ```
   http://127.0.0.1:8000/docs
   ```

##  Cómo probar la autenticación en Swagger

1. Registrá un usuario en `POST /registro` con `username` y `password`.
2. Hacé clic en el botón **Authorize**  (arriba a la derecha).
3. Completá `username` y `password` (dejá vacíos `client_id` y `client_secret`).
4. Hacé clic en **Authorize** y luego en **Close**.
5. Probá `GET /perfil` — debería devolver un mensaje personalizado con tu usuario.
6. Si probás sin autorizar, la ruta devuelve error `401 Unauthorized`.

##  Aprendizajes aplicados en este proyecto

- Hasheo seguro de contraseñas con bcrypt (nunca se guardan en texto plano)
- Generación y validación de tokens JWT
- Protección de endpoints con `Depends` y `OAuth2PasswordBearer`
- Manejo de errores de autenticación con códigos HTTP `401`
- Integración del flujo OAuth2 con la documentación interactiva de Swagger

##  Posibles mejoras futuras

- Roles de usuario (admin / usuario común)
- Refresh tokens para renovar la sesión sin volver a hacer login
- Relacionar esta autenticación con otra API (por ejemplo, proteger una API de productos)
- Tests automatizados

---

Proyecto desarrollado como parte de mi proceso de aprendizaje en desarrollo backend con Python.
