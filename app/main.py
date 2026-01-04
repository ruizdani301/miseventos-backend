from fastapi import FastAPI

#from .infrastructure.persistence.postgresql.database import create_tables
#from .infrastructure.api.routes import user_router
#create_tables()

app = FastAPI()
# app.include_router(
#     router=user_router
# )