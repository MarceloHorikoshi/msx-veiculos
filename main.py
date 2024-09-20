from typing import Annotated
from fastapi import FastAPI, Depends

from src.models import models_db as models
from src.dependencies.database import engine, SessionLocal

from sqlalchemy.orm import Session

from src.routes import users, veiculos

app = FastAPI(
    title='API-VEICULOS',
    description='API com CRUD e gerador de token para login',
)


models.Base.metadata.create_all(bind=engine)


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


db_dependency = Annotated[Session, Depends(get_db)]

app.include_router(users.router)
app.include_router(veiculos.router)

