### misEventos

* Este proyecto es una API REST para la gestión de eventos, sesiones, ponentes y usuarios.
El obejetivo que busca es simplificar a los potenciales asistentes la tarea de encontrar eventos y registrarse ene llos; Asi como a los organizadores poder gestionar sus eventos, sesiones, ponentes y usuarios.

Este es el backend de una aplicacion fullstack desarrollado con Python y FastAPI, y conectado a una base de datos postgres la cual para efectos de este proyecto se encuentra en un contenedor docker usando la imagen de "postgres:16-alpine", utilizando una arquitectura limpia.

Se usa poetry para la gestion de dependencias.

## Estructura del Proyecto
 ```
miseventos/
├── src/
│   ├── miseventos/
│   │   ├── __init__.py
│   │   ├── main.py
│   │   ├── config.py
│   │   ├── entitis/
│   │   │   ├── __init__.py
│   │   │   ├── event.py
│   │   │   ├── session.py
│   │   │   ├── speaker.py
│   │   │   ├── user.py
│   │   ├── infrastructure/
│   │   │   ├── __init__.py
│   │   │   ├── api/
│   │   │   │   ├── __init__.py
│   │   │   │   ├── routes/
│   │   │   │   │   ├── __init__.py
│   │   │   │   │   ├── event_routes.py
│   │   │   │   │   ├── session_routes.py
│   │   │   │   │   ├── speaker_routes.py
│   │   │   │   │   ├── user_routes.py
│   │   │   │   ├── controllers/
│   │   │   │   │   ├── __init__.py
│   │   │   │   │   ├── event_controller.py
│   │   │   │   │   ├── session_controller.py
│   │   │   │   │   ├── speaker_controller.py
│   │   │   │   │   ├── user_controller.py
│   │   │   ├── persistence/
│   │   │   │   ├── __init__.py
│   │   │   │   ├── postgresql/
│   │   │   │   │   ├── __init__.py
│   │   │   │   │   ├── models/
│   │   │   │   │   │   ├── __init__.py
│   │   │   │   │   │   ├── database.py
│   │   │   │   │   │   ├── event_model.py
│   │   │   │   │   │   ├── session_model.py
│   │   │   │   │   │   ├── speaker_model.py
│   │   │   │   │   │   ├── user_model.py
│   │   │   │   │   ├── implement/
│   │   │   │   │   │   ├── __init__.py
│   │   │   │   │   │   ├── event_implemet.py
│   │   │   │   │   │   ├── session_implement.py
│   │   │   │   │   │   ├── speaker_implement.py
│   │   │   │   │   │   ├── user_implement.py
│   │   │   │   │   ├── schemas/
│   │   │   │   │   │   ├── __init__.py
│   │   │   │   │   │   ├── event_schema.py
│   │   │   │   │   │   ├── session_schema.py
│   │   │   │   │   │   ├── speaker_schema.py
│   │   │   │   │   │   ├── user_schema.py
│   │   │   │   │   │   ├── schema.py
│   │   ├── repositories/
│   │   │   ├── __init__.py
│   │   │   ├── event_repository.py
│   │   │   ├── session_repository.py
│   │   │   ├── speaker_repository.py
│   │   │   ├── user_repository.py
│   │   ├── use_case/
│   │   │   ├── __init__.py
│   │   │   ├── event_usecase.py
│   │   │   ├── session_usecase.py
│   │   │   ├── speaker_usecase.py
│   │   │   ├── user_usecase.py
│   ├── token_jwt/
│   │   ├── __init__.py
│   │   ├── jwt_handler.py
│   │   ├
│   ├── tests/
│   │   ├── __init__.py
│   │   ├── test_event.py
│   │   ├── test_session.py
│   │   ├── test_speaker.py
│   │   ├── test_user.py
```
## Instalación
 - Se recomienda ustilizar docker para la instalacion de este proyecto, el archivo Dockerfile se encuentra en la raiz del proyecto,
 - Puedes crear el .env con las configuracion necesarias
 ejemplo de .env
    ```env
   DATABASE_URL=postgresql://<usuario>:<contraseña>@<host>:<puerto>/<nombre_de_la_base_de_datos>
   SECRET_KEY=<tu_contraseña>
   ALGORITHM=<algoritmo>
    * docker build -t miseventos-backend .
 * docker run -d -p 8000:8000 --name miseventos-backend miseventos-backend

- Debido a que este proyecto hace parte de una aplicación completa se recomienda seguir las intrucciones del README.md del repositorio : [eventos](https://github.com/ruizdani301/eventos),  el cual explica como clonar los repositorios vinculados a este, y levanta la aplicacion usando docker-compose.yml.

- Si deseas instalarlo de forma individual localmente, sigue los siguientes pasos:
    * Clonar el repositorio
    * Crear un entorno virtual 
    * Instalar dependencias usando poetry
    * Configurar la base de datos la cual recomiendo q sea postgres >=16 y < 18
    * Levantar la aplicacion


1. **Clonar el repositorio**
```
git clone git@github.com:ruizdani301/miseventos-backend.git
   cd miseventos-backend
```

2. **Crear un entorno virtual**
   ```bash
   python3 -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Instalar dependencias**
   ```bash
   poetry install
   ```

## Configuration

1. **Crea  un `.env` archivo** in the `src/miseventos-backend/`  basada en la configuracion abajo expuesta
 

- DATABASE_URL=postgresql://usuario:contraseña@host:puerto/nombre_de_la_base_de_datos
- SECRET_KEY=tu_contraseña
- ALGORITHM=algoritmo
- ACCESS_TOKEN_EXPIRE_MINUTES=minutos
   


3. **Aplicar migraciones**:
   ```bash
   poetry run alembic upgrade head
   

## Ejecutar la aplicacion
```bash
poetry run uvicorn src.miseventos-backend.main:app --reload
